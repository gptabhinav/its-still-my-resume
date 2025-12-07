"""
Tests for LLM integration module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from llm_integration import LatexModifier, LLMProvider, OpenAIProvider, AnthropicProvider


class MockLLMProvider(LLMProvider):
    """Mock LLM provider for testing."""
    
    def __init__(self, response: str = "Modified content"):
        self.response = response
        self.last_prompt = None
        self.last_system_message = None
    
    def generate(self, prompt: str, system_message: str = None) -> str:
        self.last_prompt = prompt
        self.last_system_message = system_message
        return self.response


def test_latex_modifier_initialization():
    """Test LatexModifier initialization with mock provider."""
    provider = MockLLMProvider()
    modifier = LatexModifier(provider=provider)
    
    assert modifier.provider == provider


def test_modify_section_basic():
    """Test basic section modification."""
    provider = MockLLMProvider(response="Updated section content")
    modifier = LatexModifier(provider=provider)
    
    original_content = "Original content here"
    prompt = "Make it more concise"
    
    result = modifier.modify_section(original_content, prompt)
    
    assert result == "Updated section content"
    assert original_content in provider.last_prompt
    assert prompt in provider.last_prompt


def test_modify_section_with_section_name():
    """Test section modification with section name context."""
    provider = MockLLMProvider(response="Updated content")
    modifier = LatexModifier(provider=provider)
    
    result = modifier.modify_section(
        "Original content",
        "Add more details",
        section_name="Experience"
    )
    
    assert "Experience" in provider.last_prompt


def test_modify_section_removes_code_blocks():
    """Test that markdown code blocks are removed from response."""
    provider = MockLLMProvider(response="```latex\nCleaned content\n```")
    modifier = LatexModifier(provider=provider)
    
    result = modifier.modify_section("Original", "Modify this")
    
    assert result == "Cleaned content"
    assert "```" not in result


def test_modify_section_removes_plain_code_blocks():
    """Test removal of plain code blocks."""
    provider = MockLLMProvider(response="```\nCleaned content\n```")
    modifier = LatexModifier(provider=provider)
    
    result = modifier.modify_section("Original", "Modify this")
    
    assert result == "Cleaned content"
    assert "```" not in result


def test_generate_section_basic():
    """Test basic section generation."""
    provider = MockLLMProvider(response="Generated section content")
    modifier = LatexModifier(provider=provider)
    
    result = modifier.generate_section(
        section_name="Projects",
        generation_prompt="Create a projects section"
    )
    
    assert result == "Generated section content"
    assert "Projects" in provider.last_prompt
    assert "Create a projects section" in provider.last_prompt


def test_generate_section_with_level():
    """Test section generation with specific level."""
    provider = MockLLMProvider(response="Subsection content")
    modifier = LatexModifier(provider=provider)
    
    result = modifier.generate_section(
        section_name="Details",
        generation_prompt="Add details",
        section_level="subsection"
    )
    
    assert "subsection" in provider.last_prompt


def test_system_message_contains_latex_instructions():
    """Test that system message contains LaTeX-specific instructions."""
    provider = MockLLMProvider()
    modifier = LatexModifier(provider=provider)
    
    modifier.modify_section("Content", "Modify")
    
    assert provider.last_system_message is not None
    assert "latex" in provider.last_system_message.lower()
    assert "formatting" in provider.last_system_message.lower()


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_openai_provider_initialization():
    """Test OpenAI provider initialization."""
    with patch('openai.OpenAI') as mock_openai_class:
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        provider = OpenAIProvider(api_key='test-key', model='gpt-4')
        
        assert provider.model == 'gpt-4'
        assert provider.api_key == 'test-key'
        mock_openai_class.assert_called_once_with(api_key='test-key')


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
def test_openai_provider_generate():
    """Test OpenAI provider generate method."""
    with patch('openai.OpenAI') as mock_openai_class:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated text"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai_class.return_value = mock_client
        
        provider = OpenAIProvider(api_key='test-key')
        result = provider.generate("Test prompt", "System message")
        
        assert result == "Generated text"
        mock_client.chat.completions.create.assert_called_once()


@patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
def test_anthropic_provider_initialization():
    """Test Anthropic provider initialization."""
    with patch('anthropic.Anthropic') as mock_anthropic_class:
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        
        provider = AnthropicProvider(api_key='test-key')
        
        assert provider.api_key == 'test-key'
        mock_anthropic_class.assert_called_once_with(api_key='test-key')


@patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'})
def test_anthropic_provider_generate():
    """Test Anthropic provider generate method."""
    with patch('anthropic.Anthropic') as mock_anthropic_class:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Generated text"
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_class.return_value = mock_client
        
        provider = AnthropicProvider(api_key='test-key')
        result = provider.generate("Test prompt", "System message")
        
        assert result == "Generated text"
        mock_client.messages.create.assert_called_once()


def test_openai_provider_no_api_key():
    """Test that OpenAI provider raises error without API key."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="OpenAI API key"):
            OpenAIProvider()


def test_anthropic_provider_no_api_key():
    """Test that Anthropic provider raises error without API key."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="Anthropic API key"):
            AnthropicProvider()


@patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key', 'LLM_PROVIDER': 'openai'})
def test_latex_modifier_default_provider():
    """Test that LatexModifier uses default provider from environment."""
    with patch('openai.OpenAI') as mock_openai_class:
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        modifier = LatexModifier()
        
        assert isinstance(modifier.provider, OpenAIProvider)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
