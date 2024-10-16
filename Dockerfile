# Use Python 3.10 slim image as a base for builder stage
FROM python:3.10-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Install any necessary build dependencies
RUN apt-get update && apt-get install -y gcc g++ libgcc1

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install Python dependencies into a local folder
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt -t /app/dependencies

# Create a lightweight production image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y libgcc1 libstdc++6 && rm -rf /var/lib/apt/lists/*

# Copy the dependencies from the builder stage
COPY --from=builder /app/dependencies /app/dependencies

# Copy the contents of the project into the container
COPY . /app

# Set the environment variable to include dependencies in PYTHONPATH
ENV PYTHONPATH /app/dependencies

# Create the necessary directory for static files
RUN mkdir -p /app/tmp/static

# Set permissions for the non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app/tmp

# Create a non-root user to run the container
USER appuser

# Set the entry point for the container
CMD ["python", "-c", "print('Visit your API at http://localhost:8000'); import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=8000)"]
