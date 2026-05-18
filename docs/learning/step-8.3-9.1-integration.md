# Learning Objectives: Database Persistence & Keyset Pagination

In this step, we integrated our in-memory data structures into a fully realized asynchronous Supabase PostgreSQL persistence engine, created interactive client-side fetching loops, and set up modern type-safe schemas.

## 1. SQLAlchemy 2.0 type-safe `Mapped` Fields
Historically, SQLAlchemy columns were declared dynamically via class attributes (e.g. `title = Column(String)`), which Mypy and other static checkers could not type check correctly. 
By utilizing SQLAlchemy 2.0's `Mapped[str] = mapped_column(...)` syntax, we achieve 100% type safety. Attributes are typed natively (like `str` and `datetime`), preventing runtime type issues and ensuring strict compilation compliance.

## 2. Keyset (Cursor-Based) Pagination
For high-frequency database applications, traditional offset-based pagination (`OFFSET 100 LIMIT 20`) is slow because the database must scan and skip the first 100 records. Additionally, it causes record skipping or duplication if items are inserted or deleted while a user is scrolling.

We implemented **Keyset Pagination** (also known as cursor pagination):
1. **Opaque Cursor**: We pack the sort keys `(scraped_at, id)` of the last item on the page and encode it as a base64 string.
2. **Filtering**: When querying the next page, we filter items where `scraped_at < cursor_time OR (scraped_at == cursor_time AND id < cursor_id)`.
3. **Efficiency**: The database can use indices on `scraped_at` and `id` to jump directly to the target record in $O(\log N)$ time, regardless of how deep the user is paging.

## 3. High-Concurrency PostgreSQL `UPSERT`
Scrapers frequently scrape the same job postings multiple times. To avoid filling our tables with duplicates, we use a PostgreSQL `UPSERT` operation via `on_conflict_do_update`:
- Compute a unique, deterministic ID (e.g., a hash of the job URL).
- Attempt to insert the job record.
- If a record with that ID already exists, update its details (title, description, scraped_at) dynamically in a single query.

## 4. Next.js Dev rewrites
When developing frontends that make relative API calls (e.g. `fetch('/api/v1/jobs/')`), local requests default to port 3000 where the Next.js server runs.
Instead of hardcoding absolute ports or facing browser CORS blocks, we add development-only rewrites to `next.config.ts`. In dev mode, Next.js acts as a reverse proxy to forward `/api/` traffic to FastAPI on port 8000, perfectly mirroring Nginx's production behavior.
