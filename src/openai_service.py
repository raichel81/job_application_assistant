"""OpenAI service for generating and analyzing content."""

import os
from openai import OpenAI

class OpenAIService:
    """Handles all OpenAI API operations for content generation and analysis."""
    
    def __init__(self):
        """Initialize the OpenAI service with API key."""
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def analyze_job_description(self, job_description):
        """Analyze a job description using OpenAI to extract key requirements."""
        prompt = f"""
        Analyze this job description and provide key requirements and focus areas:
        
        {job_description}
        
        Please format the response as:
        Key Requirements:
        - [requirement 1]
        - [requirement 2]
        ...
        
        Focus Areas:
        - [focus area 1]
        - [focus area 2]
        
        Company Culture & Values:
        - [value 1]
        - [value 2]
        ...
        
        Unique Opportunities:
        - [opportunity 1]
        - [opportunity 2]
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional job application analyst who excels at identifying both technical requirements and cultural aspects of job opportunities."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
    
    def _format_linkedin_data(self, linkedin_data, connections):
        """Format LinkedIn data for the prompt."""
        if not linkedin_data:
            return ""
            
        formatted = "\n\nMy LinkedIn Profile Data:"
        
        # Add professional summary
        if linkedin_data.get('summary'):
            formatted += f"\nProfessional Summary:\n{linkedin_data['summary']}"
        
        # Add experience
        if linkedin_data.get('experience'):
            formatted += "\n\nRelevant Experience:"
            for exp in linkedin_data['experience']:
                formatted += f"\n- {exp['title']} at {exp['company']} ({exp['duration']})"
                if exp['description']:
                    formatted += f"\n  {exp['description']}"
        
        # Add skills
        if linkedin_data.get('skills'):
            formatted += "\n\nKey Skills:\n- " + "\n- ".join(linkedin_data['skills'])
        
        # Add recommendations
        if linkedin_data.get('recommendations'):
            formatted += "\n\nProfessional Recommendations:"
            for rec in linkedin_data['recommendations'][:2]:  # Include top 2 recommendations
                formatted += f"\n\"{rec['text']}\" - {rec['author']}"
        
        # Add connections at the company
        if connections:
            formatted += "\n\nNote: I have professional connections at the company who can speak to the company's culture and values."
        
        return formatted
    
    def generate_cover_letter(self, job_description, resume_content, original_letter, linkedin_data=None, connections=None):
        """Generate a customized cover letter using OpenAI."""
        linkedin_content = self._format_linkedin_data(linkedin_data, connections) if linkedin_data else ""
        
        prompt = f"""
        Create an engaging and personable cover letter based on these inputs:
        
        Job Description:
        {job_description}
        
        My Resume:
        {resume_content}
        
        My Original Cover Letter Style:
        {original_letter}{linkedin_content}
        
        Guidelines:
        1. Start with a compelling opening that shows genuine enthusiasm for the company's mission
        2. Share a brief personal story or insight that demonstrates your alignment with their values
        3. Use a warm, conversational tone while maintaining professionalism
        4. Connect your experience to their needs through specific examples, not just listing skills
        5. Show you've done your research by referencing their work
        6. If there are connections at the company, mention your network there (but don't name-drop without permission)
        7. Use endorsements and recommendations from LinkedIn to support your qualifications
        8. Include a thoughtful closing that reinforces your cultural fit
        9. Keep it concise but memorable
        10. Maintain authenticity - let your personality shine through
        11. Focus on impact and results, not just responsibilities
        
        Remember:
        - This is a conversation starter, not a resume rehash
        - Show enthusiasm and genuine interest in their mission
        - Demonstrate cultural fit while highlighting technical expertise
        - Be authentic and personable
        - If you have connections at the company, subtly indicate your familiarity with their work culture
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer who excels at creating engaging, personable letters that stand out while maintaining professionalism."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
