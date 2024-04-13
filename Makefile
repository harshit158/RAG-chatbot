# Makefile

# Define variables
VENV_NAME = venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

# Default target
all: install

# Set up the virtual environment
venv:
    python -m venv $(VENV_NAME)

# Install project dependencies
install: venv
    $(PIP) install -r requirements.txt

# Run tests
test: venv
    $(PYTHON) -m pytest tests/

# Clean up
clean:
    rm -rf $(VENV_NAME)

.PHONY: venv install test clean