#!/usr/bin/env python3
"""
AI Interviewer System - Command Line Interface
Main entry point for the AI interviewer application.
"""

import sys
import platform
from typing import Optional

try:
    import click
except ImportError:
    # Provide fallback if click is not installed
    click = None

from src.interviewer import AIInterviewer


def main_without_click():
    """Fallback main function without click dependency."""
    print("=" * 60)
    print("AI Interviewer System v0.1.0")
    print("Cross-platform AI Interview Application")
    print("=" * 60)
    print()
    
    # Initialize interviewer
    interviewer = AIInterviewer()
    
    # Display platform info
    platform_info = interviewer.get_platform_info()
    print("Platform Information:")
    print(f"  System: {platform_info['system']}")
    print(f"  Release: {platform_info['release']}")
    print(f"  Machine: {platform_info['machine']}")
    print()
    
    # Check platform support
    if not interviewer.is_supported_platform():
        print(f"WARNING: Your platform ({platform_info['system']}) may not be fully supported.")
        print("Supported platforms: Windows, Linux")
        print()
    else:
        print(f"✓ Platform {platform_info['system']} is supported!")
        print()
    
    # Start interview
    interviewer.start_interview()
    print()
    
    # Demo: Add some sample questions
    print("Demo Mode: Adding sample interview questions...")
    interviewer.add_question("Tell me about yourself.")
    interviewer.add_question("What are your strengths?")
    interviewer.add_question("Where do you see yourself in 5 years?")
    
    print(f"Added {len(interviewer.questions)} sample questions.")
    print()
    
    # Display questions
    print("Interview Questions:")
    for i, question in enumerate(interviewer.questions, 1):
        print(f"  {i}. {question}")
    print()
    
    # End interview
    interviewer.end_interview()
    print()
    print("Thank you for using AI Interviewer System!")


def main_with_click():
    """Main function using click for CLI."""
    @click.command()
    @click.option('--demo', is_flag=True, help='Run in demo mode')
    @click.option('--info', is_flag=True, help='Show platform information')
    @click.version_option(version='0.1.0')
    def cli(demo: bool, info: bool):
        """AI Interviewer System - Cross-platform interview application."""
        print("=" * 60)
        print("AI Interviewer System v0.1.0")
        print("Cross-platform AI Interview Application")
        print("=" * 60)
        print()
        
        interviewer = AIInterviewer()
        
        if info:
            platform_info = interviewer.get_platform_info()
            print("Platform Information:")
            for key, value in platform_info.items():
                print(f"  {key.capitalize()}: {value}")
            print()
            print(f"Supported: {interviewer.is_supported_platform()}")
            return
        
        if demo:
            main_without_click()
            return
        
        print("Use --demo flag to run a demonstration")
        print("Use --info flag to see platform information")
        print("Use --help for more options")
    
    cli()


def main():
    """Main entry point with fallback support."""
    if click is not None:
        main_with_click()
    else:
        main_without_click()


if __name__ == "__main__":
    main()
