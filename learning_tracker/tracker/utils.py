import requests
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


import requests
from .models import Challenge, FieldOfInterest

def suggest_challenges(fields_of_interest):
    # Use Gemini API if available
    api_url = "https://api.gemini.com/v1/suggest"
    api_key = os.getenv("GEMINI_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"fields_of_interest": [field.name for field in fields_of_interest]}
    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return [Challenge.objects.get(name=challenge) for challenge in data['challenges']]
    else:
        # Fallback: Use predefined relationships from the database
        suggested_challenges = []
        for field in fields_of_interest:
            suggested_challenges.extend(field.challenges.all())
        return list(set(suggested_challenges))[:15]  # Return up to 15 unique challenges