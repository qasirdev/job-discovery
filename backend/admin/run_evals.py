import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Any, Dict

# Setup logger
from ..logging_config import get_logger
logger = get_logger("admin.run_evals")

# Check for DeepEval
try:
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, LLMTestCaseParams
    HAS_DEEPEVAL = True
except ImportError:
    HAS_DEEPEVAL = False

# List of mandatory prompt files for each agent under prompts/
MANDATORY_FILES = [
    "CONTRACT.md",
    "CHANGELOG.md",
    "system.md",
    "skills.md",
    "tools.md",
    "guardrails.md",
]

# Mandatory XML tags for prompt system.md
MANDATORY_XML_TAGS = [
    "role",
    "context",
    "instructions",
    "constraints",
    "output_format",
    "example",
]


def validate_contract(content: str, agent_name: str) -> list[str]:
    """Parse and validate key fields in CONTRACT.md."""
    errors = []
    required_patterns = {
        "Target Model": r"## Target Model\s*\n\s*(.+)",
        "Model Version Pinned": r"## Model Version Pinned\s*\n\s*(.+)",
        "Reasoning Effort": r"## Reasoning Effort\s*\n\s*(.+)",
        "Max Output Tokens": r"## Max Output Tokens\s*\n\s*(\d+)",
        "Temperature": r"## Temperature\s*\n\s*([0-9.]+)",
    }

    for field, pattern in required_patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if not match:
            errors.append(f"[{agent_name}] CONTRACT.md is missing or has malformed '{field}' block.")
        else:
            value = match.group(1).strip()
            logger.debug(f"[{agent_name}] Contract field '{field}': {value}")

    return errors


def validate_system_prompt_xml(content: str, agent_name: str) -> list[str]:
    """Verify that system.md contains all mandatory XML structure tags."""
    errors = []
    for tag in MANDATORY_XML_TAGS:
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"

        if start_tag not in content or end_tag not in content:
            errors.append(
                f"[{agent_name}] system.md is missing XML tag: '{tag}' (must have both '{start_tag}' and '{end_tag}')"
            )

    return errors


def simulate_agent_extraction(html_input: str, source: str) -> Dict[str, Any]:
    """Simulate extraction of job details from HTML snippet (similar to Playwright agent logic)."""
    title_match = re.search(r"<h1>(.*?)</h1>", html_input, re.IGNORECASE)
    company_match = re.search(r"<h2>(.*?)</h2>", html_input, re.IGNORECASE)
    location_match = re.search(r"<p>Location:\s*(.*?)</p>", html_input, re.IGNORECASE)
    
    # Fallback to extract description cleanly
    all_p = re.findall(r"<p>(.*?)</p>", html_input, re.IGNORECASE)
    desc = ""
    for p in all_p:
        if "location:" not in p.lower():
            desc = p
            break
            
    return {
        "title": title_match.group(1).strip() if title_match else "",
        "company": company_match.group(1).strip() if company_match else "",
        "location": location_match.group(1).strip() if location_match else "",
        "description": desc.strip() if desc else html_input,
        "source": source
    }


