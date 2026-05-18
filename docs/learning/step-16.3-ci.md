# Learning: Step 16.3 - CI Pipeline

## Learning Objectives
- Understand the 2026 industry standard for continuous integration using GitHub Actions.
- Learn the concept of reusable workflows (`workflow_call`).

## Technical Details
- **Reusable Workflows**: Instead of writing the same steps (like setting up Node.js or Python) in every workflow file, a reusable workflow (`ci-reusable.yml`) encapsulates these actions. The main `ci.yml` merely "calls" this reusable workflow using the `uses` keyword. This reduces code duplication, centralizes pipeline logic, and is a major best practice for maintaining large repositories.
- **`setup-uv`**: The pipeline utilizes the modern Python package manager `uv`, which is orders of magnitude faster than traditional `pip` or `poetry`. By leveraging `astral-sh/setup-uv`, the CI run time is drastically minimized.
