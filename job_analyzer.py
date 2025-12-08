#!/usr/bin/env python3
"""
Job Posting Analyzer
Extracts and verifies relevant skills from job postings.
"""

import os
import re
import yaml
import json
from typing import Dict, List, Any


def load_config(config_file='config.yaml'):
    """Load configuration from YAML file."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def get_llm_client(config):
    """Initialize LLM client based on configuration."""
    provider = config['llm']['provider']
    api_key = config['llm'].get('api_key')
    
    # Check environment variable if not in config
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        if provider == 'openai':
            api_key = os.getenv('OPENAI_API_KEY')
        elif provider == 'anthropic':
            api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        raise ValueError(f"API key not found for {provider}. Set it in config.yaml or environment variable.")
    
    model = config['llm']['model']
    
    if provider == 'openai':
        from openai import OpenAI
        return OpenAI(api_key=api_key), model, 'openai'
    elif provider == 'anthropic':
        from anthropic import Anthropic
        return Anthropic(api_key=api_key), model, 'anthropic'
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def extract_skills_from_job_posting(client, model, provider_type, job_description: str) -> Dict[str, Any]:
    """
    Extract job title, hard skills, soft skills, tools/technologies, 
    action verbs, seniority signals, and domain keywords from job description.
    """
    system_message = """You are an expert job posting analyzer. Extract structured information from job descriptions.

