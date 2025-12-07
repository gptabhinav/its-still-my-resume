# LaTeX Resume Modifier

Using LLMs to modify resume sections for getting 80%+ match where possible.

## Overview

This tool allows you to modify LaTeX document sections using natural language prompts powered by Large Language Models (LLMs). It's specifically designed for resume optimization but can work with any LaTeX document.

## Features

- 🔍 **Parse LaTeX documents** - Extract and identify sections automatically
- ✏️ **Modify sections with LLM** - Use natural language to modify specific sections
- ➕ **Generate new sections** - Create new content using AI
- 🎯 **Targeted modifications** - Work on specific sections without affecting others
- 🔌 **Multiple LLM providers** - Support for OpenAI and Anthropic
- 🛠️ **CLI interface** - Easy-to-use command-line tool

## Installation

1. Clone the repository:
```bash
git clone https://github.com/gptabhinav/its-still-my-resume.git
cd its-still-my-resume
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API keys:
```bash
cp .env.example .env
# Edit .env and add your API key
```

## Configuration

Create a `.env` file with your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Choose provider (openai or anthropic)
LLM_PROVIDER=openai

# Choose model
LLM_MODEL=gpt-4
```

## Usage

### List sections in a LaTeX document

```bash
python resume_modifier.py list-sections sample_resume.tex
```

### Show content of a specific section

```bash
python resume_modifier.py show sample_resume.tex "Experience"
```

### Modify a section using LLM

```bash
python resume_modifier.py modify sample_resume.tex "Experience" \
  "Make the bullet points more quantitative and add metrics"
```

With options:
```bash
python resume_modifier.py modify sample_resume.tex "Skills" \
  "Add cloud technologies and DevOps tools" \
  --output modified_resume.tex \
  --provider openai \
  --model gpt-4
```

### Generate a new section

```bash
python resume_modifier.py generate sample_resume.tex "Awards" \
  "Create a section highlighting professional awards and recognitions" \
  --level section \
  --position end
```

### Dry run (preview changes without saving)

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Tailor this for a senior data scientist role" \
  --dry-run
```

## Examples

### Example 1: Tailor Summary for Specific Role

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Tailor this summary for a senior backend engineer position at a fintech company. Emphasize Python, microservices, and financial systems experience."
```

### Example 2: Quantify Achievements

```bash
python resume_modifier.py modify sample_resume.tex "Experience" \
  "Add specific metrics and quantify all achievements. Include percentages, dollar amounts, and team sizes where applicable."
```

### Example 3: Add Technical Details

```bash
python resume_modifier.py modify sample_resume.tex "Projects" \
  "Add more technical details about the architecture, technologies used, and challenges overcome in each project."
```

### Example 4: Generate New Section

```bash
python resume_modifier.py generate sample_resume.tex "Publications" \
  "Create a publications section with 3 sample technical blog posts about Python and microservices"
```

## Python API Usage

You can also use the library programmatically:

```python
from latex_parser import LatexParser
from llm_integration import LatexModifier

# Load your LaTeX document
with open('resume.tex', 'r') as f:
    content = f.read()

# Parse the document
parser = LatexParser(content)

# List all sections
sections = parser.list_sections()
print(f"Found sections: {sections}")

# Get a specific section
section = parser.get_section("Experience")
print(f"Current content: {section.content}")

# Modify using LLM
modifier = LatexModifier()
modified_content = modifier.modify_section(
    section.content,
    "Make it more concise and focused on leadership"
)

# Apply changes
modified_doc = parser.replace_section_content("Experience", modified_content)

# Save modified document
with open('modified_resume.tex', 'w') as f:
    f.write(modified_doc)
```

## Testing

Run the test suite:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_latex_parser.py -v
```

## Project Structure

```
.
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment configuration
├── .gitignore                # Git ignore rules
├── latex_parser.py           # LaTeX document parser
├── llm_integration.py        # LLM provider integrations
├── resume_modifier.py        # CLI interface
├── sample_resume.tex         # Sample LaTeX resume
├── test_latex_parser.py      # Parser tests
└── test_llm_integration.py   # LLM integration tests
```

## How It Works

1. **Parse LaTeX**: The `LatexParser` class extracts sections from your LaTeX document
2. **Identify sections**: Recognizes `\section`, `\subsection`, etc., and their content
3. **LLM Processing**: Sends section content and your prompt to the LLM
4. **Generate modifications**: LLM returns modified content in LaTeX format
5. **Apply changes**: Modified content replaces the original section
6. **Save document**: Updated document is saved to file

## Tips for Best Results

1. **Be specific in prompts**: "Add metrics showing 40% performance improvement" is better than "improve this"
2. **One section at a time**: Modify sections individually for better control
3. **Use dry-run first**: Preview changes before committing them
4. **Preserve structure**: The tool maintains LaTeX formatting, but review output
5. **Iterate**: Make incremental changes and review after each modification

## Supported LLM Providers

### OpenAI
- GPT-4 (recommended)
- GPT-3.5-turbo
- Other chat models

### Anthropic
- Claude 3 Sonnet
- Claude 3 Opus
- Other Claude models

## Limitations

- Assumes standard LaTeX section commands (`\section`, `\subsection`, etc.)
- Complex nested structures may need manual review
- LLM output quality depends on the model and prompt
- Requires valid API keys for LLM providers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this tool for your resume optimization needs.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
