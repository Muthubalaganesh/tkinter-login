# Use an official Python runtime as base image
FROM python:3.11  

# Set the working directory in the container
WORKDIR /app  

# Copy the current directory contents into the container at /app
COPY . /app  

# Upgrade pip
RUN pip install --upgrade pip  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt  

# Command to run the application (modify if needed)
CMD ["python", "your_script.py"]  # Replace 'your_script.py' with your actual file
