#!/usr/bin/env python3
"""
Unit tests for job_analyzer module.
"""

import unittest
import json
import os
from unittest.mock import Mock, patch, MagicMock
from job_analyzer import (
    extract_skills_from_job_posting,
    verify_extracted_skills,
    analyze_job_posting,
    load_config
)


class TestJobAnalyzer(unittest.TestCase):
    """Test cases for job analyzer functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_job_description = """
Senior Backend Engineer - Platform Team

Responsibilities:
- Design and develop RESTful APIs using Python
- Build distributed systems with high availability
- Collaborate with frontend engineers and product managers
- Mentor junior engineers

Required Qualifications:
- 5+ years of backend development experience
- Strong Python and SQL skills
- Experience with AWS and Docker
- Excellent communication skills
"""
        
        self.sample_extracted_data = {
            "job_title": "Senior Backend Engineer",
            "hard_skills": ["RESTful APIs", "distributed systems", "backend development", "SQL"],
            "soft_skills": ["communication", "collaboration", "mentoring"],
            "tools_technologies": ["Python", "AWS", "Docker"],
            "action_verbs": ["Design", "develop", "Build", "Collaborate", "Mentor"],
            "seniority_signals": ["5+ years", "Senior"],
            "domain_keywords": ["Platform Team", "high availability"]
        }
        
        self.sample_verification_report = {
            "job_title": {
                "value": "Senior Backend Engineer",
                "verified": True,
                "confidence": "high"
            },
            "verified_items": {
                "hard_skills": ["RESTful APIs", "distributed systems", "backend development", "SQL"],
                "soft_skills": ["communication", "collaboration", "mentoring"],
                "tools_technologies": ["Python", "AWS", "Docker"],
                "action_verbs": ["Design", "develop", "Build", "Collaborate", "Mentor"],
                "seniority_signals": ["5+ years", "Senior"],
                "domain_keywords": ["Platform Team", "high availability"]
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
                "total_extracted": 21,
                "total_verified": 21,
                "verification_rate": 1.0
            }
        }
    
    def test_extract_skills_openai(self):
        """Test skill extraction with OpenAI provider."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(self.sample_extracted_data)))]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test extraction
        result = extract_skills_from_job_posting(
            mock_client, 
            "gpt-4", 
            "openai", 
            self.sample_job_description
        )
        
        # Verify
        self.assertEqual(result["job_title"], "Senior Backend Engineer")
        self.assertIn("Python", result["tools_technologies"])
        self.assertIn("communication", result["soft_skills"])
        self.assertTrue(mock_client.chat.completions.create.called)
    
    def test_extract_skills_anthropic(self):
        """Test skill extraction with Anthropic provider."""
        # Mock Anthropic response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps(self.sample_extracted_data))]
        mock_client.messages.create.return_value = mock_response
        
        # Test extraction
        result = extract_skills_from_job_posting(
            mock_client,
            "claude-3-sonnet-20240229",
            "anthropic",
            self.sample_job_description
        )
        
        # Verify
        self.assertEqual(result["job_title"], "Senior Backend Engineer")
        self.assertIn("RESTful APIs", result["hard_skills"])
        self.assertTrue(mock_client.messages.create.called)
    
    def test_verify_extracted_skills(self):
        """Test verification of extracted skills."""
        # Mock OpenAI response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(self.sample_verification_report)))]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test verification
        result = verify_extracted_skills(
            mock_client,
            "gpt-4",
            "openai",
            self.sample_job_description,
            self.sample_extracted_data
        )
        
        # Verify
        self.assertTrue(result["job_title"]["verified"])
        self.assertEqual(result["verification_summary"]["verification_rate"], 1.0)
        self.assertEqual(len(result["unverified_items"]["hard_skills"]), 0)
        self.assertTrue(mock_client.chat.completions.create.called)
    
    def test_extract_skills_json_cleanup(self):
        """Test that JSON response cleanup works correctly."""
        # Mock with markdown code blocks
        mock_client = Mock()
        mock_response = Mock()
        wrapped_json = f"```json\n{json.dumps(self.sample_extracted_data)}\n```"
        mock_response.choices = [Mock(message=Mock(content=wrapped_json))]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Test extraction
        result = extract_skills_from_job_posting(
            mock_client,
            "gpt-4",
            "openai",
            self.sample_job_description
        )
        
        # Should successfully parse despite markdown wrapping
        self.assertEqual(result["job_title"], "Senior Backend Engineer")
    
    def test_verification_with_unverified_items(self):
        """Test verification when some items are not verified."""
        # Create verification report with unverified items
        verification_with_unverified = {
            "job_title": {
                "value": "Senior Backend Engineer",
                "verified": True,
                "confidence": "high"
            },
            "verified_items": {
                "hard_skills": ["RESTful APIs", "SQL"],
                "soft_skills": ["communication"],
                "tools_technologies": ["Python"],
                "action_verbs": ["Design", "develop"],
                "seniority_signals": ["5+ years"],
                "domain_keywords": []
            },
            "unverified_items": {
                "hard_skills": ["blockchain"],  # This wasn't in the job description
                "soft_skills": [],
                "tools_technologies": ["Kubernetes"],  # This wasn't mentioned
                "action_verbs": [],
                "seniority_signals": [],
                "domain_keywords": []
            },
            "verification_summary": {
                "total_extracted": 10,
                "total_verified": 8,
                "verification_rate": 0.8
            }
        }
        
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(verification_with_unverified)))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = verify_extracted_skills(
            mock_client,
            "gpt-4",
            "openai",
            self.sample_job_description,
            self.sample_extracted_data
        )
        
        # Verify that unverified items are detected
        self.assertIn("blockchain", result["unverified_items"]["hard_skills"])
        self.assertIn("Kubernetes", result["unverified_items"]["tools_technologies"])
        self.assertEqual(result["verification_summary"]["verification_rate"], 0.8)
    
    def test_empty_job_description(self):
        """Test handling of empty job description."""
        mock_client = Mock()
        empty_result = {
            "job_title": "",
            "hard_skills": [],
            "soft_skills": [],
            "tools_technologies": [],
            "action_verbs": [],
            "seniority_signals": [],
            "domain_keywords": []
        }
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content=json.dumps(empty_result)))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = extract_skills_from_job_posting(
            mock_client,
            "gpt-4",
            "openai",
            ""
        )
        
        self.assertEqual(result["job_title"], "")
        self.assertEqual(len(result["hard_skills"]), 0)
    
    def test_invalid_json_response(self):
        """Test handling of invalid JSON response."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="This is not valid JSON"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        with self.assertRaises(ValueError):
            extract_skills_from_job_posting(
                mock_client,
                "gpt-4",
                "openai",
                self.sample_job_description
            )
    
    def test_load_config(self):
        """Test configuration loading."""
        # This tests the actual config file
        if os.path.exists('config.yaml'):
            config = load_config('config.yaml')
            self.assertIn('llm', config)
            self.assertIn('provider', config['llm'])
            self.assertIn('model', config['llm'])


class TestJobAnalyzerIntegration(unittest.TestCase):
    """Integration tests for job analyzer."""
    
    @patch('job_analyzer.get_llm_client')
    def test_analyze_job_posting_full_flow(self, mock_get_client):
        """Test the complete analyze_job_posting flow."""
        # Mock the LLM client and responses
        mock_client = Mock()
        mock_get_client.return_value = (mock_client, "gpt-4", "openai")
        
        # Mock extraction response
        extracted_data = {
            "job_title": "Senior Software Engineer",
            "hard_skills": ["Python", "SQL"],
            "soft_skills": ["leadership"],
            "tools_technologies": ["Docker"],
            "action_verbs": ["develop"],
            "seniority_signals": ["senior"],
            "domain_keywords": ["software"]
        }
        
        # Mock verification response
        verification_report = {
            "job_title": {
                "value": "Senior Software Engineer",
                "verified": True,
                "confidence": "high"
            },
            "verified_items": extracted_data,
            "unverified_items": {
                "hard_skills": [],
                "soft_skills": [],
                "tools_technologies": [],
                "action_verbs": [],
                "seniority_signals": [],
                "domain_keywords": []
            },
            "verification_summary": {
                "total_extracted": 7,
                "total_verified": 7,
                "verification_rate": 1.0
            }
        }
        
        mock_response_1 = Mock()
        mock_response_1.choices = [Mock(message=Mock(content=json.dumps(extracted_data)))]
        
        mock_response_2 = Mock()
        mock_response_2.choices = [Mock(message=Mock(content=json.dumps(verification_report)))]
        
        mock_client.chat.completions.create.side_effect = [mock_response_1, mock_response_2]
        
        # Test the full flow
        result = analyze_job_posting(
            "Test job description",
            config_file='config.yaml'
        )
        
        # Verify structure
        self.assertIn("extracted_data", result)
        self.assertIn("verification_report", result)
        self.assertIn("final_verified_data", result)
        self.assertIn("job_title", result)
        
        # Verify content
        self.assertEqual(result["job_title"]["value"], "Senior Software Engineer")
        self.assertTrue(result["job_title"]["verified"])


if __name__ == '__main__':
    unittest.main()
