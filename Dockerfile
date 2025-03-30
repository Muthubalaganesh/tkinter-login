# Use an official Python runtime as base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the current project files to the container
COPY . .

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Tkinter application
CMD ["python", "main.py"]
