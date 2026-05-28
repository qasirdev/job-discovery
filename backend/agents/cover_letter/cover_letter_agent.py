import json
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from litellm import acompletion
from pydantic import BaseModel
from jinja2 import Template
from ...llm.client import generate_structured_response
from ...models import Job, UserProfile, CV, CoverLetter, CoverLetterStatus
from ...logging_config import get_logger

logger = get_logger(__name__)

class CoverLetterOutput(BaseModel):
    role_summary: str
    matching_skills: list[str]
    quantified_achievements: list[str]
    ai_narrative: str
    ats_keywords: list[str]
    recruiter_closing: str
    final_cover_letter: str

from pathlib import Path
import time
from ...schemas import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ..base import BaseAgent

class CoverLetterAgent(BaseAgent):
    agent_id = "cover_letter"
    canonical_role = "doer"
    display_name = "Cover Letter Agent"

    def __init__(self, db: AsyncSession, job_structured: dict = None):
        self.db = db
        job_structured = job_structured or {}
        template_name = job_structured.get("job_type", "technical-specialist")
        # JD-316: Ensure fallback if the job_type is null or invalid
        if not template_name:
            template_name = "technical-specialist"
            
        template_path = Path(__file__).parent.parent.parent.parent / "prompts" / "cover_letter" / "templates" / f"{template_name}.md"
        
        if not template_path.exists():
            logger.warning(f"Template {template_name} not found. Falling back to technical-specialist.")
            template_path = Path(__file__).parent.parent.parent.parent / "prompts" / "cover_letter" / "templates" / "technical-specialist.md"
        
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "cover_letter" / "system.md"
        self.user_prompt_path = template_path
        
    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Cover letter prompt {path} not found.")
            return ""

    async def _extract_ats_keywords(self, job_description: str) -> list[str]:
        """Extract ATS keywords from job description using LLM."""
        prompt = f"""Extract a concise list of the most critical technical skills, tools, and methodologies from this job description.
Return ONLY a valid JSON array of strings. Do not include any other text.
Job Description:
{job_description}"""

        response = await acompletion(
            model="claude-3-5-sonnet-20240620",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        try:
            keywords = json.loads(content)
            if isinstance(keywords, list):
                return [k.lower() for k in keywords]
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse ATS keywords JSON: {content}")
            
        return []

    def _calculate_ats_match(self, text: str, keywords: list[str]) -> float:
        if not keywords:
            return 100.0
            
        text_lower = text.lower()
        matched = sum(1 for kw in keywords if kw in text_lower)
        return (matched / len(keywords)) * 100

    async def generate(self, job_id: UUID, user_id: UUID, critic_feedback: str | None = None, learner_context: str | None = None) -> AgentResultEnvelope:
        logger.info(f"Starting Cover Letter generation for job {job_id}")
        
        # 1. Fetch Context
        job = (await self.db.execute(select(Job).where(Job.id == job_id))).scalar_one_or_none()
        profile = (await self.db.execute(select(UserProfile).where(UserProfile.id == user_id))).scalar_one_or_none()
        cv = (await self.db.execute(select(CV).where(CV.user_id == user_id))).scalar_one_or_none()
        
        if not job or not profile:
            raise ValueError("Job or Profile not found")
            
        cv_text = cv.text_content if cv else "No CV provided."
        
        # 2. Setup existing or new Cover Letter record
        cl = (await self.db.execute(select(CoverLetter).where(CoverLetter.job_id == job_id))).scalar_one_or_none()
        if not cl:
            cl = CoverLetter(job_id=job_id, status=CoverLetterStatus.generating)
            self.db.add(cl)
            await self.db.commit()
        else:
            cl.status = CoverLetterStatus.generating
            await self.db.commit()

        try:
            start_time = time.time()
            # 3. Extract ATS Keywords
            keywords = await self._extract_ats_keywords(job.description)
            logger.info(f"Extracted {len(keywords)} ATS keywords")

            system_prompt = self._load_prompt(self.system_prompt_path) or "You are an expert AI Career Coach. Generate a cover letter."
            user_template_str = self._load_prompt(self.user_prompt_path)
            
            if user_template_str:
                try:
                    template = Template(user_template_str)
                    base_user_prompt = template.render(
                        job_title=job.title,
                        job_company=job.company,
                        job_description=job.description,
                        candidate_cv=cv_text,
                        target_role=profile.target_role
                    )
                except Exception as e:
                    logger.error(f"Prompt rendering error: {e}")
                    base_user_prompt = f"Job Description:\n{job.description}\n\nCandidate CV:\n{cv_text}\n\nCandidate Target Role: {profile.target_role}"
            else:
                base_user_prompt = f"Job Description:\n{job.description}\n\nCandidate CV:\n{cv_text}\n\nCandidate Target Role: {profile.target_role}"

            if learner_context:
                base_user_prompt += f"\n\n--- Learner RAG Context ---\n{learner_context}\n---------------------------"

            max_retries = 2
            best_letter = ""
            best_score = 0.0

            for attempt in range(max_retries + 1):
                user_prompt = base_user_prompt
                if attempt > 0:
                    user_prompt += f"\n\nCRITICAL: Ensure these EXACT keywords are naturally integrated into the text: {', '.join(keywords)}"
                if critic_feedback:
                    user_prompt += f"\n\nCRITIC FEEDBACK (Must address in this revision):\n{critic_feedback}"
                    
                response = await generate_structured_response(
                    prompt=user_prompt,
                    system_instruction=system_prompt,
                    response_model=CoverLetterOutput,
                    agent_id="cover_letter"
                )
                
                final_letter = response.final_cover_letter
                    
                score = self._calculate_ats_match(final_letter, keywords)
                logger.info(f"Attempt {attempt+1} ATS Score: {score}%")
                
                if score >= best_score:
                    best_score = score
                    best_letter = final_letter
                    
                if score >= 60.0:
                    break

            # 4. Finalize
            cl.content = best_letter
            cl.ats_score = int(best_score)
            cl.status = CoverLetterStatus.ready if best_score >= 60.0 else CoverLetterStatus.failed
            
            await self.db.commit()
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="cover_letter",
                canonical_role="doer",
                status="success" if cl.status == CoverLetterStatus.ready else "failure",
                result={"cover_letter_id": str(cl.id), "content": cl.content, "ats_score": cl.ats_score},
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="claude-3-5-sonnet-20240620",
                    prompt_version=None
                )
            )

        except Exception as e:
            logger.error(f"Cover Letter generation failed: {e}")
            cl.status = CoverLetterStatus.failed
            await self.db.commit()
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="cover_letter",
                canonical_role="doer",
                status="failure",
                result={"cover_letter_id": str(cl.id), "content": "", "ats_score": 0},
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="unknown",
                    prompt_version=None
                ),
                escalation=AgentEscalation(reason=str(e), target_agent="orchestrator")
            )
