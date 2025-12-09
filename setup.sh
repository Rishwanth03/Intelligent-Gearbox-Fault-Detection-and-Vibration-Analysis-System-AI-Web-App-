#!/bin/bash

# Intelligent Gearbox Fault Detection System - Setup Script
# This script sets up the development environment

echo "====================================="
echo "Gearbox Fault Detection System Setup"
echo "====================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1)
echo "Found: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
echo "Virtual environment created."
echo ""

# Activate virtual environment
echo "To activate the virtual environment, run:"
echo "  On Linux/macOS: source venv/bin/activate"
echo "  On Windows: venv\\Scripts\\activate"
echo ""

# Install dependencies
echo "Installing dependencies..."
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        ./venv/Scripts/pip install -r requirements.txt
    else
        ./venv/bin/pip install -r requirements.txt
    fi
else
    pip install -r requirements.txt
fi
echo ""

# Generate sample data
echo "Generating sample data..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ./venv/Scripts/python generate_sample_data.py
else
    ./venv/bin/python generate_sample_data.py
fi
echo ""

# Run tests
echo "Running tests..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ./venv/Scripts/python test_system.py
else
    ./venv/bin/python test_system.py
fi
echo ""

echo "====================================="
echo "Setup Complete!"
echo "====================================="
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment (see above)"
echo "  2. Run: python app.py"
echo "  3. Open browser to: http://localhost:5000"
echo ""
