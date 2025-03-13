import json

class CourtAgent:
    """Base class for courtroom agents."""
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def introduce(self):
        return f"My name is {self.name}, and I am the {self.role} in this case."

class Judge(CourtAgent):
    def __init__(self, name):
        super().__init__(name, "Judge")

    def give_ruling(self, verdict):
        return f"As the Judge, I have reached the verdict: {verdict}"

class Party(CourtAgent):
    def __init__(self, name, role, arguments):
        super().__init__(name, role)
        self.arguments = arguments

    def present_arguments(self):
        return f"As {self.role}, my arguments are: {self.arguments}"

class Witness(CourtAgent):
    def __init__(self, name, testimony):
        super().__init__(name, "Witness")
        self.testimony = testimony

    def give_testimony(self):
        return f"My testimony is: {self.testimony}"

def load_case_data(json_file):
    """Load case details from JSON file."""
    with open(json_file, "r") as file:
        return json.load(file)

def simulate_court_case(case_data):
    """Simulate a court case using AI agents."""
    print(f"Case Title: {case_data['case_title']}")
    print(f"Court: {case_data['court']}")
    print(f"Date: {case_data['date']}\n")

    judge = Judge(case_data["judgment_by"])
    appellant = Party(
        case_data["parties"]["appellant"]["name"],
        "Appellant",
        case_data["key_arguments"]["appellant"]
    )
    respondent = Party(
        case_data["parties"]["respondents"][0]["name"],
        "Respondent",
        case_data["key_arguments"]["respondent"]
    )

    print(judge.introduce())
    print(appellant.introduce())
    print(appellant.present_arguments())
    print(respondent.introduce())
    print(respondent.present_arguments())

    print("\nFinal Judgment:")
    print(judge.give_ruling(case_data["judgment_summary"]["court_decision"]))
    print(f"Final Award: {case_data['judgment_summary']['final_award']}")

if __name__ == "__main__":
    case_data = load_case_data("data/case_data.json")
    simulate_court_case(case_data)
