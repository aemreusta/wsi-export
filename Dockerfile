# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY main.py .
COPY requirements.in .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir pip-tools

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    openslide-tools \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Compile and install Python dependencies
RUN pip-compile requirements.in && pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Use entrypoint to ensure script arguments are passed correctly
ENTRYPOINT ["python", "main.py"]