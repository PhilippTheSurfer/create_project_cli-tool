#!/bin/bash

# Install script for the 'project' CLI tool (system-wide installation)

# Exit immediately if a command exits with a non-zero status
set -e

echo "-------------------------------------------"
echo "Installing 'project' CLI tool system-wide..."
echo "-------------------------------------------"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ 'python3' could not be found. Please install Python 3 and try again."
    exit 1
fi

# Optionally, check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version $PYTHON_VERSION found."

# Upgrade pip and setuptools system-wide (with --break-system-packages)
echo "Upgrading pip and setuptools system-wide..."
sudo python3 -m pip install --upgrade pip setuptools --break-system-packages

# Install the package system-wide (with --break-system-packages)
echo "Running 'pip install .' to install the package system-wide..."
sudo python3 -m pip install . --break-system-packages

echo "-------------------------------------------"
echo "'project' CLI tool has been installed successfully system-wide."
echo "-------------------------------------------"

# Verify installation
if command -v project &> /dev/null
then
    echo "✅ 'project' command is now available."
else
    echo "⚠️  Installation completed, but 'project' command not found in PATH."
    echo "You might need to add Python scripts directory to your PATH."
    echo "Alternatively, ensure you're using the correct Python environment."
fi

