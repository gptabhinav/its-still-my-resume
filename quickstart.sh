#!/bin/bash
# Quickstart script for LaTeX Resume Modifier

set -e

echo "======================================"
echo "LaTeX Resume Modifier - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✓ pip found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "📝 Please edit .env and add your API key:"
    echo "   OPENAI_API_KEY=your_key_here"
    echo ""
    echo "   Then run this script again or proceed with the demo using mock provider."
    echo ""
fi

# Run tests
echo "Running tests..."
pytest -q
echo "✓ All tests passed"
echo ""

# Run example
echo "Running example usage (no API key required)..."
echo ""
python example_usage.py
echo ""

# Show help
echo "======================================"
echo "Quick Commands:"
echo "======================================"
echo ""
echo "List sections:"
echo "  python resume_modifier.py list-sections sample_resume.tex"
echo ""
echo "Show a section:"
echo "  python resume_modifier.py show sample_resume.tex 'Summary'"
echo ""
echo "Modify a section (requires API key):"
echo "  python resume_modifier.py modify sample_resume.tex 'Summary' 'Make it more concise'"
echo ""
echo "See USAGE_GUIDE.md for more examples!"
echo ""
echo "======================================"
echo "✓ Quickstart Complete!"
echo "======================================"
