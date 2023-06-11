#!/bin/bash

set -e

# Create the build/static folder if it doesn't exist
echo "Creating build/static folder if it doesn't exist..."
mkdir -p build/static

# Continue with the rest of the build script
echo "Creating virtual environment..."
python -m venv .venv
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running collectstatic..."
# python manage.py collectstatic --no-input -v 3 # This provides a more verbose version
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"