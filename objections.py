import os
import json
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Define Groq API Endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # ✅ Correct



def load_case_details(json_path):
    """Loads case details from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def detect_objections(statement, case_facts):
    """
    Uses Groq LLM to detect if a courtroom statement is objectionable, considering the case context.
    """
    try:
        prompt = f"""
        You are a legal expert skilled in courtroom objections.
        Analyze the following courtroom statement in the context of this case:

        **Statement:** "{statement}"
        **Case Facts:** {case_facts}

        Instructions:
        1. Should an objection be raised? (Yes/No)
        2. If yes, what is the best objection type? (Hearsay, Leading, Relevance, Speculation, etc.)?
        3. Provide a legal explanation based on case law.
        4. If the judge were to rule on the objection, should it be "Sustained" or "Overruled"? Provide a reason.
        """

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mixtral-8x7b-32768",  # More advanced model for legal reasoning
            "messages": [{"role": "system", "content": prompt}],
            "temperature": 0.3
        }

        response = requests.post(GROQ_API_URL, headers=headers, json=payload)

        # ✅ Debugging: Print API Response Status
        if response.status_code != 200:
            print(f"⚠ Error: API returned status code {response.status_code}")
            print("🔍 API Response:", response.text)
            return f"⚠ Error {response.status_code}: {response.text}"

        response_data = response.json()

        # ✅ Debugging: Print API Response
        print("\n🔍 Raw API Response:", json.dumps(response_data, indent=4))

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            return "⚠ AI did not generate a valid objection analysis."

    except requests.exceptions.RequestException as req_err:
        return f"⚠ Network error: {str(req_err)}"
    except Exception as e:
        return f"⚠ Unexpected error: {str(e)}"


def handle_objection(opposing_agent, objection_response):
    """
    Handles an objection using AI's judgment.
    """
    print(f"⚖️ {opposing_agent} raises an objection!")
    print(f"🔹 AI Objection Analysis:\n{objection_response}")

    if "Sustained" in objection_response:
        return "Judge: Sustained (Objection upheld)"
    elif "Overruled" in objection_response:
        return "Judge: Overruled (Proceed with questioning)"
    else:
        return "Judge: No clear ruling provided by AI."


# Example Usage
if __name__ == "__main__":
    case_file_path = "data/case_data.json"
    case_data = load_case_details(case_file_path)

    # Extract key facts for better AI reasoning
    case_facts = {
        "title": case_data["case_title"],
        "arguments": case_data.get("key_arguments") or case_data.get("legal_arguments",{}),
        "precedents": case_data["legal_references"]["precedents"]
    }

    statement = input("Enter a courtroom statement: ")
    objection_response = detect_objections(statement, case_facts)

    ruling = handle_objection("Defense Attorney", objection_response)
    print("\n🔹 Judge's Ruling:\n", ruling)
