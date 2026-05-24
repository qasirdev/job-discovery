import os
import re
from typing import Dict, Any
from pydantic import BaseModel
from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from ...schemas import Job

logger = get_logger(__name__)


class CoverLetterResult(BaseModel):
    cover_letter: str
    ats_keyword_match: float
    word_count: int


class CoverLetterAgent:
    """Generates ATS-optimized cover letters with keyword matching and retry logic."""

    def __init__(self) -> None:
        self.system_prompt_path = os.path.join("prompts", "cover-letter-agent", "system.md")
        self.ats_threshold = 0.60  # 60% keyword match required
        self.max_retries = 2
        self.min_words = 300
        self.max_words = 500

    def _load_prompt(self) -> str:
        """Load the system instruction prompt from disk."""
        try:
            with open(self.system_prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("Cover letter system prompt not found, using fallback.")
            return "You are a cover letter agent. Generate a professional cover letter."

    def _extract_keywords(self, text: str) -> set[str]:
        """Extract technical keywords from job description."""
        # Common tech keywords pattern
        tech_keywords = set()
        
        # Extract words that are likely technical terms (capitalized, camelCase, etc.)
        patterns = [
            r'\b[A-Z][a-zA-Z]+\b',  # Capitalized words
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\w+\.\w+\b',  # Dot notation (e.g., React.js)
            r'\b\w+-\w+\b',  # Hyphenated terms
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            tech_keywords.update(matches)
        
        # Also extract common programming languages and frameworks
        common_tech = {
            'python', 'javascript', 'typescript', 'java', 'go', 'rust', 'c++',
            'react', 'vue', 'angular', 'fastapi', 'django', 'flask', 'express',
            'postgresql', 'mongodb', 'redis', 'sql', 'nosql', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'git', 'ci/cd', 'agile', 'scrum'
        }
        
        text_lower = text.lower()
        for tech in common_tech:
            if tech in text_lower:
                tech_keywords.add(tech)
        
        return tech_keywords

    def _calculate_ats_match(self, job_keywords: set[str], cover_letter: str) -> float:
        """Calculate ATS keyword match percentage."""
        cover_letter_lower = cover_letter.lower()
        matched = sum(1 for kw in job_keywords if kw.lower() in cover_letter_lower)
        
        if not job_keywords:
            return 0.0
        
        return matched / len(job_keywords)

    def _validate_word_count(self, cover_letter: str) -> bool:
        """Validate cover letter word count is within acceptable range."""
        word_count = len(cover_letter.split())
        return self.min_words <= word_count <= self.max_words

    async def generate_cover_letter(self, job: Job, context: str, candidate_profile: Dict[str, Any] | None = None) -> CoverLetterResult:
        """
        Draft a custom cover letter leveraging the RAG context with ATS optimization.
        
        Args:
            job: The job object
            context: RAG-retrieved context about candidate
            candidate_profile: Optional candidate profile data
        
        Returns:
            CoverLetterResult with letter, ATS match score, and word count
        """
        logger.info(f"Generating cover letter for job: {job.id}")
        
        system_instruction = self._load_prompt()
        job_keywords = self._extract_keywords(job.description)
        
        # Build prompt with job details and context
        prompt = f"""Job Title: {job.title}
Company: {job.company}
Job Description: {job.description}

Candidate Context:
{context if context else "No specific context available."}
"""
        
        # Retry loop for ATS keyword matching
        for attempt in range(self.max_retries + 1):
            try:
                # Add keyword injection instruction if retrying
                if attempt > 0:
                    prompt += f"\n\nIMPORTANT: Ensure the cover letter includes these keywords: {', '.join(job_keywords)}"
                
                # Generate cover letter using LLM
                response = await generate_structured_response(
                    prompt=prompt,
                    system_instruction=system_instruction,
                    response_model=CoverLetterResult
                )
                
                # Calculate ATS match
                ats_match = self._calculate_ats_match(job_keywords, response.cover_letter)
                
                # Validate word count
                word_count_valid = self._validate_word_count(response.cover_letter)
                
                logger.info(f"Cover letter attempt {attempt + 1}: ATS match={ats_match:.2%}, word_count={response.word_count}, valid={word_count_valid}")
                
                # Check if ATS threshold met
                if ats_match >= self.ats_threshold and word_count_valid:
                    logger.info(f"Cover letter generated successfully with ATS match {ats_match:.2%}")
                    return CoverLetterResult(
                        cover_letter=response.cover_letter,
                        ats_keyword_match=ats_match,
                        word_count=response.word_count
                    )
                
                # If below threshold and we have retries left, continue
                if attempt < self.max_retries:
                    logger.warning(f"ATS match {ats_match:.2%} below threshold {self.ats_threshold:.2%}, retrying...")
                    continue
                else:
                    logger.warning(f"Max retries reached, returning best attempt with ATS match {ats_match:.2%}")
                    return CoverLetterResult(
                        cover_letter=response.cover_letter,
                        ats_keyword_match=ats_match,
                        word_count=response.word_count
                    )
                    
            except Exception as e:
                logger.error(f"Cover letter generation failed on attempt {attempt + 1}: {e}")
                if attempt == self.max_retries:
                    # Return fallback on final failure
                    fallback = self._generate_fallback_letter(job, context)
                    return CoverLetterResult(
                        cover_letter=fallback,
                        ats_keyword_match=0.0,
                        word_count=len(fallback.split())
                    )
        
        # Should not reach here, but fallback just in case
        fallback = self._generate_fallback_letter(job, context)
        return CoverLetterResult(
            cover_letter=fallback,
            ats_keyword_match=0.0,
            word_count=len(fallback.split())
        )

    def _generate_fallback_letter(self, job: Job, context: str) -> str:
        """Generate a simple fallback cover letter when LLM fails."""
        return f"""Dear Hiring Manager,

I am writing to express my interest in the {job.title} position at {job.company}. With my background and experience, I believe I would be a valuable addition to your team.

{context[:200] if context else "I am excited about the opportunity to contribute to your organization's success."}

Thank you for your time and consideration.

Sincerely,
Candidate"""
