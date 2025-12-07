# LaTeX Resume Modifier - Usage Guide

This guide provides detailed examples of how to use the LaTeX Resume Modifier to optimize your resume using LLM prompts.

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/gptabhinav/its-still-my-resume.git
cd its-still-my-resume

# Install dependencies
pip install -r requirements.txt

# Set up API key
cp .env.example .env
# Edit .env and add your OpenAI or Anthropic API key
```

### 2. Explore Your Resume

First, see what sections are in your LaTeX resume:

```bash
python resume_modifier.py list-sections sample_resume.tex
```

Output:
```
Found 11 sections:

  [section] Summary
  [section] Experience
  [subsection] Senior Software Engineer | Tech Company Inc.
  [subsection] Software Engineer | Startup Solutions
  [section] Education
  [subsection] Bachelor of Science in Computer Science
  [section] Skills
  [section] Projects
  [subsection] E-Commerce Platform
  [subsection] Data Analytics Dashboard
  [section] Certifications
```

### 3. View Section Content

Look at a specific section:

```bash
python resume_modifier.py show sample_resume.tex "Summary"
```

## Common Use Cases

### Tailoring Resume for Specific Job Roles

#### Backend Engineer Role

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Rewrite this summary to emphasize backend engineering skills, focusing on API development, database design, and system architecture. Mention Python, Node.js, and microservices experience."
```

#### Data Science Role

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Rewrite this to highlight data science and machine learning experience. Emphasize Python, statistical analysis, ML frameworks, and data visualization. Target a senior data scientist position."
```

#### DevOps Engineer Role

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Tailor this for a DevOps engineer role. Highlight CI/CD, container orchestration, infrastructure as code, and cloud platforms. Emphasize automation and reliability."
```

### Quantifying Achievements

Make your experience more impactful with metrics:

```bash
python resume_modifier.py modify sample_resume.tex "Experience" \
  "Add specific quantifiable metrics to all bullet points. Include percentages, dollar amounts, user numbers, and time savings. Make achievements more concrete and impressive."
```

### Adding Technical Details

Enhance your project descriptions:

```bash
python resume_modifier.py modify sample_resume.tex "Projects" \
  "Add more technical details to each project. Include specific technologies, architectural patterns, challenges overcome, and measurable outcomes. Make it more technical and detailed."
```

### Optimizing for ATS (Applicant Tracking Systems)

```bash
python resume_modifier.py modify sample_resume.tex "Skills" \
  "Add these keywords for better ATS compatibility: AWS Lambda, Terraform, GitLab CI, Redis, Elasticsearch, gRPC. Organize by category."
```

### Creating New Sections

#### Add Publications Section

```bash
python resume_modifier.py generate sample_resume.tex "Publications" \
  "Create a publications section with 3 technical blog posts about cloud architecture, microservices best practices, and Python performance optimization. Include realistic titles and publication venues." \
  --level section --position end
```

#### Add Awards Section

```bash
python resume_modifier.py generate sample_resume.tex "Awards and Recognition" \
  "Generate an awards section highlighting: Employee of the Year 2022, Best Innovation Award for microservices architecture, Top Contributor Award for open source contributions." \
  --level section --position end
```

## Advanced Features

### Dry Run Mode

Preview changes before applying them:

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Make it more concise, under 100 words" \
  --dry-run
```

### Save to Different File

Keep original and create modified version:

```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Emphasize leadership and team management" \
  --output resume_leadership.tex
```

### Choose LLM Provider

Use specific LLM provider and model:

```bash
# Use OpenAI GPT-4
python resume_modifier.py modify sample_resume.tex "Experience" \
  "Add more technical depth" \
  --provider openai --model gpt-4

# Use Anthropic Claude
python resume_modifier.py modify sample_resume.tex "Skills" \
  "Reorganize by proficiency level" \
  --provider anthropic --model claude-3-sonnet-20240229
```

## Job-Specific Optimization Workflow

### Example: Applying to Senior Software Engineer at Fintech Company

**Job Requirements:**
- 5+ years Python experience
- Microservices architecture
- Financial systems knowledge
- Team leadership
- AWS/Cloud expertise

**Optimization Steps:**

1. **Tailor Summary**
```bash
python resume_modifier.py modify sample_resume.tex "Summary" \
  "Rewrite emphasizing: 7+ years Python experience, microservices expertise, financial systems development, team leadership of 5+ engineers, AWS cloud architecture. Target senior engineer at fintech company."
