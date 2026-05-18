# SKILLS — LinkedIn Agent

This file describes the domain-specific skills and heuristic abilities available to the LinkedIn Agent.

## 1. DOM Pattern Matching
- Identify standard LinkedIn CSS selectors for job panels and description bodies.
- Handle fallback selectors when standard LinkedIn layouts change dynamically.

## 2. Text Normalization
- Strip non-printable unicode control characters and emoji strings.
- Standardize spacing, line endings, and indentation.

## 3. Preliminary Filtering
- Perform case-insensitive substring checks for exclusion keywords (e.g. "intern", "junior" when searching for senior roles, or "on-site only").
- Flag relevant stack terms (e.g. "python", "fastapi", "react", "next.js").
