# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install system dependencies for h5py and pkg-config
RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the local requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the app will run on
EXPOSE 8080

# Run the MLflow server with the new Python script
CMD ["python", "run_mlflow.py"]
