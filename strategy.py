import os
import json
from dotenv import load_dotenv
import groq

# Load API Key from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set up Groq API client
client = groq.Client(api_key=GROQ_API_KEY)

def load_case_details(json_path):
    """Loads case details from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def suggest_strategy(role, case_facts, legal_references):
    """
    Uses Groq API (llama3-8b-8192) to generate courtroom strategies.
    """
    try:
        prompt = f"""
        You are a skilled {role} preparing a courtroom strategy.

        **Case Facts:**
        {case_facts}

        **Legal References (Precedents & Laws Cited):**
        {legal_references}

        Provide a well-structured, legally strong strategy that includes:
        1️⃣ Key arguments based on legal principles.
        2️⃣ How to counter the opposing side.
        3️⃣ Real-world case examples to support your position.
        """

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠ Error generating strategy: {str(e)}"

# Example Usage
if __name__ == "__main__":
    case_file_path = "data/case_data.json"
    case_data = load_case_details(case_file_path)

    # Extract necessary data
    case_facts = {
        "title": case_data["case_title"],
        "arguments": case_data["key_arguments"],
        "contract_purpose": case_data["contract_details"]["contract_purpose"],
        "court_decision": case_data["judgment_summary"]["court_decision"]
    }

    legal_references = {
        "laws_cited": case_data["legal_references"]["laws_cited"],
        "precedents": case_data["legal_references"]["precedents"]
    }

    print("\n📌 **AI-Generated Courtroom Strategies**\n")

    # Generate strategies
    prosecution_strategy = suggest_strategy("Prosecutor", case_facts, legal_references)
    defense_strategy = suggest_strategy("Defense Attorney", case_facts, legal_references)

    print("\n🔹 **Prosecution Strategy:**\n", prosecution_strategy)
    print("\n🔹 **Defense Strategy:**\n", defense_strategy)
