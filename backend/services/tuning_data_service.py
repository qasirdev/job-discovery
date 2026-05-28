import json
import os
from pathlib import Path
from datetime import datetime, timezone
import fcntl
from ..logging_config import get_logger

logger = get_logger(__name__)

class TuningDataService:
    """
    Service to track failed evaluation cases as negative examples for agent tuning.
    Addresses JD-303: Model Tuning Data Loop.
    Extracts failure cases, saves them to a separate JSONL dataset, and prevents unbounded growth.
    """
    
    def __init__(self, data_dir: str | Path | None = None, max_examples: int = 1000):
        if data_dir is None:
            # Default to a 'data/tuning' dir at project root
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data" / "tuning"
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.negative_examples_file = self.data_dir / "negative_examples.jsonl"
        self.max_examples = max_examples

    def record_failure(self, agent_id: str, prompt: str, output: str, feedback: list[str], critic_score: float = 0.0) -> None:
        """
        Record a failed case into the negative examples JSONL file.
        Prevents unbounded growth by keeping only the last `max_examples`.
        """
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent_id": agent_id,
            "prompt": prompt,
            "output": output,
            "feedback": feedback,
            "critic_score": critic_score
        }
        
        try:
            records = []
            if self.negative_examples_file.exists():
                with open(self.negative_examples_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            records.append(line)
            
            records.append(json.dumps(record) + "\n")
            
            if len(records) > self.max_examples:
                records = records[-self.max_examples:]
                
            with open(self.negative_examples_file, "w", encoding="utf-8") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.writelines(records)
                fcntl.flock(f, fcntl.LOCK_UN)
                
            logger.info(f"Recorded tuning failure for agent {agent_id}. Total records: {len(records)}")
            
        except Exception as e:
            logger.error(f"Failed to record tuning data: {e}", exc_info=True)

    def get_negative_examples(self, agent_id: str, limit: int = 3) -> list[dict]:
        """
        Retrieve negative examples for a specific agent to be included in prompt `<example>` blocks.
        """
        if not self.negative_examples_file.exists():
            return []
            
        examples = []
        try:
            with open(self.negative_examples_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if line.strip():
                        try:
                            record = json.loads(line)
                            if record.get("agent_id") == agent_id:
                                examples.append(record)
                                if len(examples) >= limit:
                                    break
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            logger.error(f"Failed to retrieve negative examples: {e}", exc_info=True)
            
        return examples
        
    def format_for_prompt(self, agent_id: str, limit: int = 3) -> str:
        """
        Format negative examples into a markdown string suitable for prompt injection.
        """
        examples = self.get_negative_examples(agent_id, limit)
        if not examples:
            return ""
            
        formatted = "\n### Negative Examples (Do NOT do this):\n"
        for i, ex in enumerate(examples, 1):
            formatted += f"\n**Example {i}**\n"
            formatted += f"- **Failed Output**:\n{ex.get('output', '')}\n"
            formatted += f"- **Critic Feedback (Why it failed)**:\n"
            for f in ex.get('feedback', []):
                formatted += f"  * {f}\n"
                
        return formatted
