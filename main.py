import time
import json
import os
import requests
from dotenv import load_dotenv
import groq
from agents import CourtAgent
from objections import handle_objection, detect_objections
from roles import assign_roles  # Import correct role extraction
from strategy import suggest_strategy

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set up Groq API client
client = groq.Client(api_key=GROQ_API_KEY)


def build_legal_context(legal_references):
    """Formats legal references for AI reasoning."""
    if not legal_references or not any(legal_references.values()):
        print("⚠ Warning: `legal_references` is empty in `build_legal_context()`")
        return "No legal references found."

    return f"""
    📜 **Legal Context:**
    - **Laws Cited:** {', '.join(legal_references.get('laws_cited', ['None']))}
    - **Precedents Applied:** {', '.join(legal_references.get('precedents', ['None']))}
    """


def load_case_data(case_file):
    """Loads case data from a JSON file."""
    try:
        with open(case_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠ Error: The case file '{case_file}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"⚠ Error: The case file '{case_file}' is not a valid JSON file.")
        return None


def get_user_input(prompt, valid_options=None, default=None):
    """Helper function to get user input with validation."""
    while True:
        user_input = input(prompt).strip().capitalize()
        if valid_options and user_input not in valid_options:
            print(f"❌ Invalid input. Please enter one of: {', '.join(valid_options)}")
            if default:
                print(f"🔹 Defaulting to {default}.")
                return default
            continue
        return user_input


def main():
    """Simulates an interactive courtroom trial with AI agents and user participation."""

    print("\n⚖️ Welcome to the **AI Courtroom Simulation**! ⚖️\n")
    time.sleep(1)

    # Load case data from JSON
    case_data = load_case_data("data/case_data.json")
    if case_data is None:
        return  # Exit if case data couldn't be loaded

    # Extract legal references directly
    legal_references = case_data.get("legal_references", {})
    legal_context_full = build_legal_context(legal_references)

    print("📜 **Legal References Loaded:**")
    print(legal_context_full)
    print("=" * 60, "\n")

    # Assign courtroom roles
    assigned_roles = assign_roles(case_data)
    judge = assigned_roles["Judge"]
    appellant = assigned_roles["Appellant"]
    respondents = assigned_roles["Respondents"]

    # Let the user choose a role
    user_role = get_user_input("🔹 Choose your role (Appellant/Respondent): ", ["Appellant", "Respondent"], "Appellant")
    user_agent = appellant if user_role == "Appellant" else respondents[0]

    # Extract key case details
    case_facts = {
        "title": case_data["case_title"],
        "arguments": case_data["key_arguments"],
        "contract_purpose": case_data["contract_details"]["contract_purpose"],
        "court_decision": case_data["judgment_summary"]["court_decision"]
    }

    # AI-generated legal strategy
    strategy = suggest_strategy(user_role, case_facts, legal_references)
    print(f"\n⚖️ **AI-Generated Legal Strategy for {user_role}:**\n")
    print("💡 **Suggested Argument:**\n", strategy)
    print("\n" + "=" * 60)

    # Opening Statement by the user
    print(f"⚖️ {user_agent.name}, it's your turn to present your opening statement.")
    user_statement = get_user_input("📢 Enter your statement (or type 'suggest' for AI-generated): ", default="suggest")
    if user_statement.lower() == "suggest":
        user_statement = strategy  # Use the AI-suggested strategy

    print("\n-- AI Judge's Response --")
    print(f"👨‍⚖️ Judge: Considering the arguments presented, I acknowledge the statements made.\n")

    # AI dynamically detects objections
    objection = detect_objections(user_statement, case_facts)
    if "Yes" in objection:
        objection_type = objection.split("\n")[1]  # Extract objection type from AI response
        handle_objection("Opposing Counsel", objection_type)
        time.sleep(2)

    # Cross-examination phase
    print("\n⚔️ **Cross-Examination Phase Begins**")
    question = get_user_input(f"⚔️ You ({user_role}): Ask a question to Respondent (or type 'suggest'): ", default="suggest")
    if question.lower() == "suggest":
        question = "Can you provide evidence supporting your counterclaim?"
    answer = respondents[0].introduce() + " - Responds: The contract clause 9.7.1 was fairly assessed."

    print(f"💬 {respondents[0].name}: {answer}\n")

    # Courtroom dialogue loop
    while True:
        cont = get_user_input("🔄 Do you want to continue the courtroom debate? (Yes/No): ", ["Yes", "No"], "No")
        if cont == "No":
            break

        round_type = get_user_input("Type 'argument' to make another statement or 'question' to cross-examine: ", ["Argument", "Question"])
        if round_type == "Argument":
            new_statement = get_user_input("📢 Enter your statement (or type 'suggest' for AI argument): ", default="suggest")
            if new_statement.lower() == "suggest":
                new_statement = strategy
            print("\n-- AI Response --")
            print(f"👨‍⚖️ Judge: Noted. Proceeding with deliberation.\n")

        elif round_type == "Question":
            new_question = get_user_input(f"⚔️ Ask a question to {respondents[0].name} (or type 'suggest'): ", default="suggest")
            if new_question.lower() == "suggest":
                new_question = "How does your argument align with past legal precedents?"
            new_answer = respondents[0].introduce() + " - Responds: We rely on similar cases for justification."
            print(f"💬 {respondents[0].name}: {new_answer}\n")

    # AI-Judge delivers the final verdict
    print("\n🏛️ **Final Verdict:**")
    print(f"👨‍⚖️ Judge: After reviewing all arguments and legal precedents, I have reached a decision.\n")
    print(f"✅ **Court Decision:** {case_data['judgment_summary']['court_decision']}")
    print(f"📝 **Final Award:** {case_data['judgment_summary']['final_award']}\n")


if __name__ == "__main__":
    main()
