"""
Tests for LaTeX parser module.
"""

import pytest
from latex_parser import LatexParser, LatexSection


SAMPLE_LATEX = r"""
\documentclass{article}
\begin{document}

\section{Introduction}
This is the introduction section with some content.

\section{Methods}
This section describes the methods used.

\subsection{Data Collection}
Information about data collection.

\subsection{Analysis}
Details about the analysis process.

\section{Results}
The results of the study.

\end{document}
"""


def test_parse_sections():
    """Test that sections are correctly parsed."""
    parser = LatexParser(SAMPLE_LATEX)
    
    assert len(parser.sections) == 5
    assert parser.sections[0].name == "Introduction"
    assert parser.sections[0].level == "section"
    assert parser.sections[1].name == "Methods"
    assert parser.sections[2].name == "Data Collection"
    assert parser.sections[2].level == "subsection"


def test_get_section():
    """Test retrieving a specific section."""
    parser = LatexParser(SAMPLE_LATEX)
    
    section = parser.get_section("Methods")
    assert section is not None
    assert section.name == "Methods"
    assert section.level == "section"
    assert "methods used" in section.content.lower()


def test_get_section_not_found():
    """Test retrieving a non-existent section."""
    parser = LatexParser(SAMPLE_LATEX)
    
    section = parser.get_section("NonExistent")
    assert section is None


def test_get_sections_by_level():
    """Test retrieving sections by level."""
    parser = LatexParser(SAMPLE_LATEX)
    
    sections = parser.get_sections_by_level("section")
    assert len(sections) == 3
    
    subsections = parser.get_sections_by_level("subsection")
    assert len(subsections) == 2


def test_list_sections():
    """Test listing all sections."""
    parser = LatexParser(SAMPLE_LATEX)
    
    sections = parser.list_sections()
    assert len(sections) == 5
    assert sections[0] == ("Introduction", "section")
    assert sections[2] == ("Data Collection", "subsection")


def test_replace_section_content():
    """Test replacing section content."""
    parser = LatexParser(SAMPLE_LATEX)
    
    new_content = "This is completely new content for the introduction."
    modified = parser.replace_section_content("Introduction", new_content)
    
    assert new_content in modified
    assert "\\section{Introduction}" in modified
    
    # Verify other sections are still present
    assert "\\section{Methods}" in modified
    assert "\\section{Results}" in modified


def test_get_preamble():
    """Test extracting document preamble."""
    parser = LatexParser(SAMPLE_LATEX)
    
    preamble = parser.get_preamble()
    assert "\\documentclass{article}" in preamble
    assert "\\begin{document}" in preamble
    assert "\\section" not in preamble


def test_extract_environment():
    """Test extracting LaTeX environments."""
    latex_with_items = r"""
\section{Skills}
\begin{itemize}
\item Python
\item JavaScript
\end{itemize}

Some other text.

\begin{itemize}
\item Docker
\item Kubernetes
\end{itemize}
"""
    
    parser = LatexParser(latex_with_items)
    itemize_contents = parser.extract_environment("itemize")
    
    assert len(itemize_contents) == 2
    assert "Python" in itemize_contents[0]
    assert "Docker" in itemize_contents[1]


def test_case_insensitive_section_search():
    """Test that section search is case-insensitive."""
    parser = LatexParser(SAMPLE_LATEX)
    
    section1 = parser.get_section("introduction")
    section2 = parser.get_section("INTRODUCTION")
    section3 = parser.get_section("Introduction")
    
    assert section1 is not None
    assert section2 is not None
    assert section3 is not None
    assert section1.name == section2.name == section3.name


def test_section_content_extraction():
    """Test that section content is correctly extracted."""
    parser = LatexParser(SAMPLE_LATEX)
    
    section = parser.get_section("Introduction")
    assert section is not None
    
    # Content should not include the section command
    assert "\\section{Introduction}" not in section.content
    
    # Content should be the text after the section header
    assert "introduction section" in section.content.lower()


def test_empty_document():
    """Test parsing an empty document."""
    parser = LatexParser("")
    
    assert len(parser.sections) == 0
    assert parser.list_sections() == []
    assert parser.get_preamble() == ""


def test_document_without_sections():
    """Test parsing a document without sections."""
    latex = r"""
\documentclass{article}
\begin{document}
Just some content without sections.
\end{document}
"""
    
    parser = LatexParser(latex)
    
    assert len(parser.sections) == 0
    preamble = parser.get_preamble()
    assert "\\documentclass{article}" in preamble


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
