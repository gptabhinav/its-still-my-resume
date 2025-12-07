"""
LaTeX document parser for extracting and managing sections.
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class LatexSection:
    """Represents a section in a LaTeX document."""
    name: str
    level: str  # section, subsection, subsubsection, etc.
    content: str
    start_pos: int
    end_pos: int
    full_text: str  # Including the section command


class LatexParser:
    """Parser for LaTeX documents to extract and manage sections."""
    
    # Section commands in order of hierarchy
    SECTION_COMMANDS = [
        'part',
        'chapter',
        'section',
        'subsection',
        'subsubsection',
        'paragraph',
        'subparagraph'
    ]
    
    def __init__(self, latex_content: str):
        """
        Initialize the parser with LaTeX content.
        
        Args:
            latex_content: The full LaTeX document content
        """
        self.content = latex_content
        self.sections = []
        self._parse_sections()
    
    def _parse_sections(self):
        """Parse all sections from the LaTeX document."""
        # Pattern to match section commands
        # Matches: \section{title}, \subsection{title}, etc.
        pattern = r'\\(' + '|'.join(self.SECTION_COMMANDS) + r')\{([^}]+)\}'
        
        matches = list(re.finditer(pattern, self.content))
        
        for i, match in enumerate(matches):
            level = match.group(1)
            name = match.group(2)
            start_pos = match.start()
            
            # Find the end position (start of next section or end of document)
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(self.content)
            
            # Extract content (everything after the section command until next section)
            full_text = self.content[start_pos:end_pos]
            
            # Content is everything after the section header line
            header_end = match.end()
            content = self.content[header_end:end_pos].strip()
            
            section = LatexSection(
                name=name,
                level=level,
                content=content,
                start_pos=start_pos,
                end_pos=end_pos,
                full_text=full_text
            )
            
            self.sections.append(section)
    
    def get_section(self, section_name: str) -> Optional[LatexSection]:
        """
        Get a section by its name.
        
        Args:
            section_name: The name of the section to retrieve
            
        Returns:
            LatexSection if found, None otherwise
        """
        for section in self.sections:
            if section.name.lower() == section_name.lower():
                return section
        return None
    
    def get_sections_by_level(self, level: str) -> List[LatexSection]:
        """
        Get all sections of a specific level.
        
        Args:
            level: The section level (e.g., 'section', 'subsection')
            
        Returns:
            List of sections matching the level
        """
        return [s for s in self.sections if s.level == level]
    
    def list_sections(self) -> List[Tuple[str, str]]:
        """
        List all sections with their levels.
        
        Returns:
            List of tuples (section_name, section_level)
        """
        return [(s.name, s.level) for s in self.sections]
    
    def replace_section_content(self, section_name: str, new_content: str) -> str:
        """
        Replace the content of a specific section.
        
        Args:
            section_name: The name of the section to modify
            new_content: The new content for the section
            
        Returns:
            Modified LaTeX document
        """
        section = self.get_section(section_name)
        if not section:
            raise ValueError(f"Section '{section_name}' not found")
        
        # Build the new section text
        section_header = f"\\{section.level}{{{section.name}}}\n"
        new_section_text = section_header + new_content.strip()
        
        # If there's whitespace before the next section, preserve it
        if section.end_pos < len(self.content):
            trailing = self.content[section.end_pos:section.end_pos+2]
            if trailing.startswith('\n'):
                new_section_text += '\n'
        
        # Replace in the document
        modified = (
            self.content[:section.start_pos] +
            new_section_text +
            self.content[section.end_pos:]
        )
        
        return modified
    
    def get_preamble(self) -> str:
        """
        Get the document preamble (everything before first section).
        
        Returns:
            The preamble content
        """
        if not self.sections:
            return self.content
        
        return self.content[:self.sections[0].start_pos]
    
    def extract_environment(self, env_name: str) -> List[str]:
        """
        Extract content from LaTeX environments (e.g., itemize, enumerate).
        
        Args:
            env_name: Name of the environment
            
        Returns:
            List of environment contents
        """
        pattern = r'\\begin\{' + env_name + r'\}(.*?)\\end\{' + env_name + r'\}'
        matches = re.findall(pattern, self.content, re.DOTALL)
        return matches
