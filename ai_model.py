import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


class AIModel:
    """AI Model class to generate courtroom responses using Groq API."""

    def __init__(self):
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing! Please check your .env file.")

    def generate_text(self, prompt):
        """Calls the Groq API to generate AI responses."""
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mixtral-8x7b-32768",
            "messages": [{"role": "system", "content": prompt}],
            "temperature": 0.5
        }
        try:
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)
            if response.status_code != 200:
                print(f"⚠ Error: API returned status code {response.status_code}")
                print("🔍 API Response:", response.text)
                return f"Error: {response.status_code} {response.text}"
            data = response.json()
            return data["choices"][0]["message"][
                "content"].strip() if "choices" in data else "No valid response from AI."
        except Exception as e:
            return f"Unexpected error: {str(e)}"
