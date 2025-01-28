# Job Application Assistant

An intelligent assistant that helps generate personalized, engaging cover letters based on job descriptions using GPT-4 and Google Drive integration.

## Features
- Analyzes job descriptions to identify:
  - Key technical requirements
  - Focus areas
  - Company culture & values
  - Unique opportunities
- Generates engaging, personalized cover letters that:
  - Show genuine enthusiasm for the company's mission
  - Share relevant personal insights
  - Connect your experience through specific examples
  - Maintain a warm yet professional tone
- Seamlessly integrates with Google Drive for document management:
  - Supports both Google Docs and Microsoft Word (.docx) formats
  - Automatically converts documents to proper format
  - Saves generated cover letters as Google Docs for easy editing
- Uses GPT-4 for high-quality, nuanced content generation

## Setup
1. Create a `.env` file with your API credentials:
   ```
   OPENAI_API_KEY=your_openai_key
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   RESUME_FILE_ID=your_resume_google_doc_id
   COVER_LETTER_FILE_ID=your_cover_letter_google_doc_id
   ```
   A template file `.env.example` is provided for reference. Copy it to create your `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then replace the placeholder values with your actual credentials.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Upload your reference documents to Google Drive:
   - Resume: Can be either a Google Doc or Microsoft Word (.docx) file
   - Sample Cover Letter: Can be either a Google Doc or Microsoft Word (.docx) file
   - Note the file IDs from Google Drive URLs and add them to the `.env` file
   - Example file ID from URL: For `https://docs.google.com/document/d/FILE_ID/edit`, use `FILE_ID`

## Usage

### Generate a cover letter from a file:
```bash
python main.py -f path/to/job_listing.txt
```

### Generate a cover letter by pasting the description:
```bash
python main.py
```
Then paste the job description and press Ctrl+Z (Windows) or Ctrl+D (Unix) followed by Enter.

### List available Google Drive files:
```bash
python main.py -l
```
This will show your configured resume and cover letter files, along with their formats.

## Output
The generated cover letter will be:
1. Saved directly to your Google Drive as a Google Doc
2. Accessible via a Google Docs link provided in the output
3. Ready for immediate editing and sharing

## Project Structure
```
job_application_assistant/
├── main.py                    # CLI interface
├── src/
│   ├── job_application_assistant.py  # Main application logic
│   ├── google_drive_service.py       # Google Drive integration
│   └── openai_service.py            # OpenAI/GPT-4 integration
├── requirements.txt           # Project dependencies
└── .env                      # API keys and configuration
```

## Dependencies
- openai - For GPT-4 integration
- google-api-python-client - For Google Drive API
- google-auth-oauthlib - For Google OAuth authentication
- python-docx - For handling Microsoft Word documents
- python-dotenv - For environment variable management

## Future Goals
- LinkedIn Integration:
  - Pull professional experience directly from LinkedIn profile
  - Use endorsements and recommendations for more personalized content
  - Analyze connection network for potential referrals
- Enhanced AI Features:
  - Company research integration to reference recent news and achievements
  - Industry-specific cover letter templates and styles
  - Automatic tailoring based on company culture (startup vs. enterprise)
- Resume Enhancement:
  - Automatic resume tailoring based on job requirements
  - Skills gap analysis with suggestions for improvement
  - ATS (Applicant Tracking System) optimization
- User Interface:
  - Web interface for easier document management
  - Real-time editing and preview
  - Job application tracking and status management
- Collaboration Features:
  - Share and get feedback on generated documents
  - Community-driven templates and examples
  - Integration with job search platforms

Want to contribute? Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests for improvements
- Share your templates or enhancement ideas
- Help with documentation or testing
