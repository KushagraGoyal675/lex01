import openai
from dotenv import load_dotenv
import os
import json

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
openai.api_key = GROQ_API_KEY

def load_case_file(file_path):
    """Loads case data from JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def extract_case_details(case_data):
    """Extracts structured case details from JSON."""
    case_facts = {
        "title": case_data["case_title"],
        "court": case_data["court"],
        "date": case_data["date"],
        "contract_purpose": case_data["contract_details"]["contract_purpose"],
        "arguments": case_data.get("key_arguments") or case_data.get("legal_arguments",{}),
        "final_award": case_data["judgment_summary"]["final_award"]
    }

    # No explicit witnesses in JSON, so assume none unless added later
    witnesses = []  # If witness data is included in the JSON, update this

    return {"case_facts": case_facts, "witnesses": witnesses}

def generate_cross_examination(witness_name, witness_statement, case_facts):
    """
    Generates AI-powered cross-examination questions.
    """
    prompt = f"""
    You are a courtroom lawyer cross-examining the witness: {witness_name}.
    Their testimony: "{witness_statement}"

    Based on the case facts: {case_facts}, generate:
    - 3 strong cross-examination questions to challenge inconsistencies.
    - A possible follow-up if the witness contradicts themselves.
    """

    response = openai.ChatCompletion.create(
        model="deepseek-r1-distill-llama-7b",
        messages=[{"role": "system", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Example Usage:
if __name__ == "__main__":
    case_file_path = "data/case_data.json"
    case_data = load_case_file(case_file_path)

    if case_data:
        structured_case = extract_case_details(case_data)

        if structured_case["witnesses"]:  # Proceed only if witnesses exist
            for witness in structured_case["witnesses"]:
                witness_statement = f"Witness {witness} claims they saw the defendant at the scene."
                cross_exam = generate_cross_examination(witness, witness_statement, structured_case["case_facts"])
                print(f"\n🔹 Cross-Examination for {witness}:\n", cross_exam)
        else:
            print("⚠ No witness data found in the case file.")
