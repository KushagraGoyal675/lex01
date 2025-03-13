import json

class CourtRole:
    """
    Represents a courtroom role (Judge, Prosecutor, Defense, Witness, etc.).
    """
    def __init__(self, name, role_type):
        self.name = name
        self.role_type = role_type
        self.personality = self.assign_personality()

    def assign_personality(self):
        """
        Assigns a specific personality type based on the role.
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
        return f"{self.name}, serving as the {self.role_type}. Personality: {self.personality}"

def assign_roles(case_data):
    """
    Dynamically assigns courtroom roles based on case_data.json format.
    """
    return {
        "Judge": CourtRole(case_data["judgment_by"], "Judge"),
        "Appellant": CourtRole(case_data["parties"]["appellant"]["name"], "Appellant"),
        "Respondents": [CourtRole(r["name"], "Respondent") for r in case_data["parties"]["respondents"]],
        "Witnesses": [CourtRole(w, "Witness") for w in case_data.get("witnesses", [])]
    }

# Example Usage:
if __name__ == "__main__":
    case_file_path = "data/case_data.json"

    def load_case_file(file_path):
        """Loads case data from JSON file."""
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    case_data = load_case_file(case_file_path)

    if case_data:
        assigned_roles = assign_roles(case_data)

        print("\n📌 Courtroom Roles Assigned:\n")
        for role, persons in assigned_roles.items():
            if isinstance(persons, list):  # Multiple respondents or witnesses
                for person in persons:
                    print(person.introduce())
            else:
                print(persons.introduce())
