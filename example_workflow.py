#!/usr/bin/env python3
"""
Example workflow showing how to use job_analyzer with the resume modifier.

This script demonstrates:
1. Analyzing a job posting to extract skills
2. Using extracted skills to inform resume modifications
"""

import json
from job_analyzer import analyze_job_posting, print_analysis_results


def example_analyze_and_save():
    """
    Example: Analyze a job posting and save results for later use.
    """
    print("=" * 80)
    print("EXAMPLE: Analyze Job Posting and Save Results")
    print("=" * 80)
    print()
    
    # Read the sample job posting
    with open('sample_job_posting.txt', 'r') as f:
        job_description = f.read()
    
    print("Step 1: Analyzing job posting...")
    print("-" * 80)
    
    # Analyze the job posting
    results = analyze_job_posting(job_description)
    
    # Print results
    print_analysis_results(results)
    
    # Save results to file
    output_file = 'job_analysis_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_file}")
    print()
    
    return results


def example_use_results_in_prompt():
    """
    Example: Show how to use extracted skills in resume modification prompts.
    """
    print("=" * 80)
    print("EXAMPLE: Use Extracted Skills in Resume Prompts")
    print("=" * 80)
    print()
    
    # Load saved results
    try:
        with open('job_analysis_results.json', 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Error: Run example_analyze_and_save() first to generate job_analysis_results.json")
        return
    
    # Extract verified skills
    verified_skills = results.get('final_verified_data', {})
    job_title = results.get('job_title', {}).get('value', 'Unknown')
    
    # Generate a sample prompt for the summary section
    hard_skills = verified_skills.get('hard_skills', [])
    tools = verified_skills.get('tools_technologies', [])
    soft_skills = verified_skills.get('soft_skills', [])
    
    print("Job Title:", job_title)
    print()
    
    print("Suggested prompt for 'summary' section in prompts.yaml:")
    print("-" * 80)
    
    summary_prompt = f"""Rewrite this summary to emphasize:
- Job title alignment: {job_title}
- Technical skills: {', '.join(hard_skills[:5])}
- Tools/Technologies: {', '.join(tools[:5])}
- Soft skills: {', '.join(soft_skills[:3])}

Make it concise, impactful, and tailored to match the job requirements."""
    
    print(summary_prompt)
    print()
    
    print("Suggested prompt for 'skills' section in prompts.yaml:")
    print("-" * 80)
    
    skills_prompt = f"""Update the skills section to emphasize:
- Required tools: {', '.join(tools)}
- Key technical skills: {', '.join(hard_skills)}

Reorganize by relevance to the target role. Ensure all listed skills are ones you actually possess."""
    
    print(skills_prompt)
    print()
    
    print("=" * 80)
    print("💡 TIP: Copy these prompts into prompts.yaml and set enabled: true")
    print("=" * 80)
    print()


def example_full_workflow():
    """
    Example: Complete workflow from job analysis to resume modification hints.
    """
    print("\n" + "=" * 80)
    print("COMPLETE WORKFLOW EXAMPLE")
    print("=" * 80)
    print()
    
    print("This workflow demonstrates:")
    print("1. Analyzing a job posting to extract and verify skills")
    print("2. Generating targeted prompts for resume modification")
    print("3. Saving results for reference")
    print()
    
    input("Press Enter to continue...")
    print()
    
    # Step 1: Analyze job posting
    results = example_analyze_and_save()
    
    print()
    input("Press Enter to see how to use these results...")
    print()
    
    # Step 2: Generate prompts based on results
    example_use_results_in_prompt()
    
    print()
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Review the extracted skills and verify they match the job posting")
    print("2. Copy the suggested prompts into prompts.yaml")
    print("3. Adjust prompts based on your actual experience")
    print("4. Run: python modifier.py")
    print("5. Review the modified resume and adjust as needed")
    print("=" * 80)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'analyze':
            example_analyze_and_save()
        elif sys.argv[1] == 'prompts':
            example_use_results_in_prompt()
        elif sys.argv[1] == 'full':
            example_full_workflow()
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Usage: python example_workflow.py [analyze|prompts|full]")
    else:
        print("Usage: python example_workflow.py [analyze|prompts|full]")
        print()
        print("Commands:")
        print("  analyze  - Analyze job posting and save results")
        print("  prompts  - Generate resume modification prompts from saved results")
        print("  full     - Run complete workflow (interactive)")
        print()
        print("Example:")
        print("  python example_workflow.py analyze")
