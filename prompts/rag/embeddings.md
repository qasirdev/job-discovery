<embeddings_rules>
- Expect 1536-dimensional embeddings from `text-embedding-3-small`.
- Apply a cosine similarity threshold of `0.75`. Discard any document below this threshold.
- For chunked documents (like a CV), aggregate chunks using max pooling before applying the similarity threshold.
</embeddings_rules>
