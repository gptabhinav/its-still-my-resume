# Example Output

This document shows what the job analyzer output looks like when analyzing a job posting.

## Command

```bash
python job_analyzer.py sample_job_posting.txt
```

## Expected Output

```
================================================================================
Job Posting Analyzer
================================================================================

Reading job posting from: sample_job_posting.txt
Job description length: 1683 characters

Loading configuration...
Loading prompts...
Initializing LLM client...
Using openai with model gpt-4

Extracting information from job posting...
Verifying extracted information...

================================================================================
JOB POSTING ANALYSIS RESULTS
================================================================================

📋 Job Title: Senior Backend Engineer
   Verified: ✓
   Confidence: high

--------------------------------------------------------------------------------
VERIFIED EXTRACTED INFORMATION
--------------------------------------------------------------------------------

Hard Skills: (8 items)
  ✓ Backend software development
  ✓ RESTful APIs
  ✓ Microservices architecture
  ✓ Distributed systems
  ✓ SQL databases
  ✓ NoSQL databases
  ✓ System design
  ✓ Data structures and algorithms

Soft Skills: (4 items)
  ✓ Problem-solving
  ✓ Communication
  ✓ Collaboration
  ✓ Mentoring

Tools & Technologies: (11 items)
  ✓ Python
  ✓ Go
  ✓ PostgreSQL
  ✓ MongoDB
  ✓ Redis
  ✓ AWS
  ✓ GCP
  ✓ Docker
  ✓ Kubernetes
  ✓ RabbitMQ
  ✓ Kafka

Action Verbs: (7 items)
  ✓ Design
  ✓ Develop
  ✓ Build
  ✓ Maintain
  ✓ Collaborate
  ✓ Optimize
  ✓ Mentor

Seniority Signals: (2 items)
  ✓ 5+ years of experience
  ✓ Senior

Domain Keywords: (4 items)
  ✓ E-commerce
  ✓ Platform team
  ✓ High availability
  ✓ Fintech

--------------------------------------------------------------------------------
VERIFICATION SUMMARY
--------------------------------------------------------------------------------
Total Extracted: 36
Total Verified: 36
Verification Rate: 100.0%

================================================================================
```

## With Unverified Items

If the LLM extracts items not in the job description, they would be flagged:

```
--------------------------------------------------------------------------------
⚠️  UNVERIFIED ITEMS (not found in job description)
--------------------------------------------------------------------------------

Tools & Technologies:
  ✗ Terraform (not mentioned in job posting)
  ✗ Jenkins (not mentioned in job posting)

Verification Rate: 94.4%
```

## JSON Output

When using `--output results.json`:

```json
{
  "extracted_data": {
    "job_title": "Senior Backend Engineer",
    "hard_skills": [
      "Backend software development",
      "RESTful APIs",
      "Microservices architecture",
      "Distributed systems",
      "SQL databases",
      "NoSQL databases",
      "System design",
      "Data structures and algorithms"
    ],
    "soft_skills": [
      "Problem-solving",
      "Communication",
      "Collaboration",
      "Mentoring"
    ],
    "tools_technologies": [
      "Python",
      "Go",
      "PostgreSQL",
      "MongoDB",
      "Redis",
      "AWS",
      "GCP",
      "Docker",
      "Kubernetes",
      "RabbitMQ",
      "Kafka"
    ],
    "action_verbs": [
      "Design",
      "Develop",
      "Build",
      "Maintain",
      "Collaborate",
      "Optimize",
      "Mentor"
    ],
    "seniority_signals": [
      "5+ years of experience",
      "Senior"
    ],
    "domain_keywords": [
      "E-commerce",
      "Platform team",
      "High availability",
      "Fintech"
    ]
  },
  "verification_report": {
    "job_title": {
      "value": "Senior Backend Engineer",
      "verified": true,
      "confidence": "high"
    },
    "verified_items": {
      "hard_skills": [...],
      "soft_skills": [...],
      "tools_technologies": [...],
      "action_verbs": [...],
      "seniority_signals": [...],
      "domain_keywords": [...]
    },
    "unverified_items": {
      "hard_skills": [],
      "soft_skills": [],
      "tools_technologies": [],
      "action_verbs": [],
      "seniority_signals": [],
      "domain_keywords": []
    },
    "verification_summary": {
      "total_extracted": 36,
      "total_verified": 36,
      "verification_rate": 1.0
    }
  }
}
```

## Using with Resume Modifier

After analyzing, generate targeted prompts:

```bash
python example_workflow.py prompts
```

Output:
```
Job Title: Senior Backend Engineer

Suggested prompt for 'summary' section in prompts.yaml:
--------------------------------------------------------------------------------
Rewrite this summary to emphasize:
- Job title alignment: Senior Backend Engineer
- Technical skills: Backend software development, RESTful APIs, Microservices architecture, Distributed systems, SQL databases
- Tools/Technologies: Python, Go, PostgreSQL, MongoDB, Redis
- Soft skills: Problem-solving, Communication, Collaboration

Make it concise, impactful, and tailored to match the job requirements.

Suggested prompt for 'skills' section in prompts.yaml:
--------------------------------------------------------------------------------
Update the skills section to emphasize:
- Required tools: Python, Go, PostgreSQL, MongoDB, Redis, AWS, GCP, Docker, Kubernetes, RabbitMQ, Kafka
- Key technical skills: Backend software development, RESTful APIs, Microservices architecture, Distributed systems, SQL databases, NoSQL databases, System design, Data structures and algorithms

Reorganize by relevance to the target role. Ensure all listed skills are ones you actually possess.

================================================================================
💡 TIP: Copy these prompts into prompts.yaml and set enabled: true
================================================================================
```

Then update `prompts.yaml` with these prompts and run `python modifier.py` to modify your resume!