```

2. **Enhance Experience Section**
```bash
python resume_modifier.py modify sample_resume.tex "Experience" \
  "Add financial/payment system context. Emphasize Python microservices, AWS services used, team size led, and quantifiable business impact. Include compliance and security mentions."
```

3. **Update Skills**
```bash
python resume_modifier.py modify sample_resume.tex "Skills" \
  "Prioritize: Python (advanced), Microservices, AWS (Lambda, ECS, RDS), PostgreSQL, REST APIs, Docker, Kubernetes. Add financial domain keywords: payment processing, compliance, fraud detection."
```

4. **Add Relevant Projects**
```bash
python resume_modifier.py modify sample_resume.tex "Projects" \
  "Add or enhance a project about payment processing system or financial data pipeline. Include Python, AWS, real-time processing, and security considerations."
```

5. **Review Everything**
```bash
python resume_modifier.py show sample_resume.tex "Summary"
python resume_modifier.py show sample_resume.tex "Experience"
python resume_modifier.py show sample_resume.tex "Skills"
```

## Python API Usage

For automation or custom workflows, use the Python API directly:

```python
from latex_parser import LatexParser
from llm_integration import LatexModifier

# Load resume
with open('resume.tex', 'r') as f:
    content = f.read()

# Parse sections
parser = LatexParser(content)
print(f"Found {len(parser.sections)} sections")

# Initialize modifier
modifier = LatexModifier()

# Modify multiple sections
sections_to_modify = {
    "Summary": "Make more concise and impactful",
    "Experience": "Add quantifiable metrics",
    "Skills": "Prioritize cloud technologies"
}

for section_name, prompt in sections_to_modify.items():
    section = parser.get_section(section_name)
    if section:
        modified = modifier.modify_section(section.content, prompt)
        content = parser.replace_section_content(section_name, modified)
        parser = LatexParser(content)  # Re-parse for next iteration

# Save modified resume
with open('resume_modified.tex', 'w') as f:
    f.write(content)
```

## Tips for Effective Prompts

1. **Be Specific**: "Add metrics showing 40% improvement" > "make it better"
2. **Provide Context**: Mention the target role, company type, or industry
3. **Set Constraints**: Specify length, tone, or specific keywords to include
4. **Iterate**: Make small changes and review, rather than big rewrites
5. **Use Dry Run**: Preview changes before committing

## Best Practices

1. **Keep Backups**: Always backup your original resume before modifications
2. **Review Output**: LLMs can make mistakes - always review generated content
3. **Iterative Approach**: Make one section at a time for better control
4. **Version Control**: Use git or similar to track changes
5. **Test Compilation**: Compile LaTeX after modifications to ensure syntax is valid

## Troubleshooting

### Issue: API Key Not Found

**Solution**: Ensure `.env` file exists with valid API key:
```bash
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai
```

### Issue: Section Not Found

**Solution**: List all sections first to see exact names:
```bash
python resume_modifier.py list-sections your_resume.tex
```

Section names are case-insensitive but must match exactly.

### Issue: LaTeX Compilation Errors

**Solution**: The tool preserves LaTeX syntax, but review the output. Check for:
- Unescaped special characters
- Unclosed environments
- Missing packages

### Issue: Poor Quality Modifications

**Solution**: 
- Use more specific prompts
- Try a different LLM model (GPT-4 generally better than GPT-3.5)
- Break down complex changes into smaller steps
- Use dry-run to preview before applying

## Example: Complete Resume Optimization

See the complete workflow in `example_usage.py`:

```bash
python example_usage.py
```

This demonstrates:
- Parsing sections
- Extracting content
- Modifying sections
- Generating new content
- All without requiring API keys (uses mock provider)

## Next Steps

1. Start with `sample_resume.tex` to practice
2. Try different prompts and see what works best
3. Adapt your real resume to the format
4. Create multiple versions for different job applications
5. Track which versions get the best response rates

## Support

For issues or questions:
- Check existing GitHub issues
- Review the main README.md
- Create a new issue with details about your problem

Happy resume optimizing! 🚀