IMPORTANT:
- Extract ONLY information that is explicitly present in the job description
- Do NOT invent, assume, or infer information that isn't stated
- Return valid JSON with the exact structure requested
- Be thorough but conservative - if unsure, don't include it"""
    
    extraction_prompt = f"""Analyze this job description and extract the following information in JSON format:

Job Description:
{job_description}

Extract the following as a JSON object:
{{
  "job_title": "extracted job title",
  "hard_skills": ["technical skill 1", "technical skill 2"],
  "soft_skills": ["soft skill 1", "soft skill 2"],
  "tools_technologies": ["tool 1", "technology 1"],
  "action_verbs": ["verb 1", "verb 2"],
  "seniority_signals": ["signal 1", "signal 2"],
  "domain_keywords": ["keyword 1", "keyword 2"]
}}

Guidelines:
- hard_skills: Technical competencies (e.g., "machine learning", "REST APIs", "SQL")
- soft_skills: Interpersonal/behavioral skills (e.g., "communication", "leadership")
- tools_technologies: Specific tools, frameworks, languages (e.g., "Python", "Docker", "AWS")
- action_verbs: Key action words describing responsibilities (e.g., "develop", "design", "collaborate")
- seniority_signals: Experience level indicators (e.g., "5+ years", "senior", "lead")
- domain_keywords: Industry/domain specific terms (e.g., "fintech", "e-commerce", "healthcare")

Return ONLY the JSON object, no additional text or explanations."""
    
    if provider_type == 'openai':
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        result_text = response.choices[0].message.content
    elif provider_type == 'anthropic':
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_message,
            temperature=0.3,
            messages=[{"role": "user", "content": extraction_prompt}]
        )
        result_text = response.content[0].text
    
    # Parse JSON response
    result_text = result_text.strip()
    # Clean up markdown code blocks if present
    if result_text.startswith('```json'):
        result_text = result_text[7:]
    elif result_text.startswith('```'):
        result_text = result_text[3:]
    if result_text.endswith('```'):
        result_text = result_text[:-3]
    
    try:
        extracted_data = json.loads(result_text.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nResponse: {result_text}")
    
    return extracted_data


def verify_extracted_skills(client, model, provider_type, job_description: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verify that extracted skills are actually present in the job description.
    Returns a verification report with validated data.
    """
    system_message = """You are a verification expert. Your job is to verify that extracted information from a job description is accurate and not hallucinated.

IMPORTANT:
- Check if each extracted item is actually mentioned or strongly implied in the original job description
- Mark items as "verified" only if they appear explicitly or are clearly implied
- Mark items as "not_found" if they are not present in the description
- Be strict in verification - when in doubt, mark as not_found"""
    
    verification_prompt = f"""Original Job Description:
{job_description}

Extracted Information:
{json.dumps(extracted_data, indent=2)}

Verify each extracted item against the original job description. For each category, check if the items are actually present.

Return a JSON object with this structure:
{{
  "job_title": {{
    "value": "extracted job title",
    "verified": true/false,
    "confidence": "high/medium/low"
  }},
  "verified_items": {{
    "hard_skills": ["verified skill 1", "verified skill 2"],
    "soft_skills": ["verified skill 1", "verified skill 2"],
    "tools_technologies": ["verified tool 1", "verified tool 2"],
    "action_verbs": ["verified verb 1", "verified verb 2"],
    "seniority_signals": ["verified signal 1", "verified signal 2"],
    "domain_keywords": ["verified keyword 1", "verified keyword 2"]
  }},
  "unverified_items": {{
    "hard_skills": ["unverified skill 1"],
    "soft_skills": ["unverified skill 1"],
    "tools_technologies": ["unverified tool 1"],
    "action_verbs": ["unverified verb 1"],
    "seniority_signals": ["unverified signal 1"],
    "domain_keywords": ["unverified keyword 1"]
  }},
  "verification_summary": {{
    "total_extracted": 0,
    "total_verified": 0,
    "verification_rate": 0.0
  }}
}}

Return ONLY the JSON object."""
    
    if provider_type == 'openai':
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": verification_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        result_text = response.choices[0].message.content
    elif provider_type == 'anthropic':
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_message,
            temperature=0.1,
            messages=[{"role": "user", "content": verification_prompt}]
        )
        result_text = response.content[0].text
    
    # Parse JSON response
    result_text = result_text.strip()
    if result_text.startswith('```json'):
        result_text = result_text[7:]
    elif result_text.startswith('```'):
        result_text = result_text[3:]
    if result_text.endswith('```'):
        result_text = result_text[:-3]
    
    try:
        verification_report = json.loads(result_text.strip())
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse verification response as JSON: {e}\nResponse: {result_text}")
    
    return verification_report


def analyze_job_posting(job_description: str, config_file='config.yaml') -> Dict[str, Any]:
    """
    Main function to analyze a job posting and return verified extracted information.
    
    Args:
        job_description: The job posting text to analyze
        config_file: Path to configuration file
    
    Returns:
        Dictionary containing extracted and verified information
    """
    # Load configuration
    config = load_config(config_file)
    
    # Initialize LLM client
    client, model, provider_type = get_llm_client(config)
    
    # Extract skills and information
    print("Extracting information from job posting...")
    extracted_data = extract_skills_from_job_posting(client, model, provider_type, job_description)
    
    # Verify extracted information
    print("Verifying extracted information...")
    verification_report = verify_extracted_skills(client, model, provider_type, job_description, extracted_data)
    
    # Combine results
    result = {
        "extracted_data": extracted_data,
        "verification_report": verification_report,
        "final_verified_data": verification_report.get("verified_items", {}),
        "job_title": verification_report.get("job_title", {})
    }
    
    return result


def print_analysis_results(results: Dict[str, Any]):
    """Pretty print the analysis results."""
    print("\n" + "=" * 80)
    print("JOB POSTING ANALYSIS RESULTS")
    print("=" * 80)
    
    # Job Title
    job_title_info = results.get("job_title", {})
    print(f"\n📋 Job Title: {job_title_info.get('value', 'Not found')}")
    print(f"   Verified: {'✓' if job_title_info.get('verified') else '✗'}")
    print(f"   Confidence: {job_title_info.get('confidence', 'unknown')}")
    
    # Verified Items
    verified = results.get("final_verified_data", {})
    
    print("\n" + "-" * 80)
    print("VERIFIED EXTRACTED INFORMATION")
    print("-" * 80)
    
    categories = [
        ("Hard Skills", "hard_skills"),
        ("Soft Skills", "soft_skills"),
        ("Tools & Technologies", "tools_technologies"),
        ("Action Verbs", "action_verbs"),
        ("Seniority Signals", "seniority_signals"),
        ("Domain Keywords", "domain_keywords")
    ]
    
    for label, key in categories:
        items = verified.get(key, [])
        print(f"\n{label}: ({len(items)} items)")
        if items:
            for item in items:
                print(f"  ✓ {item}")
        else:
            print("  (none)")
    
    # Verification Summary
    summary = results.get("verification_report", {}).get("verification_summary", {})
    if summary:
        print("\n" + "-" * 80)
        print("VERIFICATION SUMMARY")
        print("-" * 80)
        print(f"Total Extracted: {summary.get('total_extracted', 0)}")
        print(f"Total Verified: {summary.get('total_verified', 0)}")
        print(f"Verification Rate: {summary.get('verification_rate', 0):.1%}")
    
    # Unverified Items (if any)
    unverified = results.get("verification_report", {}).get("unverified_items", {})
    has_unverified = any(unverified.get(key, []) for key in ["hard_skills", "soft_skills", "tools_technologies", 
                                                               "action_verbs", "seniority_signals", "domain_keywords"])
    
    if has_unverified:
        print("\n" + "-" * 80)
        print("⚠️  UNVERIFIED ITEMS (not found in job description)")
        print("-" * 80)
        for label, key in categories:
            items = unverified.get(key, [])
            if items:
                print(f"\n{label}:")
                for item in items:
                    print(f"  ✗ {item}")
    
    print("\n" + "=" * 80)


def main():
    """Main execution function for standalone usage."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze job postings to extract and verify skills')
    parser.add_argument('job_file', help='Path to file containing job posting text')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--output', help='Path to save JSON output (optional)')
    
    args = parser.parse_args()
    
    # Read job posting
    if not os.path.exists(args.job_file):
        print(f"Error: Job posting file '{args.job_file}' not found!")
        sys.exit(1)
    
    with open(args.job_file, 'r') as f:
        job_description = f.read()
    
    print("=" * 80)
    print("Job Posting Analyzer")
    print("=" * 80)
    print(f"\nReading job posting from: {args.job_file}")
    print(f"Job description length: {len(job_description)} characters")
    
    try:
        # Analyze job posting
        results = analyze_job_posting(job_description, args.config)
        
        # Print results
        print_analysis_results(results)
        
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Results saved to: {args.output}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
