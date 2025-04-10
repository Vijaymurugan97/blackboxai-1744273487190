#!/bin/bash

echo "Building PDF Processor Windows Installer..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.7 or higher and try again"
    exit 1
fi

# Check and create data directory structure if it doesn't exist
if [ ! -d "data" ]; then
    mkdir -p data
fi

if [ ! -d "data/input" ]; then
    mkdir -p data/input
fi

# Install required dependencies
echo "Installing required dependencies..."
pip install -r requirements.txt

# Build the package
echo "Building executable with cx_Freeze..."
python3 setup.py build

# Create the Windows installer
echo "Creating Windows installer..."
python3 setup.py bdist_msi

echo
echo "Build complete! The installer can be found in the 'dist' folder."
echo
