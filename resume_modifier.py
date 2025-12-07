#!/usr/bin/env python3
"""
CLI tool for modifying LaTeX resume sections using LLM prompts.
"""

import click
import os
from typing import Optional

from latex_parser import LatexParser
from llm_integration import LatexModifier, OpenAIProvider, AnthropicProvider


@click.group()
def cli():
    """LaTeX Resume Modifier - Modify resume sections using LLM prompts."""
    pass


@cli.command()
@click.argument('latex_file', type=click.Path(exists=True))
def list_sections(latex_file: str):
    """List all sections in a LaTeX document."""
    with open(latex_file, 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    sections = parser.list_sections()
    
    if not sections:
        click.echo("No sections found in the document.")
        return
    
    click.echo(f"\nFound {len(sections)} sections:\n")
    for name, level in sections:
        click.echo(f"  [{level}] {name}")
    click.echo()


@cli.command()
@click.argument('latex_file', type=click.Path(exists=True))
@click.argument('section_name')
@click.argument('prompt')
@click.option('--output', '-o', help='Output file (default: overwrites input)')
@click.option('--provider', '-p', type=click.Choice(['openai', 'anthropic']), 
              help='LLM provider to use')
@click.option('--model', '-m', help='Model to use')
@click.option('--dry-run', is_flag=True, help='Show changes without saving')
def modify(latex_file: str, section_name: str, prompt: str, output: Optional[str],
          provider: Optional[str], model: Optional[str], dry_run: bool):
    """Modify a specific section using LLM prompt."""
    
    # Read the LaTeX file
    with open(latex_file, 'r') as f:
        content = f.read()
    
    # Parse the document
    parser = LatexParser(content)
    section = parser.get_section(section_name)
    
    if not section:
        click.echo(f"Error: Section '{section_name}' not found.", err=True)
        click.echo("\nAvailable sections:")
        for name, level in parser.list_sections():
            click.echo(f"  - {name}")
        return
    
    # Initialize LLM provider
    llm_provider = None
    if provider:
        if provider == 'openai':
            llm_provider = OpenAIProvider(model=model or 'gpt-4')
        elif provider == 'anthropic':
            llm_provider = AnthropicProvider(model=model or 'claude-3-sonnet-20240229')
    
    modifier = LatexModifier(provider=llm_provider)
    
    # Show original content
    click.echo(f"\n{'='*60}")
    click.echo(f"Section: {section_name} [{section.level}]")
    click.echo(f"{'='*60}")
    click.echo("\nOriginal content:")
    click.echo("-" * 60)
    click.echo(section.content)
    click.echo("-" * 60)
    
    # Modify the section
    click.echo(f"\nApplying modification: {prompt}")
    click.echo("Processing with LLM...")
    
    try:
        modified_content = modifier.modify_section(
            section.content,
            prompt,
            section_name=section_name
        )
        
        # Show modified content
        click.echo("\nModified content:")
        click.echo("-" * 60)
        click.echo(modified_content)
        click.echo("-" * 60)
        
        # Apply changes to document
        modified_doc = parser.replace_section_content(section_name, modified_content)
        
        if dry_run:
            click.echo("\n[DRY RUN] Changes not saved.")
            return
        
        # Save the modified document
        output_file = output or latex_file
        with open(output_file, 'w') as f:
            f.write(modified_doc)
        
        click.echo(f"\n✓ Modified document saved to: {output_file}")
        
    except Exception as e:
        click.echo(f"\nError: {str(e)}", err=True)
        raise


@cli.command()
@click.argument('latex_file', type=click.Path(exists=True))
@click.argument('section_name')
def show(latex_file: str, section_name: str):
    """Show the content of a specific section."""
    with open(latex_file, 'r') as f:
        content = f.read()
    
    parser = LatexParser(content)
    section = parser.get_section(section_name)
    
    if not section:
        click.echo(f"Error: Section '{section_name}' not found.", err=True)
        return
    
    click.echo(f"\nSection: {section_name} [{section.level}]")
    click.echo("=" * 60)
    click.echo(section.content)
    click.echo("=" * 60)


@cli.command()
@click.argument('latex_file', type=click.Path(exists=True))
@click.argument('section_name')
@click.argument('prompt')
@click.option('--level', '-l', default='section',
              type=click.Choice(['section', 'subsection', 'subsubsection']),
              help='Section level (default: section)')
@click.option('--position', type=click.Choice(['end', 'start']), default='end',
              help='Where to insert the section (default: end)')
@click.option('--output', '-o', help='Output file (default: overwrites input)')
@click.option('--provider', '-p', type=click.Choice(['openai', 'anthropic']),
              help='LLM provider to use')
@click.option('--model', '-m', help='Model to use')
def generate(latex_file: str, section_name: str, prompt: str, level: str,
            position: str, output: Optional[str], provider: Optional[str],
            model: Optional[str]):
    """Generate a new section using LLM."""
    
    # Read the LaTeX file
    with open(latex_file, 'r') as f:
        content = f.read()
    
    # Initialize LLM provider
    llm_provider = None
    if provider:
        if provider == 'openai':
            llm_provider = OpenAIProvider(model=model or 'gpt-4')
        elif provider == 'anthropic':
            llm_provider = AnthropicProvider(model=model or 'claude-3-sonnet-20240229')
    
    modifier = LatexModifier(provider=llm_provider)
    
    click.echo(f"\nGenerating new {level}: {section_name}")
    click.echo(f"Prompt: {prompt}")
    click.echo("Processing with LLM...")
    
    try:
        # Generate section content
        generated_content = modifier.generate_section(
            section_name,
            prompt,
            section_level=level
        )
        
        click.echo("\nGenerated content:")
        click.echo("-" * 60)
        click.echo(generated_content)
        click.echo("-" * 60)
        
        # Create the full section
        new_section = f"\n\\{level}{{{section_name}}}\n{generated_content}\n"
        
        # Add to document
        if position == 'end':
            # Add before \end{document} if it exists
            if '\\end{document}' in content:
                modified_doc = content.replace('\\end{document}', new_section + '\\end{document}')
            else:
                modified_doc = content + new_section
        else:
            # Add after \begin{document} if it exists
            if '\\begin{document}' in content:
                modified_doc = content.replace('\\begin{document}', '\\begin{document}' + new_section)
            else:
                modified_doc = new_section + content
        
        # Save the modified document
        output_file = output or latex_file
        with open(output_file, 'w') as f:
            f.write(modified_doc)
        
        click.echo(f"\n✓ New section added to: {output_file}")
        
    except Exception as e:
        click.echo(f"\nError: {str(e)}", err=True)
        raise


if __name__ == '__main__':
    cli()
