"""LinkedIn service for fetching profile data and company connections."""

import os
from linkedin_api import Linkedin
from linkedin_api.client import ChallengeException

class LinkedInService:
    """Handles all LinkedIn API operations."""
    
    def __init__(self):
        """Initialize the LinkedIn service with credentials."""
        self.api = None
        self.mock_mode = True  # For now, we'll use mock data for testing
        
        username = os.getenv('LINKEDIN_USERNAME')
        password = os.getenv('LINKEDIN_PASSWORD')
        if not username or not password:
            raise ValueError("LinkedIn credentials not found in environment variables")
            
        if not self.mock_mode:
            try:
                self.api = Linkedin(username, password)
            except ChallengeException:
                print("LinkedIn security challenge detected. Using mock data for testing.")
            except Exception as e:
                print(f"Error authenticating with LinkedIn: {str(e)}")
    
    def get_profile_data(self):
        """Get the user's LinkedIn profile data."""
        if self.mock_mode:
            return self._get_mock_profile_data()
            
        try:
            profile = self.api.get_profile('me')
            experience = self.api.get_profile_experience('me')
            skills = self.api.get_profile_skills('me')
            
            return {
                'summary': profile.get('summary', ''),
                'experience': [
                    {
                        'title': exp.get('title', ''),
                        'company': exp.get('companyName', ''),
                        'duration': exp.get('timePeriod', {}).get('duration', ''),
                        'description': exp.get('description', '')
                    }
                    for exp in experience
                ],
                'skills': [skill.get('name', '') for skill in skills],
                'recommendations': self._get_recommendations()
            }
        except Exception as e:
            print(f"Error fetching LinkedIn profile data: {str(e)}")
            return self._get_mock_profile_data()
    
    def _get_recommendations(self):
        """Get recommendations from the user's profile."""
        if self.mock_mode:
            return self._get_mock_recommendations()
            
        try:
            recommendations = self.api.get_profile_recommendations('me')
            return [
                {
                    'text': rec.get('recommendationText', ''),
                    'author': f"{rec.get('recommender', {}).get('firstName', '')} {rec.get('recommender', {}).get('lastName', '')}"
                }
                for rec in recommendations
            ]
        except Exception as e:
            print(f"Error fetching recommendations: {str(e)}")
            return []
    
    def find_company_connections(self, company_name):
        """Find user's connections at a specific company."""
        if self.mock_mode:
            return self._get_mock_connections(company_name)
            
        try:
            search_results = self.api.search_people(
                keywords=company_name,
                connection_of='me',
                current_company=True
            )
            
            connections = []
            for result in search_results:
                profile = self.api.get_profile(result['public_id'])
                connections.append({
                    'name': f"{profile.get('firstName', '')} {profile.get('lastName', '')}",
                    'title': profile.get('headline', '')
                })
            
            return connections
        except Exception as e:
            print(f"Error searching for company connections: {str(e)}")
            return []
    
    def _get_mock_profile_data(self):
        """Return mock profile data for testing."""
        return {
            'summary': 'Experienced software engineer passionate about building innovative solutions.',
            'experience': [
                {
                    'title': 'Senior Software Engineer',
                    'company': 'Tech Corp',
                    'duration': '3 years',
                    'description': 'Led development of cloud-based applications.'
                },
                {
                    'title': 'Software Developer',
                    'company': 'StartUp Inc',
                    'duration': '2 years',
                    'description': 'Full-stack development of web applications.'
                }
            ],
            'skills': [
                'Python',
                'JavaScript',
                'React',
                'Cloud Computing',
                'System Design'
            ],
            'recommendations': self._get_mock_recommendations()
        }
    
    def _get_mock_recommendations(self):
        """Return mock recommendations for testing."""
        return [
            {
                'text': 'An exceptional engineer who consistently delivers high-quality work.',
                'author': 'Jane Smith'
            },
            {
                'text': 'Great team player with strong problem-solving skills.',
                'author': 'John Doe'
            }
        ]
    
    def _get_mock_connections(self, company_name):
        """Return mock connections for testing."""
        return [
            {
                'name': 'Alice Johnson',
                'title': f'Product Manager at {company_name}'
            },
            {
                'name': 'Bob Wilson',
                'title': f'Software Engineer at {company_name}'
            }
        ]
