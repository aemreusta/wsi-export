# WSI Image Processing Setup

This repository provides the necessary steps to set up a Python environment for processing Whole Slide Images (WSI) using OpenSlide and other required libraries.

## Prerequisites

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html): Make sure you have Conda installed on your system.

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