import os
import groq
from dotenv import load_dotenv
from utils import remove_chain_of_thought

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("API key missing. Set GROQ_API_KEY in your .env file.")

client = groq.Client(api_key=API_KEY)

class CourtAgent:
    """AI-Powered Courtroom Agent."""
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def respond(self, message, additional_info=None):
        """Generates an AI response considering legal context."""
        prompt = (
            f"You are {self.role} named {self.name}. "
            f"Analyze the legal argument carefully and respond with precision.\n"
            f"Argument: {message}"
        )
        if additional_info:
            prompt += f"\nAdditional Info: {additional_info}"

        try:
            response = client.chat.completions.create(
                model="deepseek-r1-distill-llama-70b",
                messages=[{"role": "system", "content": prompt}]
            )
            raw_response = response.choices[0].message.content
            final_response = remove_chain_of_thought(raw_response)
            return final_response
        except Exception as e:
            print(f"Error: {e}")
            return "AI failed to generate a response."
