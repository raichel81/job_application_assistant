"""Google Drive service for handling file operations."""

import os
import io
import pickle
from docx import Document
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

class GoogleDriveService:
    """Handles all Google Drive operations including authentication and file management."""
    
    def __init__(self):
        """Initialize the Google Drive service with OAuth2 authentication."""
        self.drive_service = self._setup_google_drive()
    
    def _setup_google_drive(self):
        """Set up and authenticate Google Drive API service."""
        SCOPES = [
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/drive.file'
        ]
        creds = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                client_config = {
                    "installed": {
                        "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                        "client_secret": os.getenv('GOOGLE_CLIENT_SECRET'),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                    }
                }
                
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('drive', 'v3', credentials=creds)
    
    def download_file(self, file_id):
        """Download and read content from a Google Drive file."""
        try:
            file = self.drive_service.files().get(
                fileId=file_id,
                fields='id, name, mimeType'
            ).execute()
            
            print(f"Found file: {file['name']} ({file['mimeType']})")
            
            if file['mimeType'] == 'application/vnd.google-apps.document':
                request = self.drive_service.files().export_media(
                    fileId=file_id,
                    mimeType='text/plain'
                )
            elif file['mimeType'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                request = self.drive_service.files().get_media(
                    fileId=file_id
                )
            else:
                print(f"Unsupported file type: {file['mimeType']}")
                return None
            
            content = io.BytesIO()
            downloader = MediaIoBaseDownload(content, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
            
            content.seek(0)
            
            if file['mimeType'] == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                doc = Document(content)
                return '\n'.join(paragraph.text for paragraph in doc.paragraphs)
            else:
                return content.read().decode('utf-8')
            
        except Exception as e:
            print(f"An error occurred while downloading the file: {e}")
            return None
    
    def save_document(self, content, title):
        """Save a document to Google Drive."""
        try:
            file_metadata = {
                'name': title,
                'mimeType': 'application/vnd.google-apps.document'
            }
            
            content_bytes = content.encode('utf-8')
            media = MediaIoBaseUpload(
                io.BytesIO(content_bytes),
                mimetype='text/plain',
                resumable=True
            )
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            print(f"\nDocument saved to Google Drive:")
            print(f"Title: {title}")
            print(f"File ID: {file['id']}")
            print(f"Full path: https://docs.google.com/document/d/{file['id']}/edit")
            return file['id']
        except Exception as e:
            print(f"Error saving to Google Drive: {e}")
            return None
    
    def list_files(self):
        """List Google Drive files accessible to the application."""
        try:
            resume_id = os.getenv('RESUME_FILE_ID')
            cover_letter_id = os.getenv('COVER_LETTER_FILE_ID')
            
            print("\nChecking specific files:")
            if resume_id:
                try:
                    file = self.drive_service.files().get(
                        fileId=resume_id,
                        fields='id, name, mimeType'
                    ).execute()
                    print(f"Resume found: {file['name']} ({file['id']})")
                except Exception as e:
                    print(f"Could not access resume: {e}")
            
            if cover_letter_id:
                try:
                    file = self.drive_service.files().get(
                        fileId=cover_letter_id,
                        fields='id, name, mimeType'
                    ).execute()
                    print(f"Cover letter found: {file['name']} ({file['id']})")
                except Exception as e:
                    print(f"Could not access cover letter: {e}")
            
            print("\nListing all accessible documents:")
            results = self.drive_service.files().list(
                pageSize=30,
                fields="nextPageToken, files(id, name, mimeType, owners)",
                q="mimeType='application/vnd.google-apps.document'"
            ).execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                for item in items:
                    print(f"Name: {item['name']}")
                    print(f"ID: {item['id']}")
                    print(f"Type: {item['mimeType']}")
                    if 'owners' in item:
                        print(f"Owner: {item['owners'][0].get('emailAddress', 'Unknown')}")
                    print("---")
            return items
        except Exception as e:
            print(f'An error occurred: {e}')
            return []
