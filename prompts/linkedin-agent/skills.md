# SKILLS — LinkedIn Agent

This file describes the domain-specific skills and heuristic abilities available to the LinkedIn Agent.

## 1. DOM Pattern Matching
- Identify standard LinkedIn CSS selectors for job panels and description bodies.
- Handle fallback selectors when standard LinkedIn layouts change dynamically. Known fallback selectors to try:
  - Primary title: `.job-details-jobs-unified-top-card__job-title`, `.topcard__title`, `h1.t-24`
  - Primary company: `.job-details-jobs-unified-top-card__company-name`, `.topcard__org-name-link`
  - Primary location: `.job-details-jobs-unified-top-card__bullet`, `.topcard__flavor--bullet`
  - Primary description body: `.jobs-description__container`, `.show-more-less-html__markup`, `div.core-section-container__content`

## 2. Text Normalization
- Strip non-printable unicode control characters and emoji strings.
- Standardize spacing, line endings, and indentation.

## 3. Preliminary Filtering
- Perform case-insensitive substring checks for exclusion keywords (e.g. "intern", "junior" when searching for senior roles, or "on-site only").
- Flag relevant stack terms (e.g. "python", "fastapi", "react", "next.js").
