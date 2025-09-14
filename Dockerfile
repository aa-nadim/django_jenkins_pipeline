# Fast Dockerfile - Optimized for CI/CD speed
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Install only essential system packages (cached layer)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

# Copy and install requirements first (cached layer if unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (this layer changes most often)
COPY . .

# Run migrations and setup in one layer
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    mkdir -p staticfiles

EXPOSE 8000

# Simple health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=2 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Direct command (no entrypoint script needed)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]