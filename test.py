import json

with open("data/case_data.json", "r", encoding="utf-8") as f:
    case_data = json.load(f)

print("\n🔍 Checking JSON Structure:")
print(json.dumps(case_data, indent=4))  # Prints full JSON to check if "legal_references" exists

print("\n🔍 Checking `legal_references` Section:")
print(json.dumps(case_data.get("legal_references", {}), indent=4))  # Prints only legal references
