"""
evals/ragas_stub.py

Placeholder for Ragas evaluation metrics (retrieval_precision, context_recall).
This stub returns null values until the RAG agent and corpus are fully implemented in MVP 2 (JD-E9).

JD-38 / MVP 1.1 requirement.
"""

from typing import Any, Dict

def evaluate() -> Dict[str, Any]:
    """
    Stub evaluation returning null values for Ragas metrics.
    Will be fully implemented with vector DB integration in MVP 2.
    """
    return {
        "retrieval_precision": None,
        "context_recall": None
    }
