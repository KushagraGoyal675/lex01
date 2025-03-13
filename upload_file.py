import json


def load_case_file(file_path):
    """
    Loads and parses a courtroom case file from JSON.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            case_data = json.load(file)
        return case_data
    except Exception as e:
        print(f"⚠ Error loading case file: {e}")
        return None


def extract_case_details(case_data):
    """
    Extracts structured case details from JSON.
    """
    case_details = {
        "case_title": case_data.get("case_title", "Unknown Case"),
        "court": case_data.get("court", "Unknown Court"),
        "judge": case_data.get("judgment_by", "Unknown Judge"),
        "appellant": case_data["parties"]["appellant"]["name"],
        "respondents": [resp["name"] for resp in case_data["parties"]["respondents"]],
        "contract_purpose": case_data["contract_details"].get("contract_purpose", "N/A"),
        "legal_references": {
            "laws_cited": case_data["legal_references"].get("laws_cited", []),
            "precedents": case_data["legal_references"].get("precedents", [])
        },
        "key_arguments": {
            "appellant": case_data["key_arguments"].get("appellant", "N/A"),
            "respondent": case_data["key_arguments"].get("respondent", "N/A")
        },
        "court_decision": case_data["judgment_summary"].get("court_decision", "No decision recorded"),
        "final_award": case_data["judgment_summary"].get("final_award", "No award specified")
    }
    return case_details


# Example Usage
if __name__ == "__main__":
    case_file_path = "data/case_data.json"  # Ensure the correct JSON file path
    case_data = load_case_file(case_file_path)

    if case_data:
        structured_case = extract_case_details(case_data)
        print("\n📌 **Case Details Extracted Successfully:**")
        print(json.dumps(structured_case, indent=4))
