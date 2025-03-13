import os
import json
import requests
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

def generate_verdict(case_facts, prosecution_strategy, defense_strategy, legal_references):
    """
    AI-Judge generates a final verdict.
    """
    try:
        prompt = f"""
        You are an AI-Judge ruling on a legal case.

        **Case Facts:**
        {case_facts}

        **Prosecution Argument:**
        {prosecution_strategy}

        **Defense Argument:**
        {defense_strategy}

        **Legal References (Laws & Precedents):**
        {legal_references}

        **Judge Instructions:**
        - Consider the **Burden of Proof** for both sides.
        - Provide a detailed verdict with legal justification.
        - Reference any applicable legal precedents from the case.

        Deliver your verdict in a formal court ruling format.
        """

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.5
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠ Error generating verdict: {str(e)}"

# Example Usage
if __name__ == "__main__":
    case_file_path = "case_data.json"
    case_data = load_case_details(case_file_path)

    # Extract structured case details
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

    # Placeholder strategies (In full simulation, these should be AI-generated)
    prosecution_strategy = "Prosecution argues that the appellant breached the contract by failing to meet obligations."
    defense_strategy = "Defense argues that unforeseen circumstances justified the contract delays."

    print("\n📌 **AI-Judge Court Verdict Simulation**\n")

    # Generate AI Judge's Verdict
    verdict = generate_verdict(case_facts, prosecution_strategy, defense_strategy, legal_references)

    print("\n🔹 **Final Verdict:**\n", verdict)
