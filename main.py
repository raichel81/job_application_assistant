#!/usr/bin/env python3
"""Command-line interface for the Job Application Assistant."""

import argparse
import os
from dotenv import load_dotenv
from src.job_application_assistant import JobApplicationAssistant

# Load environment variables from .env file
load_dotenv()

def read_job_description(file_path=None):
    """Read job description from file or stdin."""
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    print("Please paste the job description below.")
    print("After pasting, press Enter, then Ctrl+Z (Windows) or Ctrl+D (Unix), then Enter again to finish:")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(lines)

def main():
    """Run the Job Application Assistant CLI."""
    parser = argparse.ArgumentParser(
        description='Generate customized cover letters based on job descriptions'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Path to a file containing the job description'
    )
    
    parser.add_argument(
        '-l', '--list-files',
        action='store_true',
        help='List available files in Google Drive'
    )
    
    args = parser.parse_args()
    
    # Initialize the assistant
    assistant = JobApplicationAssistant()
    
    if args.list_files:
        # List files in Google Drive
        assistant.google_drive.list_files()
    else:
        # Get job description and generate cover letter
        job_description = read_job_description(args.file)
        if job_description.strip():
            assistant.generate_application_documents(job_description)
        else:
            print("Error: No job description provided")

if __name__ == "__main__":
    main()