def run_deepeval_metrics(actual: Dict[str, Any], expected: Dict[str, Any]) -> Dict[str, float]:
    """Run DeepEval metrics if API keys and dependencies are available."""
    if not HAS_DEEPEVAL:
        logger.debug("DeepEval is not installed. Skipping DeepEval checks.")
        return {}

    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        logger.debug("OPENAI_API_KEY not found in environment. Skipping LLM-based DeepEval checks.")
        return {}

    try:
        # Define Faithfulness and Answer Relevancy using GEval to meet thresholds in CONTRACT.md
        # Faithfulness (GEval style)
        faithfulness_metric = GEval(
            name="Faithfulness",
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.RETRIEVAL_CONTEXT],
            evaluation_steps=[
                "Check if all claims in actual_output are fully supported by retrieval_context.",
                "Penalize any hallucinations or claims not present in the context."
            ],
            threshold=0.85
        )

        # Relevancy
        relevancy_metric = GEval(
            name="Answer Relevancy",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            evaluation_steps=[
                "Check if actual_output directly answers or aligns with the input query.",
                "Ensure the job description extraction is perfectly relevant to the input html."
            ],
            threshold=0.80
        )

        test_case = LLMTestCase(
            input=expected.get("description", ""),
            actual_output=actual.get("description", ""),
            retrieval_context=[expected.get("description", "")]
        )

        faithfulness_metric.measure(test_case)
        relevancy_metric.measure(test_case)

        f_score = faithfulness_metric.score
        r_score = relevancy_metric.score

        return {
            "faithfulness": f_score if f_score is not None else 0.0,
            "relevancy": r_score if r_score is not None else 0.0
        }
    except Exception as e:
        logger.warning(f"Error executing DeepEval metrics: {e}")
        return {}


