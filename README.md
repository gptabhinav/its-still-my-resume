# LaTeX Resume Modifier

Using LLMs to modify resume sections for getting 80%+ job match where possible.

### Overview

A simple tool to modify specific sections of your LaTeX resume using LLM. Uses tags in your LaTeX file to identify and modify specific sections based on prompts you define.

### Features

- **Tag-based section modification** - Mark sections in your LaTeX with tags
- **Flexible prompts** - Define different modifications for different sections 
- **Preserve formatting** - Maintains LaTeX structure and formatting (still need to add a check for this)
- **Backup support** - Automatically back up your original file
- **Job posting analyzer** - Extract and verify relevant skills from job postings (NEW!)

### Quick Start

#### 1. Installation

```bash
pip install -r requirements.txt
```

#### 2. Set up API key to use LLM

Option A: Edit `config.yaml` and add your API key:
```yaml
llm:
  provider: openai
  api_key: YOUR_API_KEY_HERE
  model: gpt-4
```

Option B: Use environment variable:
```bash
export OPENAI_API_KEY=your_key_here
```

#### 3. Configure prompts for specifc sections

Edit `prompts.yaml` to define which sections to modify and how:

```yaml
prompts:
  - tag: summary
    prompt: |
      Rewrite this summary to emphasize backend development expertise
    enabled: true
```

Set `enabled: true` for sections you want to modify.

#### 4. Run

```bash
python modifier.py
```

### (Additional)
It might help to have a local latex renderer like the `Latex Workshop` extension in vscode.  If you are in linux, you might need this too
```bash
sudo apt update
sudo apt install latexmk texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
```

The script will:
1. Read `base-template.tex` 
2. Process sections marked with enabled prompts
3. Write output to `resume.tex` (configurable in `config.yaml`)
4. Create a backup of the original file (check config.yaml)

### File Structure

- **base-template.tex** - base resume template with tagged sections for testing
- **config.yaml** - API keys and other configurations
- **prompts.yaml** - prompts for modifying each section
- **modifier.py** - main script

### How It Works?

#### Tagging Sections

In your LaTeX file, wrap sections with tags:

```latex
% TAG: summary
\section{Summary}
Your summary content here...
% END_TAG: summary

% TAG: experience  
\section{Experience}
Your experience content here...
% END_TAG: experience
```

### Defining Prompts

In `prompts.yaml`, specify modifications:

```yaml
prompts:
  - tag: summary
    prompt: "Make this more concise and emphasize cloud expertise"
    enabled: true
    
  - tag: experience
    prompt: "Add quantifiable metrics to each bullet point"
    enabled: true
```

### Running

```bash
python modifier.py
```

### Configuration

#### config.yaml

```yaml
# LLM settings
llm:
  provider: openai  # or anthropic
  api_key: YOUR_API_KEY_HERE
  model: gpt-4

# File paths
template:
  input_file: base-template.tex
  output_file: resume.tex

# Options
options:
  create_backup: true
  backup_suffix: .backup
```

#### prompts.yaml

```yaml
prompts:
  - tag: section_name
    prompt: |
      Your modification instructions here.
      Can be multiple lines.
    enabled: true
```

### Examples

#### Tailor for Backend Engineer Role

```yaml
- tag: summary
  prompt: |
    Rewrite emphasizing: Python expertise, microservices architecture,
    distributed systems, and 5+ years experience. Target senior backend role.
  enabled: true

- tag: experience
  prompt: |
    Add metrics: user numbers, performance improvements, system scale.
    Emphasize backend technologies and architecture decisions.
  enabled: true
```

#### Add Cloud Technologies

```yaml
- tag: skills
  prompt: |
    Add AWS (Lambda, ECS, RDS), Docker, Kubernetes, Terraform.
    Organize by category: Languages, Cloud, DevOps, Databases.
  enabled: true
```

### Tips

1. **Be specific in prompts** - Be clear midge
2. **Enable backup** - Better be safe than sorry, why would you wanna disable this?
3. **Iterate** - Context not saved. It will server you good to rinse and repeat till you get good results
4. **Review output** - Always review content (never trust LLMs)

### Job Posting Analyzer

The job posting analyzer helps you extract relevant skills from job descriptions and verify that the extracted information is accurate.

#### Usage

```bash
python job_analyzer.py sample_job_posting.txt
```

Or save the results to a JSON file:

```bash
python job_analyzer.py sample_job_posting.txt --output results.json
```

#### What It Extracts

The analyzer extracts the following information from job postings:

- **Job Title**: The position being advertised
- **Hard Skills**: Technical competencies (e.g., "machine learning", "REST APIs", "SQL")
- **Soft Skills**: Interpersonal/behavioral skills (e.g., "communication", "leadership")
- **Tools & Technologies**: Specific tools, frameworks, languages (e.g., "Python", "Docker", "AWS")
- **Action Verbs**: Key action words describing responsibilities (e.g., "develop", "design", "collaborate")
- **Seniority Signals**: Experience level indicators (e.g., "5+ years", "senior", "lead")
- **Domain Keywords**: Industry/domain specific terms (e.g., "fintech", "e-commerce", "healthcare")

#### Verification

The analyzer includes a **verification step** that checks if each extracted item is actually present in the original job description. This prevents hallucination and ensures accuracy.

The output includes:
- ✓ Verified items (actually present in the job description)
- ✗ Unverified items (not found in the job description)
- Verification rate (percentage of items verified)

#### Example Output

```
JOB POSTING ANALYSIS RESULTS
================================================================================

📋 Job Title: Senior Backend Engineer
   Verified: ✓
   Confidence: high

VERIFIED EXTRACTED INFORMATION
--------------------------------------------------------------------------------

Hard Skills: (5 items)
  ✓ Backend software development
  ✓ System design
  ✓ Distributed systems
  ✓ RESTful APIs
  ✓ Database optimization

...

VERIFICATION SUMMARY
--------------------------------------------------------------------------------
Total Extracted: 45
Total Verified: 43
Verification Rate: 95.6%
```

### Troubleshooting

**API Key Error**: Make sure your API key is set in `config.yaml` or as an environment variable

**Tag Not Found**: Check that your LaTeX file has matching `% TAG:` and `% END_TAG:` markers

**No Prompts**: Set `enabled: true` in `prompts.yaml` for sections you want to modify

### License

MIT License - Use freely 
