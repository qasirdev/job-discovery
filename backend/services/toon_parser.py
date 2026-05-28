import re
import json
from pydantic import BaseModel
from typing import Type, TypeVar
from ..logging_config import get_logger

logger = get_logger(__name__)

T = TypeVar('T', bound=BaseModel)

def generate_toon_instruction(response_model: Type[BaseModel] | None) -> str:
    """
    Generates a prompt instruction enforcing the [TOON] wrapper format.
    Required for chatty local LLMs (GGUF fallback models).
    """
    if not response_model:
        return ""
    
    schema = response_model.model_json_schema()
    return (
        "You MUST wrap your JSON output inside [TOON] and [/TOON] tags. "
        "Do not include any conversational filler inside the tags. "
        f"The JSON must strictly conform to this schema: {json.dumps(schema)}"
    )

def parse_toon_response(content: str, response_model: Type[T]) -> T:
    """
    Extracts JSON wrapped in [TOON]...[/TOON] and validates it against the response_model.
    """
    # Try to find [TOON] tags
    match = re.search(r'\[TOON\](.*?)\[/TOON\]', content, re.DOTALL | re.IGNORECASE)
    
    if match:
        json_str = match.group(1).strip()
    else:
        # Fallback if the model ignored the tags, try extracting markdown code blocks
        logger.warning("No [TOON] tags found, attempting fallback extraction.")
        md_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if md_match:
            json_str = md_match.group(1).strip()
        else:
            json_str = content.strip()
            
    # TOON Parsing Bug fix (JD-317): Handle partial JSON or missing braces
    start_idx = json_str.find('{')
    end_idx = json_str.rfind('}')
    
    if start_idx != -1:
        if end_idx != -1 and end_idx > start_idx:
            json_str = json_str[start_idx:end_idx+1]
        else:
            json_str = json_str[start_idx:] + '}'
            
    try:
        parsed = json.loads(json_str)
        return response_model.model_validate(parsed)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from LLM: {json_str}")
        raise ValueError(f"LLM returned invalid JSON: {e}")