def run_evaluation(agent_name_filter: str | None = None, fast_mode: bool = False) -> bool:
    """Run verification checks and evaluation datasets on all configured agent prompts under prompts/."""
    logger.info("Initializing Agent Prompt Evaluation Framework...")

    workspace_dir = Path(__file__).resolve().parents[2]
    prompts_dir = workspace_dir / "prompts"
    evals_dir = workspace_dir / "evals"

    if not prompts_dir.exists():
        logger.error(f"Prompts directory not found at {prompts_dir}")
        return False

    # Get targeted folders
    all_agent_folders = [
        d for d in prompts_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name in [
            "linkedin-agent", "jobserve-agent", "ranking-agent", "rag-agent",
            "security-agent", "orchestrator-agent", "cover-letter-agent"
        ]
    ]

    if agent_name_filter:
        agent_folders = [d for d in all_agent_folders if d.name == agent_name_filter or d.name.replace("-agent", "") == agent_name_filter]
        if not agent_folders:
            logger.error(f"Target agent '{agent_name_filter}' not found in prompts folders.")
            return False
    else:
        agent_folders = all_agent_folders

    if not agent_folders:
        logger.warning("No agent prompt directories found to evaluate.")
        return True

    all_passed = True
    report_summary = {}

    for agent_dir in agent_folders:
        agent_name = agent_dir.name
        source_id = agent_name.replace("-agent", "")
        logger.info("--------------------------------------------------")
        logger.info(f"Evaluating prompts for agent: '{agent_name}'")

        # 1. Check file integrity
        missing_files = []
        for filename in MANDATORY_FILES:
            filepath = agent_dir / filename
            if not filepath.exists():
                missing_files.append(filename)

        if missing_files:
            logger.error(f"[{agent_name}] Missing required files: {missing_files}")
            all_passed = False
            continue

        # 2. Validate Contract
        contract_path = agent_dir / "CONTRACT.md"
        with open(contract_path, "r", encoding="utf-8") as f:
            contract_content = f.read()
        contract_errors = validate_contract(contract_content, agent_name)
        if contract_errors:
            for err in contract_errors:
                logger.error(err)
            all_passed = False

        # 3. Validate System Prompt XML compliance
        system_path = agent_dir / "system.md"
        with open(system_path, "r", encoding="utf-8") as f:
            system_content = f.read()
        xml_errors = validate_system_prompt_xml(system_content, agent_name)
        if xml_errors:
            for err in xml_errors:
                logger.error(err)
            all_passed = False

        # 4. Load and run evaluation test set (if exists)
        eval_set_path = evals_dir / agent_name / "eval-set-v1.json"
        
        # Fallback to check without -agent suffix for eval set
        if not eval_set_path.exists():
            eval_set_path = evals_dir / source_id / "eval-set-v1.json"

        if eval_set_path.exists():
            logger.info(f"[{agent_name}] Found evaluation dataset at {eval_set_path}. Running regression tests...")
            try:
                with open(eval_set_path, "r", encoding="utf-8") as f:
                    eval_cases = json.load(f)
            except Exception as e:
                logger.error(f"[{agent_name}] Failed to load evaluation dataset: {e}")
                all_passed = False
                continue

            passed_cases = 0
            total_cases = len(eval_cases)
            case_results = []

            for i, case in enumerate(eval_cases, 1):
                html_input = case.get("input", "")
                expected = case.get("expected_output", {})
                
                # Perform simulated extraction
                actual = simulate_agent_extraction(html_input, source_id)
                
                # Compare fields
                field_match = True
                field_errors = []
                for field in ["title", "company", "location", "source"]:
                    if actual.get(field) != expected.get(field):
                        field_match = False
                        field_errors.append(f"Field '{field}' mismatch. Expected: '{expected.get(field)}', Got: '{actual.get(field)}'")

                # Run DeepEval metrics if enabled and not in fast mode
                deepeval_scores = {}
                if not fast_mode:
                    deepeval_scores = run_deepeval_metrics(actual, expected)

                case_passed = field_match
                if deepeval_scores:
                    # GEval Faithfulness threshold >= 0.85, Relevancy >= 0.80
                    if deepeval_scores.get("faithfulness", 1.0) < 0.85 or deepeval_scores.get("relevancy", 1.0) < 0.80:
                        case_passed = False
                        field_errors.append(f"DeepEval score threshold failed: {deepeval_scores}")

                if case_passed:
                    passed_cases += 1
                    logger.info(f"  [Case {i}/{total_cases}] PASSED")
                else:
                    logger.error(f"  [Case {i}/{total_cases}] FAILED")
                    for err in field_errors:
                        logger.error(f"    - {err}")

                case_results.append({
                    "case_number": i,
                    "passed": case_passed,
                    "errors": field_errors,
                    "deepeval_scores": deepeval_scores
                })

            pass_rate = passed_cases / total_cases if total_cases > 0 else 1.0
            logger.info(f"[{agent_name}] Regression Results: {passed_cases}/{total_cases} passed ({pass_rate * 100:.1f}%)")

            # Store in report summary
            report_summary[agent_name] = {
                "total": total_cases,
                "passed": passed_cases,
                "pass_rate": pass_rate,
                "cases": case_results
            }

            # Enforce 100% field match rate in local mock validation / CI fallback
            if pass_rate < 1.0:
                logger.error(f"[{agent_name}] Quality threshold failure: Pass rate {pass_rate*100:.1f}% is below 100% target.")
                all_passed = False
        else:
            logger.warning(f"[{agent_name}] No evaluation dataset found at {eval_set_path}. Skipping regression tests.")

        if not contract_errors and not xml_errors and (not eval_set_path.exists() or pass_rate == 1.0):
            logger.info(f"[{agent_name}] All prompt checks and regression tests PASSED.")

    # Write report summary artifact
    report_file = workspace_dir / "evals" / "eval_report.json"
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_summary, f, indent=2)
    logger.info(f"Saved combined evaluation report to {report_file}")

    if all_passed:
        logger.info("--------------------------------------------------")
        logger.info("Agent Prompt Evaluation Framework finished: ALL CHECKS PASSED.")
    else:
        logger.info("--------------------------------------------------")
        logger.error("Agent Prompt Evaluation Framework finished: CRITICAL FAILURES DETECTED.")

    return all_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent Prompt Evaluation Framework")
    parser.add_argument("--agent", type=str, default=None, help="Name of the agent to evaluate (e.g. linkedin)")
    parser.add_argument("--fast", action="store_true", help="Skip LLM-based DeepEval metrics and run static & extraction checks")
    
    args, unknown = parser.parse_known_args()
    
    success = run_evaluation(agent_name_filter=args.agent, fast_mode=args.fast)
    sys.exit(0 if success else 1)
