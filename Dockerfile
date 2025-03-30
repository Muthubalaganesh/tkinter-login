# Use an official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . /app

# Install system dependencies required by Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "your_script.py"]  # Replace with your script
