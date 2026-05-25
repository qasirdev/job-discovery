# Domain Model Definitions

This document defines the core entity shapes for the Job Discovery platform. These models map to SQLAlchemy models in MVP 2 and beyond.

## UserProfile
Core settings for job discovery relevance and application generation.
- `id`: UUID (Primary Key)
- `target_roles`: Array of strings
- `preferred_stack`: Array of strings
- `seniority_level`: Enum/String
- `target_salary_min`: Integer (pence)
- `target_salary_max`: Integer (pence)
- `preferred_location`: String
- `notice_period`: String
- `updated_at`: DateTime

## CompanyResearch
Intelligence collected on specific companies for interview prep.
- `id`: UUID (Primary Key)
- `company_name_slug`: String (Unique lookup key)
- `research_data`: JSONB
- `updated_at`: DateTime

## Job
The core job listing entity.
- `id`: UUID (Primary Key)
- `title`: String
- `company`: String
- `company_slug`: String
- `location`: String
- `source`: String (e.g. 'linkedin', 'jobserve')
- `url`: String (Unique)
- `description`: Text
- `salary_min`: Integer (pence)
- `salary_max`: Integer (pence)
- `currency`: String (default 'GBP')
- `saved`: Boolean (Computed field populated by left join against SavedJob)
- `scraped_at`: DateTime

## SavedJob
Junction tracking jobs bookmarked by the user.
- `user_id`: UUID
- `job_id`: UUID
- `saved_at`: DateTime

## Recruiter
Contact profiles discovered during scraping or manual entry.
- `id`: UUID (Primary Key)
- `name`: String
- `company`: String
- `email`: String (Optional)
- `linkedin_url`: String (Unique dedup key)
- `interaction_score`: Integer
- `notes`: Text
- `created_at`: DateTime

## Application
Tracks the lifecycle of a job application.
- `id`: UUID (Primary Key)
- `job_id`: UUID
- `user_id`: UUID
- `status`: Enum (draft, applied, awaiting_response, interviewing, offered, rejected, withdrawn)
- `notes`: Text
- `applied_at`: DateTime
- `created_at`: DateTime
- `updated_at`: DateTime

## CV
Candidate's resume, parsed and embedded for RAG.
- `id`: UUID (Primary Key)
- `user_id`: UUID
- `filename`: String
- `embedding_status`: Enum (pending, processing, ready, failed)
- `created_at`: DateTime

## CoverLetter
Generated cover letters bound to a specific job.
- `id`: UUID (Primary Key)
- `job_id`: UUID
- `user_id`: UUID (Mandatory for RLS isolation)
- `content`: Text
- `ats_score`: Integer
- `status`: Enum (draft, final)
- `created_at`: DateTime

## ScrapeRun
Audit log for scraping operations.
- `id`: UUID (Primary Key)
- `source_id`: String
- `jobs_inserted`: Integer
- `errors`: Integer
- `duration_seconds`: Float
- `ran_at`: DateTime
