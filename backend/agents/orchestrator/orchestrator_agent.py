from ...logging_config import get_logger
from ...models import Job, RankingResult
from ..ranking.ranking_agent import RankingAgent
from ..rag.rag_agent import RAGAgent
from ..cover_letter.cover_letter_agent import CoverLetterAgent
from ..security.security_agent import SecurityAgent

logger = get_logger(__name__)

class OrchestratorAgent:
    """Coordinates the entire processing pipeline for a newly discovered Job."""

    def __init__(self):
        self.security = SecurityAgent()
        self.ranking = RankingAgent()
        self.rag = RAGAgent()
        self.cover_letter = CoverLetterAgent()

    async def process_job(self, job: Job) -> dict:
        """Run the DIFA-compliant workflow for a single job."""
        logger.info(f"Orchestrator starting pipeline for job: {job.id}")
        
        # Step 1: Security Validation
        safe_desc = await self.security.sanitize_input(job.description)
        sec_result = await self.security.validate_for_injection(safe_desc)
        if not sec_result.is_safe:
            logger.warning(f"Job {job.id} failed security check: {sec_result.reason}")
            return {"status": "rejected", "reason": sec_result.reason}
        
        # Update job with sanitized description
        job.description = safe_desc

        # Step 2: Ranking
        ranking_result: RankingResult = await self.ranking.evaluate_job(job)
        
        if ranking_result.is_relevant and ranking_result.score > 80:
            # Step 3: High relevance -> RAG + Cover Letter
            context = await self.rag.retrieve_context(job.description)
            letter_result = await self.cover_letter.generate_cover_letter(job, context)
            
            logger.info(f"Pipeline complete. Generated cover letter for {job.id} with ATS match {letter_result.ats_keyword_match:.2%}")
            return {
                "status": "success",
                "score": ranking_result.score,
                "cover_letter": letter_result.cover_letter,
                "ats_match": letter_result.ats_keyword_match,
                "context": context
            }
        
        logger.info(f"Job {job.id} scored {ranking_result.score}. Below threshold.")
        return {"status": "filtered", "score": ranking_result.score}
