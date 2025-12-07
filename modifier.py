#!/usr/bin/env python3
"""
Simple LaTeX Resume Modifier
Modifies tagged sections in a LaTeX resume using LLM prompts.
"""

import os
import re
import yaml
import shutil
from pathlib import Path


def load_config(config_file='config.yaml'):
    """Load configuration from YAML file."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


def load_prompts(prompts_file='prompts.yaml'):
    """Load prompts from YAML file."""
    with open(prompts_file, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('prompts', [])


def extract_tagged_section(content, tag):
    """Extract content between TAG and END_TAG markers."""
    pattern = rf'% TAG: {tag}\n(.*?)\n% END_TAG: {tag}'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1), match.start(), match.end()
    return None, None, None


def replace_tagged_section(content, tag, new_content):
    """Replace content between TAG and END_TAG markers."""
    pattern = rf'(% TAG: {tag}\n).*?(\n% END_TAG: {tag})'
    # Use a function for replacement to avoid issues with backslashes in LaTeX content
    modified = re.sub(pattern, lambda m: m.group(1) + new_content + m.group(2), content, flags=re.DOTALL)
    return modified


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


def modify_with_llm(client, model, provider_type, section_content, prompt):
    """Modify section content using LLM."""
    system_message = """You are an expert resume writer. Modify the LaTeX content based on the user's instructions.

IMPORTANT:
- Preserve all LaTeX formatting (commands, environments, etc.)
- Only modify the content as requested
- Return ONLY the modified LaTeX content, no explanations or markdown code blocks
- Maintain consistent formatting with the original"""
    
    full_prompt = f"""Current section content:
{section_content}

Instructions: {prompt}

Return the modified content (LaTeX format only):"""
    
    if provider_type == 'openai':
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7
        )
        modified = response.choices[0].message.content
    elif provider_type == 'anthropic':
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_message,
            messages=[{"role": "user", "content": full_prompt}]
        )
        modified = response.content[0].text
    
    # Clean up response (remove markdown code blocks if present)
    modified = modified.strip()
    if modified.startswith('```latex'):
        modified = modified[8:]
    elif modified.startswith('```'):
        modified = modified[3:]
    if modified.endswith('```'):
        modified = modified[:-3]
    
    return modified.strip()


def main():
    """Main execution function."""
    print("=" * 70)
    print("LaTeX Resume Modifier")
    print("=" * 70)
    print()
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load prompts
    print("Loading prompts...")
    prompts = load_prompts()
    enabled_prompts = [p for p in prompts if p.get('enabled', False)]
    
    if not enabled_prompts:
        print("No enabled prompts found in prompts.yaml")
        print("Set 'enabled: true' for the sections you want to modify.")
        return
    
    print(f"Found {len(enabled_prompts)} enabled prompt(s)")
    print()
    
    # Load template
    template_file = config['template']['input_file']
    print(f"Reading template: {template_file}")
    
    if not os.path.exists(template_file):
        print(f"Error: Template file '{template_file}' not found!")
        return
    
    with open(template_file, 'r') as f:
        content = f.read()
    
    # Create backup if configured
    if config['options'].get('create_backup', True):
        backup_file = template_file + config['options'].get('backup_suffix', '.backup')
        shutil.copy2(template_file, backup_file)
        print(f"Backup created: {backup_file}")
    
    # Initialize LLM client
    print("Initializing LLM client...")
    try:
        client, model, provider_type = get_llm_client(config)
        print(f"Using {config['llm']['provider']} with model {model}")
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        return
    
    print()
    print("=" * 70)
    print("Processing sections...")
    print("=" * 70)
    print()
    
    # Process each enabled prompt
    for prompt_config in enabled_prompts:
        tag = prompt_config['tag']
        prompt = prompt_config['prompt']
        
        print(f"Processing section: {tag}")
        print("-" * 70)
        
        # Extract section
        section_content, start_pos, end_pos = extract_tagged_section(content, tag)
        
        if section_content is None:
            print(f"  Warning: Tag '{tag}' not found in template")
            print()
            continue
        
        print(f"  Original content ({len(section_content)} chars)")
        
        # Modify with LLM
        try:
            print(f"  Modifying with LLM...")
            modified_content = modify_with_llm(client, model, provider_type, section_content, prompt)
            print(f"  Modified content ({len(modified_content)} chars)")
            
            # Replace in document
            content = replace_tagged_section(content, tag, modified_content)
            print(f"  ✓ Section updated")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
    
    # Write output
    output_file = config['template'].get('output_file', template_file.replace('.tex', '.modified.tex'))
    print("=" * 70)
    print(f"Writing output to: {output_file}")
    
    with open(output_file, 'w') as f:
        f.write(content)
    
    print("✓ Done!")
    print("=" * 70)


if __name__ == '__main__':
    main()
