# Multi-stage production build for AI Business Copilot

# Stage 1: Build React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /build/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend Runtime
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend application source
COPY backend/ ./backend/
COPY sample_data/ ./sample_data/

# Copy built frontend assets from Stage 1 into frontend/dist
COPY --from=frontend-builder /build/frontend/dist ./frontend/dist

# Expose unified port
EXPOSE 8000

ENV PYTHONPATH=/app/backend
ENV ENVIRONMENT=production

# Launch FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--app-dir", "backend", "--host", "0.0.0.0", "--port", "8000"]
