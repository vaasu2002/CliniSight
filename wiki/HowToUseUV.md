# Using `uv`: A Quick Guide

This guide provides a basic overview of how to use `uv`, a fast Python package installer and resolver. The commands are based on the video tutorial ["The Python Packaging Ecosystem is a Mess and `uv` is the Answer"](https://www.youtube.com/watch?v=ASRCJK2aWk0).

---

## Installation

Before you can use `uv`, you need to install it on your system using pip.

```bash
pip install uv
```

---

## Getting Started

Once `uv` is installed, follow these steps to get your Python project set up.

### 1. Initialize `uv`

First, you need to initialize `uv` in your project's root directory. This command sets up the necessary configuration for `uv` to manage your project.

```bash
uv init
```

### 2. Create a Virtual Environment

It's best practice to isolate your project's dependencies. Create a virtual environment to manage them effectively.

```bash
uv venv
```

This will create a `.venv` directory in your project, which you should add to your `.gitignore` file.

### 3. Install Packages

You can install packages directly from a `requirements.txt` file. This is useful for installing multiple packages at once and ensuring consistent dependencies across different environments.

```bash
uv add -r requirements.txt
```

This command reads your `requirements.txt` file and installs all the specified libraries into your active virtual environment.