#!/usr/bin/env python3
"""
Example usage of the LaTeX Resume Modifier library.
This demonstrates how to use the library programmatically.
"""

from latex_parser import LatexParser
from llm_integration import LatexModifier, LLMProvider


def example_parse_and_list():
    """Example: Parse a LaTeX document and list sections."""
    print("=" * 60)
    print("Example 1: Parse and List Sections")
    print("=" * 60)
    
    with open('sample_resume.tex', 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    
    print(f"\nFound {len(parser.sections)} sections:\n")
    for name, level in parser.list_sections():
        print(f"  [{level:12}] {name}")
    
    print("\n")


def example_get_section_content():
    """Example: Get content of a specific section."""
    print("=" * 60)
    print("Example 2: Get Section Content")
    print("=" * 60)
    
    with open('sample_resume.tex', 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    section = parser.get_section("Summary")
    
    if section:
        print(f"\nSection: {section.name} [{section.level}]")
        print("-" * 60)
        print(section.content)
        print("-" * 60)
    
    print("\n")


def example_replace_section():
    """Example: Replace section content."""
    print("=" * 60)
    print("Example 3: Replace Section Content")
    print("=" * 60)
    
    with open('sample_resume.tex', 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    
    new_content = """Highly motivated software engineer with 5+ years of experience in building scalable web applications. Expert in Python, JavaScript, and cloud technologies. Proven track record of delivering high-quality solutions and leading technical initiatives."""
    
    modified_doc = parser.replace_section_content("Summary", new_content)
    
    # Show the modified section
    modified_parser = LatexParser(modified_doc)
    section = modified_parser.get_section("Summary")
    
    print("\nModified Summary section:")
    print("-" * 60)
    print(section.content)
    print("-" * 60)
    
    print("\n")


def example_extract_environments():
    """Example: Extract LaTeX environments."""
    print("=" * 60)
    print("Example 4: Extract Environments")
    print("=" * 60)
    
    with open('sample_resume.tex', 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    
    # Extract all itemize environments
    itemize_contents = parser.extract_environment("itemize")
    
    print(f"\nFound {len(itemize_contents)} itemize environments:\n")
    for i, items in enumerate(itemize_contents[:2], 1):  # Show first 2
        print(f"Environment {i}:")
        print(items[:200] + "..." if len(items) > 200 else items)
        print()
    
    print("\n")


class MockProvider(LLMProvider):
    """Simple mock provider for demonstration."""
    def generate(self, prompt, system_message=None):
        return """Senior Software Engineer with 7+ years of experience specializing in distributed systems and cloud architecture. Expertise in Python, Go, and Kubernetes. Led multiple teams to deliver mission-critical services serving millions of users. Strong focus on scalability, reliability, and team mentorship."""


def example_with_mock_llm():
    """Example: Use mock LLM provider (no API key needed)."""
    print("=" * 60)
    print("Example 5: Using Mock LLM Provider")
    print("=" * 60)
    
    with open('sample_resume.tex', 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    section = parser.get_section("Summary")
    
    print("\nOriginal Summary:")
    print("-" * 60)
    print(section.content)
    print("-" * 60)
    
    # Use mock provider (no API key needed)
    mock_provider = MockProvider()
    modifier = LatexModifier(provider=mock_provider)
    
    modified_content = modifier.modify_section(
        section.content,
        "Tailor for a senior backend engineer role emphasizing distributed systems"
    )
    
    print("\nModified Summary (using mock LLM):")
    print("-" * 60)
    print(modified_content)
    print("-" * 60)
    
    print("\n")


def example_get_sections_by_level():
    """Example: Get sections by level."""
    print("=" * 60)
    print("Example 6: Get Sections by Level")
    print("=" * 60)
    
    with open('sample_resume.tex', 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    
    # Get all main sections
    sections = parser.get_sections_by_level("section")
    print(f"\nMain sections ({len(sections)}):")
    for section in sections:
        print(f"  - {section.name}")
    
    # Get all subsections
    subsections = parser.get_sections_by_level("subsection")
    print(f"\nSubsections ({len(subsections)}):")
    for section in subsections:
        print(f"  - {section.name}")
    
    print("\n")


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("LaTeX Resume Modifier - Example Usage")
    print("*" * 60)
    print("\n")
    
    try:
        example_parse_and_list()
        example_get_section_content()
        example_replace_section()
        example_extract_environments()
        example_with_mock_llm()
        example_get_sections_by_level()
        
        print("=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        print("\n")
        
    except FileNotFoundError:
        print("Error: sample_resume.tex not found.")
        print("Make sure you're running this from the repository root.")
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
