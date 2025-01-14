# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=api.py \
    FLASK_ENV=production \
    HOST=0.0.0.0 \
    PORT=5001

# Set working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove gcc

# Copy the application code
COPY . .

# Make port 5001 available
EXPOSE 5001

# Run the application with gunicorn
RUN pip install gunicorn

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "api:app"]
