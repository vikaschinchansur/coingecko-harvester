# Use Python 3.13 slim image for smaller size
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and modules
COPY main.py .
COPY api/ ./api/
COPY config/ ./config/
COPY db/ ./db/
COPY streaming/ ./streaming/

# Run the application
CMD ["python", "main.py"]