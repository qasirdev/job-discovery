<filtering_rules>
- If the `score` after reranking falls below 40, set `is_filtered` to true.
- If the role requires physical relocation but the user profile states "Remote Only", set `is_filtered` to true regardless of score.
- If `is_filtered` is true, the job will not be shown to the user.
</filtering_rules>
