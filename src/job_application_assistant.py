"""Main class for the Job Application Assistant."""

import os
from datetime import datetime
from .google_drive_service import GoogleDriveService
from .openai_service import OpenAIService

class JobApplicationAssistant:
    """A class to help generate customized cover letters based on job descriptions."""
    
    def __init__(self):
        """Initialize the JobApplicationAssistant with necessary services."""
        self.google_drive = GoogleDriveService()
        self.openai = OpenAIService()
    
    def generate_application_documents(self, job_description):
        """Main function to generate and save customized application documents."""
        # Analyze the job description
        print("\nAnalyzing job description...")
        analysis = self.openai.analyze_job_description(job_description)
        print(f"\nJob Requirements Analysis:\n{analysis}")
        
        # Download reference documents
        print("\nDownloading your reference documents from Google Drive...")
        resume_content = self.google_drive.download_file(os.getenv('RESUME_FILE_ID'))
        original_letter = self.google_drive.download_file(os.getenv('COVER_LETTER_FILE_ID'))
        
        if not resume_content or not original_letter:
            print("Error: Could not download reference documents")
            return
        
        # Generate new cover letter
        print("\nGenerating new cover letter...")
        cover_letter = self.openai.generate_cover_letter(
            job_description, resume_content, original_letter
        )
        
        # Save to Google Drive
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        drive_title = f"Generated Cover Letter - {timestamp}"
        file_id = self.google_drive.save_document(cover_letter, drive_title)
        print(f"\nCover letter saved to Google Drive:")
        print(f"Title: {drive_title}")
        print(f"Document Link: https://docs.google.com/document/d/{file_id}/edit")
        
        print("\nDone! Your new cover letter has been generated and saved.")
