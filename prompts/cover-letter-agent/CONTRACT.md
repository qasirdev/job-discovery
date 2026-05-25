# Cover Letter Agent Contract

## Input
- `job_description`: (str) The raw or structured job description.
- `cv_text`: (str) The user's parsed CV text.
- `profile`: (dict) The user's target profile and skills.

## Output Structure
The output MUST strictly contain XML tags for the 6-section playbook:
- `<role_summary>`: Brief summary of the role.
- `<matching_skills>`: Skills matching the job description.
- `<quantified_achievements>`: Relevant quantified achievements from the CV.
- `<ai_narrative>`: Cohesive narrative linking skills to the company's goals.
- `<ats_keywords>`: Comma-separated list of extracted ATS keywords.
- `<recruiter_closing>`: Professional closing statement.
- `<final_cover_letter>`: The complete formatted cover letter ready for the user.

## Constraints
- Max 4000 tokens.
- Professional, concise tone.
- ATS optimized.
