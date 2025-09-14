# Simple Dockerfile for CI/CD learning
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Copy and make entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port 8000
EXPOSE 8000

# Use entrypoint script to run migrations before starting server
CMD ["./entrypoint.sh"]