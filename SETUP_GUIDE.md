# imaginAIry - New Machine Setup Guide

This guide provides step-by-step instructions on how to set up and run the **imaginAIry** project on a completely new machine, with full GPU acceleration for fast image generation.

## 1. Prerequisites

Before moving the project, make sure the new machine has the following installed:
- **Python 3.12** (Highly Recommended): Do NOT use Python 3.13 or 3.14. PyTorch currently only provides pre-built CUDA (GPU) packages for Python 3.12 and below. 
- **Git** (Optional, if you plan to clone instead of copying files)
- **NVIDIA GPU** (Recommended): For fast image generation (seconds instead of minutes).

---

## 2. Copy the Project

Move the entire `imaginAIry-master` project folder to the new machine. You can do this via a USB drive, cloud storage, or by cloning your Git repository.

---

## 3. Environment Setup

Open a terminal (or Command Prompt / PowerShell) in the project root directory (`imaginAIry-master`) and run the following commands:

### Step 3.1: Create a Virtual Environment
It's best practice to use a virtual environment to avoid dependency conflicts.
```bash
# Create a virtual environment named "venv"
python -m venv venv
```

### Step 3.2: Activate the Virtual Environment
**On Windows:**
```bash
venv\Scripts\activate
```
**On Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 3.3: Install Project Dependencies
Since this project uses a `setup.py` file, you can install all required packages by running:
```bash
pip install -e .
```

### Step 3.4: Install GPU-Accelerated PyTorch (Crucial)
To ensure the project uses your NVIDIA GPU instead of the slow CPU, you must install the CUDA version of PyTorch:
```bash
pip uninstall torch torchvision -y
pip install --upgrade --index-url https://download.pytorch.org/whl/cu121 torch torchvision
```

---

## 4. Running the Project

Once everything is installed, you can start the application server.

Make sure your virtual environment is activated, then run:
```bash
python -m imaginairy.cli.main server
```
*(Alternatively, you can just run `aimg server`)*

### Access the UI
Once the server says `Uvicorn running on http://0.0.0.0:8000`, open your web browser and go to:
**[http://localhost:8000/](http://localhost:8000/)**

> [!TIP]
> **First Run Note:** The very first time you generate an image, the backend will download the necessary AI model weights (like Stable Diffusion 1.5). This might take a few minutes depending on your internet connection. Subsequent generations will take just a few seconds.
