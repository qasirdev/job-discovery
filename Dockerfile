# ─── Stage 1: Build Next.js static export ───────────────────────────────────
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install

COPY frontend/ .
RUN npm run build
# Produces /app/frontend/out — fully static HTML/JS/CSS


# ─── Stage 2: Backend runtime + Nginx + static frontend ─────────────────────
FROM python:3.14-slim AS runtime

# System packages: nginx + supervisor (process manager)
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Backend dependencies via uv
WORKDIR /app/backend
COPY backend/pyproject.toml backend/README.md ./
RUN uv sync --no-dev

# Backend source
COPY backend/ .

# Install Playwright Chromium (required for scraper agents)
RUN uv run playwright install chromium --with-deps

# Copy built frontend into nginx web root
COPY --from=frontend-builder /app/frontend/out /var/www/html

# Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
