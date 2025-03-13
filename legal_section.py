import json

def load_legal_section(json_path):
    """
    Loads case details from the given JSON file and extracts relevant information.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        case_details = {
            "case_title": data.get("case_title", ""),
            "court": data.get("court", ""),
            "date": data.get("date", ""),
            "judgment_by": data.get("judgment_by", ""),
            "contract_purpose": data.get("contract_details", {}).get("contract_purpose", ""),
            "laws_cited": data.get("legal_references", {}).get("laws_cited", []),
            "precedents": data.get("legal_references", {}).get("precedents", []),
            "arguments": {
                "appellant": data.get("key_arguments", {}).get("appellant", ""),
                "respondent": data.get("key_arguments", {}).get("respondent", "")
            },
            "court_decision": data.get("judgment_summary", {}).get("court_decision", ""),
            "final_award": data.get("judgment_summary", {}).get("final_award", "")
        }

        return case_details

    except Exception as e:
        print(f"⚠ Error loading case details: {e}")
        return None

if __name__ == "__main__":
    case_file_path = "data/case_data.json"
    case_info = load_legal_section(case_file_path)

    if case_info:
        print(json.dumps(case_info, indent=4))
    else:
        print("⚠ Could not load case details.")
