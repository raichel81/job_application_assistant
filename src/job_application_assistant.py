"""Main class for the Job Application Assistant."""

import os
from datetime import datetime
from .google_drive_service import GoogleDriveService
from .openai_service import OpenAIService
from .linkedin_service import LinkedInService

class JobApplicationAssistant:
    """Handles the job application document generation process."""
    
    def __init__(self):
        """Initialize the job application assistant with required services."""
        self.drive_service = GoogleDriveService()
        self.openai = OpenAIService()
        try:
            self.linkedin = LinkedInService()
            self.linkedin_enabled = True
        except ValueError:
            print("LinkedIn credentials not found. LinkedIn features will be disabled.")
            self.linkedin_enabled = False
    
    def generate_application_documents(self, job_description):
        """Generate application documents based on job description."""
        try:
            # Get reference documents from Google Drive
            resume_id = os.getenv('RESUME_FILE_ID')
            cover_letter_id = os.getenv('COVER_LETTER_FILE_ID')
            
            if not resume_id or not cover_letter_id:
                raise ValueError("Resume or cover letter ID not found in environment variables")
            
            resume_content = self.drive_service.download_file(resume_id)
            original_letter = self.drive_service.download_file(cover_letter_id)
            
            # Get LinkedIn data if available
            linkedin_data = None
            company_connections = None
            if self.linkedin_enabled:
                print("Fetching LinkedIn profile data...")
                linkedin_data = self.linkedin.get_profile_data()
                
                # Try to extract company name from job description
                # This is a simple approach - could be enhanced with better parsing
                company_name = self._extract_company_name(job_description)
                if company_name:
                    print(f"Searching for connections at {company_name}...")
                    company_connections = self.linkedin.find_company_connections(company_name)
                    if company_connections:
                        print(f"Found {len(company_connections)} connections at {company_name}")
            
            # Generate customized cover letter
            print("Generating cover letter...")
            cover_letter = self.openai.generate_cover_letter(
                job_description,
                resume_content,
                original_letter,
                linkedin_data,
                company_connections
            )
            
            # Save the new cover letter
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"Cover_Letter_{timestamp}"
            
            print(f"Saving cover letter as {new_filename}...")
            file_id = self.drive_service.save_document(cover_letter, new_filename)
            print(f"Cover letter saved with ID: {file_id}")
            
            print("Cover letter generated successfully!")
            return True
            
        except Exception as e:
            print(f"Error generating application documents: {str(e)}")
            return False
    
    def _extract_company_name(self, job_description):
        """Extract company name from job description using OpenAI."""
        try:
            prompt = f"""
            Extract only the company name from this job description. 
            Return ONLY the company name, nothing else:
            
            {job_description}
            """
            
            company_name = self.openai.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts company names from text."},
                    {"role": "user", "content": prompt}
                ]
            ).choices[0].message.content.strip()
            
            return company_name
        except Exception as e:
            print(f"Error extracting company name: {str(e)}")
            return None
