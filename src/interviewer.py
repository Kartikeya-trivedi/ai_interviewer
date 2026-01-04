"""
Core interviewer module for the AI Interviewer System.
Handles interview logic and question management.
"""

import platform
from typing import List, Dict, Any


class AIInterviewer:
    """Main AI Interviewer class that manages interview sessions."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the AI Interviewer.
        
        Args:
            config: Configuration dictionary for the interviewer
        """
        self.config = config or {}
        self.platform = platform.system()
        self.questions = []
        self.responses = []
        
    def get_platform_info(self) -> Dict[str, str]:
        """
        Get current platform information.
        
        Returns:
            Dictionary containing platform details
        """
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
    
    def is_supported_platform(self) -> bool:
        """
        Check if the current platform is supported (Windows or Linux).
        
        Returns:
            True if platform is Windows or Linux, False otherwise
        """
        return self.platform in ["Windows", "Linux"]
    
    def add_question(self, question: str) -> None:
        """
        Add a question to the interview queue.
        
        Args:
            question: The question text to add
        """
        self.questions.append(question)
    
    def record_response(self, response: str) -> None:
        """
        Record a response from the interviewee.
        
        Args:
            response: The response text
        """
        self.responses.append(response)
    
    def get_interview_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the interview session.
        
        Returns:
            Dictionary containing interview summary
        """
        return {
            "platform": self.platform,
            "total_questions": len(self.questions),
            "total_responses": len(self.responses),
            "questions": self.questions,
            "responses": self.responses
        }
    
    def start_interview(self) -> None:
        """Start the interview session."""
        print(f"Starting AI Interview on {self.platform}")
        print(f"Platform supported: {self.is_supported_platform()}")
    
    def end_interview(self) -> None:
        """End the interview session."""
        summary = self.get_interview_summary()
        print(f"\nInterview completed!")
        print(f"Total questions asked: {summary['total_questions']}")
        print(f"Total responses recorded: {summary['total_responses']}")
