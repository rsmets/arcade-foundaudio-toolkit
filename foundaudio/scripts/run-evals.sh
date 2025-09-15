#!/bin/bash

# Found Audio Toolkit - Evaluation Runner Script
# This script runs the comprehensive evaluation suite for the foundaudio toolkit

set -e # Exit on any error

echo "🎵 Found Audio Toolkit - Running Evaluations"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
	echo "❌ Error: Please run this script from the foundaudio directory"
	echo "   cd foundaudio && ./scripts/run-evals.sh"
	exit 1
fi

# Check if arcade-ai[evals] is installed
echo "🔍 Checking evaluation dependencies..."
if ! python -c "import arcade_evals" 2>/dev/null; then
	echo "📦 Installing evaluation dependencies..."
	uv pip install 'arcade-ai[evals]'
else
	echo "✅ Evaluation dependencies already installed"
fi

# Navigate to evals directory
echo "📁 Navigating to evals directory..."
cd evals

# Run the evaluations
echo "🚀 Running evaluation suites..."
echo "   This will test 30+ scenarios across two evaluation files:"
echo "   - eval_foundaudio.py: Audio search tool (20+ scenarios)"
echo "     * Basic audio search functionality"
echo "     * Search and genre filtering"
echo "     * Parameter validation"
echo "     * Edge cases and error handling"
echo "     * Conversation context"
echo "   - eval_hello.py: Hello tool (10+ scenarios)"
echo "     * Simple and contextual greetings"
echo "     * Name extraction and edge cases"
echo "     * Multi-turn conversation flow"
echo ""

arcade evals .

echo ""
echo "✅ Evaluation complete!"
echo "   Check the output above for detailed results and scores."
