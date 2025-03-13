import os
import json
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define Groq API Endpoint
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

def load_case_details(json_path):
    """Loads case details from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def generate_speech(speech_type, role, case_facts):
    """
    Uses Groq LLM to generate AI-powered Opening or Closing Statements.
    """
    try:
        prompt = f"""
        You are a {role} presenting a {speech_type} statement in a courtroom. 
        The statement should be persuasive, logical, and legally sound.

        **Case Facts:**
        {case_facts}

        Deliver a strong {speech_type} argument considering these facts.
        """

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama3-8b-8192",  # Adjust model based on availability
            "messages": [{"role": "system", "content": prompt}],
            "temperature": 0.5
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            return "⚠ No valid response from AI."

    except Exception as e:
        return f"⚠ Error generating speech: {str(e)}"

# Example Usage
if __name__ == "__main__":
    case_file_path = "data/case_data.json"
    case_data = load_case_details(case_file_path)

    # Extract key facts for better AI reasoning
    case_facts = {
        "title": case_data["case_title"],
        "court": case_data["court"],
        "arguments": case_data["key_arguments"],
        "precedents": case_data["legal_references"]["precedents"]
    }

    print("\n📌 **Courtroom AI Speech Simulation**\n")

    # Generate statements
    opening_prosecutor = generate_speech("Opening", "Prosecutor", case_facts)
    opening_defense = generate_speech("Opening", "Defense Attorney", case_facts)
    closing_prosecutor = generate_speech("Closing", "Prosecutor", case_facts)
    closing_defense = generate_speech("Closing", "Defense Attorney", case_facts)

    print("\n🔹 **Prosecutor's Opening Statement:**\n", opening_prosecutor)
    print("\n🔹 **Defense Attorney's Opening Statement:**\n", opening_defense)
    print("\n🔹 **Prosecutor's Closing Statement:**\n", closing_prosecutor)
    print("\n🔹 **Defense Attorney's Closing Statement:**\n", closing_defense)
