import re
import sys
from pathlib import Path
from ..logging_config import get_logger

logger = get_logger("admin.run_evals")

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


def run_evaluation() -> bool:
    """Run verification checks on all configured agent prompts under prompts/."""
    logger.info("Initializing Agent Prompt Evaluation Framework...")

    # Root of the monorepo from backend/admin/run_evals.py is two directories up from backend/
    workspace_dir = Path(__file__).resolve().parents[2]
    prompts_dir = workspace_dir / "prompts"

    if not prompts_dir.exists():
        logger.error(f"Prompts directory not found at {prompts_dir}")
        return False

    agent_folders = [
        d for d in prompts_dir.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name in ["linkedin-agent", "jobserve-agent"]
    ]

    if not agent_folders:
        logger.warning("No agent prompt directories found to evaluate.")
        return True

    all_passed = True

    for agent_dir in agent_folders:
        agent_name = agent_dir.name
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

        if not contract_errors and not xml_errors:
            logger.info(f"[{agent_name}] All prompt structure checks PASSED successfully.")

    if all_passed:
        logger.info("Agent Prompt Evaluation Framework finished: ALL CHECKS PASSED.")
    else:
        logger.error("Agent Prompt Evaluation Framework finished: CRITICAL FAILURES DETECTED.")

    return all_passed


if __name__ == "__main__":
    success = run_evaluation()
    sys.exit(0 if success else 1)
