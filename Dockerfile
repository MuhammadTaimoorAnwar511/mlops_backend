# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# Install dependencies using pip3
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run your application
CMD ["python3", "app.py"]
