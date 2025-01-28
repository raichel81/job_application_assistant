from main import JobApplicationAssistant
import os

def test_job_assistant():
    print("Initializing Job Application Assistant...")
    assistant = JobApplicationAssistant()
    
    # Test listing files
    print("\nListing files in Google Drive...")
    try:
        files = assistant.drive_service.files().list(
            q="mimeType='application/vnd.google-apps.document'",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        for file in files.get('files', []):
            print(f"Found file: {file.get('name')} ({file.get('id')})")
    except Exception as e:
        print(f"Error listing files: {e}")
        return
    
    # Test job description
    job_description = """
    Software Engineer - Full Stack
    
    We are seeking a Full Stack Software Engineer to join our team. 
    The ideal candidate will have:
    - Experience with Python and web frameworks (Django/Flask)
    - Strong understanding of front-end technologies (HTML, CSS, JavaScript)
    - Experience with databases and SQL
    - Good communication and collaboration skills
    - Ability to write clean, maintainable code
    
    Responsibilities:
    - Develop and maintain web applications
    - Work with cross-functional teams
    - Write well-documented, reusable code
    - Participate in code reviews
    """
    
    # Create output directory
    output_dir = "test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\nGenerating customized documents for the job description...")
    assistant.generate_application_documents(job_description, output_dir)

if __name__ == "__main__":
    test_job_assistant()
