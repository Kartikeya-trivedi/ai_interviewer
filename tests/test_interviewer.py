"""
Unit tests for the AI Interviewer System.
Tests core functionality and platform compatibility.
"""

import unittest
import platform
from src.interviewer import AIInterviewer


class TestAIInterviewer(unittest.TestCase):
    """Test cases for AIInterviewer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.interviewer = AIInterviewer()
    
    def test_initialization(self):
        """Test interviewer initialization."""
        self.assertIsNotNone(self.interviewer)
        self.assertEqual(len(self.interviewer.questions), 0)
        self.assertEqual(len(self.interviewer.responses), 0)
    
    def test_platform_detection(self):
        """Test platform detection."""
        self.assertEqual(self.interviewer.platform, platform.system())
    
    def test_get_platform_info(self):
        """Test platform information retrieval."""
        info = self.interviewer.get_platform_info()
        self.assertIsInstance(info, dict)
        self.assertIn("system", info)
        self.assertIn("release", info)
        self.assertIn("version", info)
        self.assertIn("machine", info)
    
    def test_supported_platforms(self):
        """Test platform support check."""
        current_platform = platform.system()
        is_supported = self.interviewer.is_supported_platform()
        
        if current_platform in ["Windows", "Linux"]:
            self.assertTrue(is_supported)
        else:
            self.assertFalse(is_supported)
    
    def test_add_question(self):
        """Test adding questions."""
        self.interviewer.add_question("What is your name?")
        self.assertEqual(len(self.interviewer.questions), 1)
        self.assertEqual(self.interviewer.questions[0], "What is your name?")
    
    def test_add_multiple_questions(self):
        """Test adding multiple questions."""
        questions = [
            "Tell me about yourself.",
            "What are your strengths?",
            "Where do you see yourself in 5 years?"
        ]
        for question in questions:
            self.interviewer.add_question(question)
        
        self.assertEqual(len(self.interviewer.questions), 3)
        self.assertEqual(self.interviewer.questions, questions)
    
    def test_record_response(self):
        """Test recording responses."""
        self.interviewer.record_response("Sample response")
        self.assertEqual(len(self.interviewer.responses), 1)
        self.assertEqual(self.interviewer.responses[0], "Sample response")
    
    def test_get_interview_summary(self):
        """Test interview summary generation."""
        self.interviewer.add_question("Question 1")
        self.interviewer.add_question("Question 2")
        self.interviewer.record_response("Response 1")
        
        summary = self.interviewer.get_interview_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertEqual(summary["total_questions"], 2)
        self.assertEqual(summary["total_responses"], 1)
        self.assertEqual(summary["platform"], platform.system())
    
    def test_custom_config(self):
        """Test interviewer with custom configuration."""
        config = {"max_questions": 5, "timeout": 300}
        interviewer = AIInterviewer(config=config)
        
        self.assertEqual(interviewer.config, config)
        self.assertEqual(interviewer.config["max_questions"], 5)


class TestPlatformCompatibility(unittest.TestCase):
    """Test cases for platform compatibility."""
    
    def test_windows_support(self):
        """Test Windows platform is recognized as supported."""
        interviewer = AIInterviewer()
        if platform.system() == "Windows":
            self.assertTrue(interviewer.is_supported_platform())
    
    def test_linux_support(self):
        """Test Linux platform is recognized as supported."""
        interviewer = AIInterviewer()
        if platform.system() == "Linux":
            self.assertTrue(interviewer.is_supported_platform())


if __name__ == "__main__":
    unittest.main()
