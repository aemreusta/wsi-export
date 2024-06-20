# WSI Image Processing Setup

This repository provides the necessary steps to set up a Python environment for processing Whole Slide Images (WSI) using OpenSlide and other required libraries.

## Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html): Make sure you have Conda installed on your system.
- [Docker](https://docs.docker.com/get-docker/): Make sure you have Docker installed on your system.

## Setup Instructions

Follow these steps to set up the environment and install the required dependencies.

### 1. Create and Activate Conda Environment

First, create a new Conda environment named `wsiEnv`:

```bash
conda create --name wsiEnv python
```

Activate the newly created environment:

```bash
conda activate wsiEnv
```

### 2. Install OpenSlide

Install OpenSlide from the conda-forge channel:

```bash
conda install -c conda-forge openslide
```

### 3. Install pip-tools

Install `pip-tools` to manage Python dependencies:

```bash
pip install pip-tools
```

### 4. Compile and Install Dependencies

Use `pip-tools` to compile the `requirements.in` file into a `requirements.txt` file, and then install the dependencies:

```bash
pip-compile requirements.in
pip install -r requirements.txt
```

### Additional Notes

- Ensure that you have a `requirements.in` file in your project directory with all the necessary Python packages listed.
- After compiling the `requirements.in` file, a `requirements.txt` file will be generated. This file contains the exact versions of the packages to be installed.

### Running the Script

Once the environment is set up and dependencies are installed, you can run the processing script:

```bash
python main.py --approximation x16 --source_folder /path/to/source --output_folder /path/to/output
```

Replace `/path/to/source` with the path to your source folder containing SVS images, and `/path/to/output` with the desired output folder path.

## Docker Setup Instructions

To containerize your WSI Image Processing project, follow these steps:

### 1. Create a Dockerfile

Create a `Dockerfile` in your project directory with the following content:

```dockerfile
# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements files to the container
COPY requirements.in /app/requirements.in

# Install pip-tools
RUN pip install pip-tools

# Compile and install dependencies
RUN pip-compile requirements.in
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app

# Install OpenSlide
RUN apt-get update && apt-get install -y openslide-tools

# Set the entry point for the container
ENTRYPOINT ["python", "main.py"]
```

### 2. Build the Docker Image

Build the Docker image with the following command:

```bash
docker build -t wsi-image-processing .
```

### 3. Run the Docker Container

Run the Docker container with the following command, replacing `/path/to/source` and `/path/to/output` with your actual paths:

```bash
docker run -v /path/to/source:/source -v /path/to/output:/output wsi-image-processing --approximation x16 --source_folder /source --output_folder /output
```

- The `-v` flag mounts the specified directories on your host machine to the container.
- Ensure that `/path/to/source` and `/path/to/output` are accessible from your host system.

With these instructions, you can set up the environment for processing WSIs both locally and within a Docker container.