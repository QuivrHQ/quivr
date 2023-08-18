# Use the same base image as the 'backend-core' container
FROM python:3.11-bullseye

# Install necessary packages
RUN apt-get update && apt-get install -y liblzma-dev cmake git

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt --timeout 100

# Copy your application's code to the Docker container
COPY . /app

# Start the Uvicorn server on port 5051
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5051"]
