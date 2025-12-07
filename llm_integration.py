"""
LLM integration for modifying LaTeX document sections.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider:
    """Base class for LLM providers."""
    
    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate text based on prompt."""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: Model to use (default: gpt-4)
        """
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("openai package not installed. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate text using OpenAI API.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            
        Returns:
            Generated text
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )
        
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    """Anthropic API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"):
        """
        Initialize Anthropic provider.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use
        """
        try:
            from anthropic import Anthropic
        except ImportError:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
    
    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate text using Anthropic API.
        
        Args:
            prompt: User prompt
            system_message: Optional system message
            
        Returns:
            Generated text
        """
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_message:
            kwargs["system"] = system_message
        
        response = self.client.messages.create(**kwargs)
        
        return response.content[0].text


class LatexModifier:
    """Modify LaTeX sections using LLM."""
    
    def __init__(self, provider: Optional[LLMProvider] = None):
        """
        Initialize the modifier.
        
        Args:
            provider: LLM provider to use (defaults to OpenAI)
        """
        if provider is None:
            # Default to OpenAI
            llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
            model = os.getenv("LLM_MODEL", "gpt-4")
            
            if llm_provider == "openai":
                provider = OpenAIProvider(model=model)
            elif llm_provider == "anthropic":
                provider = AnthropicProvider(model=model)
            else:
                raise ValueError(f"Unsupported LLM provider: {llm_provider}")
        
        self.provider = provider
    
    def modify_section(
        self,
        section_content: str,
        modification_prompt: str,
        section_name: Optional[str] = None
    ) -> str:
        """
        Modify a section using LLM.
        
        Args:
            section_content: The current content of the section
            modification_prompt: Instructions for modification
            section_name: Optional name of the section for context
            
        Returns:
            Modified section content
        """
        system_message = """You are an expert LaTeX editor. Your task is to modify LaTeX document sections based on user instructions.

IMPORTANT RULES:
1. Preserve all LaTeX formatting (commands, environments, etc.)
2. Only modify the content as requested
3. Maintain consistent formatting with the original
4. Return ONLY the modified content, no explanations
5. Keep the same structure unless specifically asked to change it"""
        
        context = ""
        if section_name:
            context = f"\n\nSection name: {section_name}"
        
        prompt = f"""Current section content:
```latex
{section_content}
```
{context}

Instructions: {modification_prompt}

Return the modified section content (LaTeX format only, no explanations):"""
        
        modified_content = self.provider.generate(prompt, system_message)
        
        # Clean up the response (remove markdown code blocks if present)
        modified_content = modified_content.strip()
        if modified_content.startswith("```latex"):
            modified_content = modified_content[8:]
        elif modified_content.startswith("```"):
            modified_content = modified_content[3:]
        
        if modified_content.endswith("```"):
            modified_content = modified_content[:-3]
        
        return modified_content.strip()
    
    def generate_section(
        self,
        section_name: str,
        generation_prompt: str,
        section_level: str = "section"
    ) -> str:
        """
        Generate a new section using LLM.
        
        Args:
            section_name: Name of the section
            generation_prompt: Instructions for generation
            section_level: Level of section (section, subsection, etc.)
            
        Returns:
            Generated section content
        """
        system_message = """You are an expert LaTeX writer. Generate well-formatted LaTeX content based on user instructions.

IMPORTANT RULES:
1. Use proper LaTeX formatting
2. Return ONLY the section content (not the section command itself)
3. Use appropriate LaTeX environments (itemize, enumerate, etc.)
4. No explanations, just the LaTeX content"""
        
        prompt = f"""Generate content for a LaTeX {section_level} named "{section_name}".

Instructions: {generation_prompt}

Return the section content (LaTeX format only, no section command, no explanations):"""
        
        generated_content = self.provider.generate(prompt, system_message)
        
        # Clean up the response
        generated_content = generated_content.strip()
        if generated_content.startswith("```latex"):
            generated_content = generated_content[8:]
        elif generated_content.startswith("```"):
            generated_content = generated_content[3:]
        
        if generated_content.endswith("```"):
            generated_content = generated_content[:-3]
        
        return generated_content.strip()
