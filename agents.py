import json
import time


class CourtAgent:
    """Base class for all courtroom agents with AI-driven responses."""

    def __init__(self, name, role, model):
        self.name = name
        self.role = role
        self.model = model  # AI model for generating responses

    def introduce(self):
        return f"My name is {self.name}, and I am the {self.role} in this case."

    def generate_response(self, phase, case_facts):
        """Uses AI to generate a response based on the phase and case details."""
        prompt = f"""
        You are {self.role} named {self.name}.
        You are currently in the {phase} phase of a courtroom case.

        Case Title: {case_facts['title']}
        Key Arguments: {json.dumps(case_facts['arguments'], indent=2)}

        Generate a response appropriate for this phase.
        """
        return self.model.generate_text(prompt)


class Judge(CourtAgent):
    """AI-powered Judge agent."""

    def __init__(self, name, model):
        super().__init__(name, "Judge", model)

    def give_ruling(self, verdict):
        return f"As the Judge, I have reached the verdict: {verdict}"

    def comment(self, case_facts):
        return self.generate_response("judge_commentary", case_facts)


class Party(CourtAgent):
    """AI-powered party (Appellant/Respondent)."""

    def __init__(self, name, role, arguments, model):
        super().__init__(name, role, model)
        self.arguments = arguments

    def present_arguments(self, case_facts):
        return self.generate_response("arguments", case_facts)


class Witness(CourtAgent):
    """AI-powered witness with dynamic testimony."""

    def __init__(self, name, testimony, model):
        super().__init__(name, "Witness", model)
        self.testimony = testimony

    def give_testimony(self, case_facts):
        return self.generate_response("witness_testimony", case_facts)
