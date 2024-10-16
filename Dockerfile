# Use Python 3.10 (or later) slim image as a base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of your project directory into the container at /app
COPY . /app

# Upgrade pip and install dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to run your script
CMD ["python", "app.py"]
