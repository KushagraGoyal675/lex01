import json

class CourtRole:
    """
    Represents a courtroom role (Judge, Appellant, Respondent, Witness, etc.).
    """
    def __init__(self, name="Unknown", role_type="Unknown"):
        self.name = name
        self.role_type = role_type
        self.personality = self.assign_personality()

    def assign_personality(self):
        """
        Assigns a personality type based on the courtroom role.
        """
        personalities = {
            "Judge": "Neutral, logical, authoritative",
            "Appellant": "Determined, fact-driven, persistent",
            "Respondent": "Defensive, strategic, argument-driven",
            "Witness": "Observational, fact-based, supportive"
        }
        return personalities.get(self.role_type, "Neutral")

    def introduce(self):
        """
        Introduces the role in a courtroom setting.
        """
        return f"{self.name} is serving as the {self.role_type}. Personality: {self.personality}"

def assign_roles(case_data):
    """
    Dynamically assigns courtroom roles based on JSON case data.
    """

    # Identify the Appellant's key (could be 'appellant', 'petitioner', or 'plaintiff')
    appellant_key = next((key for key in ["appellant", "petitioner", "plaintiff"] if key in case_data.get("parties", {})), None)
    if not appellant_key:
        raise KeyError("❌ No valid appellant (petitioner/plaintiff) found in the case file.")

    # Assign roles
    return {
        "Judge": CourtRole(case_data.get("judgment_by", "Honorable Judge"), "Judge"),
        "Appellant": CourtRole(case_data["parties"][appellant_key].get("name", "Unknown Appellant"), "Appellant"),
        "Respondents": [
            CourtRole(resp.get("name", "Unknown Respondent"), "Respondent")
            for resp in case_data.get("parties", {}).get("respondents", [])
        ],
        "Witnesses": [
            CourtRole(witness, "Witness") for witness in case_data.get("witnesses", [])
        ]
    }

# Example Usage
if __name__ == "__main__":
    case_file_path = "data/case_data.json"

    def load_case_file(file_path):
        """Loads case data from JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Error loading case file: {e}")
            return {}

    case_data = load_case_file(case_file_path)

    if case_data:
        assigned_roles = assign_roles(case_data)

        print("\n📌 Courtroom Roles Assigned:\n")
        print(assigned_roles["Judge"].introduce())
        print(assigned_roles["Appellant"].introduce())

        if assigned_roles["Respondents"]:
            print("\n👥 Respondents:")
            for respondent in assigned_roles["Respondents"]:
                print(f"   - {respondent.introduce()}")

        if assigned_roles["Witnesses"]:
            print("\n👀 Witnesses:")
            for witness in assigned_roles["Witnesses"]:
                print(f"   - {witness.introduce()}")
