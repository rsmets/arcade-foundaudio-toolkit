#!/bin/bash

# Test CI workflow locally
# This script simulates what the GitHub Actions workflow does

set -e

echo "🧪 Testing CI workflow locally..."

# Set environment variables
export SUPABASE_ANON_KEY="test-key-for-local-ci"

# Install dependencies
echo "📦 Installing dependencies..."
python -m pip install --upgrade pip
pip install -e .
pip install -e ".[dev]"

# Run linting
echo "🔍 Running linting..."
ruff check foundaudio/ tests/

# Run type checking
echo "🔍 Running type checking..."
mypy foundaudio/

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --cov=foundaudio --cov-report=xml --cov-report=term-missing

# Check package build
echo "📦 Testing package build..."
python -m build

echo "✅ All CI checks passed locally!"
