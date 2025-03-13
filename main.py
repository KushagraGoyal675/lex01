import time
import json
import os
import requests
from dotenv import load_dotenv
import groq
from agents import CourtAgent
from objections import handle_objection, detect_objections
from roles import assign_roles
from strategy import suggest_strategy
from file_selection import select_case_file  # Allow user to select case data file

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Set up Groq API client
client = groq.Client(api_key=GROQ_API_KEY)

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def llm_generate_response(prompt):
    """Calls the Groq LLM API to generate a response based on the prompt."""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "system", "content": prompt}],
        "temperature": 0.5
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except requests.RequestException as e:
        return f"⚠ API Error: {str(e)}"

def load_case_data():
    """Loads case data from a user-selected JSON file."""
    case_file = select_case_file()
    if not case_file:
        return None
    try:
        with open(case_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"⚠ Error: Unable to load or parse {case_file}.")
        return None

def get_user_input(prompt, valid_options=None, default=None):
    """Gets user input with optional validation."""
    while True:
        user_input = input(prompt).strip()
        if valid_options and user_input.capitalize() not in valid_options:
            print(f"❌ Invalid input. Please enter one of: {', '.join(valid_options)}")
            continue
        return user_input.capitalize() if valid_options else user_input or default

def print_courtroom_scene(phase):
    """Displays courtroom phase descriptions."""
    scenes = {
        "opening": "The courtroom is in session. The judge takes the bench. The audience quiets as the trial begins.",
        "evidence": "A key piece of evidence is presented, drawing murmurs from the gallery.",
        "witness": "A crucial witness is called to the stand. The room is silent in anticipation.",
        "cross": "The air is tense as cross-examination begins. Lawyers exchange sharp questions.",
        "jury": "The jury deliberates over the evidence and arguments, weighing every detail.",
        "closing": "Both sides present their closing arguments, making their final persuasive appeals.",
        "verdict": "The judge returns to deliver the final verdict after reviewing all evidence and arguments."
    }
    print(f"\n📣 {scenes.get(phase, '')}")
    time.sleep(2)

def generate_phase_response(phase, user_role, case_facts):
    """Generates AI responses for courtroom phases."""
    prompt_templates = {
        "opening": f"Generate an opening statement for {user_role} in the case titled '{case_facts['title']}'. Arguments: {case_facts['arguments']}.",
        "evidence": f"Describe a key piece of evidence {user_role} might present in '{case_facts['title']}'.",
        "witness": f"Generate a witness testimony relevant to '{case_facts['title']}'.",
        "cross": f"Generate a tough cross-examination question for the opposing party in '{case_facts['title']}'.",
        "closing": f"Generate a persuasive closing argument for {user_role} in '{case_facts['title']}', summarizing key arguments."
    }
    return llm_generate_response(prompt_templates.get(phase, "Generate a legal argument."))

def main():
    """Runs the AI courtroom simulation."""
    print("\n⚖️ Welcome to the **AI Courtroom Simulation**! ⚖️\n")
    time.sleep(1)

    # Load case data
    case_data = load_case_data()
    if case_data is None:
        return

    print(f"\n✅ Loaded case: {case_data['case_title']} ({case_data['date']})")
    time.sleep(1)

    # Assign courtroom roles
    assigned_roles = assign_roles(case_data)
    appellant, respondents = assigned_roles["Appellant"], assigned_roles["Respondents"]
    judge = assigned_roles["Judge"]

    # User selects role
    user_role = get_user_input("🔹 Choose your role (Appellant/Respondent): ", ["Appellant", "Respondent"], "Appellant")
    user_agent = appellant if user_role == "Appellant" else respondents[0]
    opposition = respondents[0] if user_role == "Appellant" else appellant

    # Extract key case details
    case_facts = {
        "title": case_data["case_title"],
        "arguments": case_data.get("key_arguments") or case_data.get("legal_arguments", {})
    }

    # AI-generated legal strategy
    print(f"\n⚖️ **AI Legal Strategy for {user_role}:**")
    strategy = suggest_strategy(user_role, case_facts, case_data.get("legal_references", {}))
    print("💡 **Suggested Argument:**\n", strategy)
    print("=" * 60)
    time.sleep(1)

    # **Opening Statements Phase**
    print_courtroom_scene("opening")
    opening_statement = get_user_input("📢 Enter opening statement (or type 'suggest'): ", default="suggest")
    print(f"\n-- {user_agent.name} states: \"{generate_phase_response('opening', user_role, case_facts) if opening_statement.lower() == 'suggest' else opening_statement}\"")

    print(
        f"\n-- {opposition.name} (Opposing Counsel) responds: \"{generate_phase_response('opening', opposition.role_type, case_facts)}\"")
    time.sleep(2)

    # **Objections Handling**
    objection = detect_objections(opening_statement, case_facts)
    if "Yes" in objection:
        handle_objection(opposition.name, objection.split("\n")[1])
        time.sleep(2)

    # **Cross-Examination**
    print_courtroom_scene("cross")
    question = get_user_input(f"⚔️ Ask a question to {opposition.name} (or type 'suggest'): ", default="suggest")
    print(f"\n💬 {opposition.name} responds: \"{generate_phase_response('cross', opposition.role, case_facts) if question.lower() == 'suggest' else 'The contract clause was fairly applied.'}\"")
    time.sleep(2)

    # **Closing Arguments**
    print_courtroom_scene("closing")
    closing_statement = get_user_input("📢 Enter closing argument (or type 'suggest'): ", default="suggest")
    print(f"\n-- AI Judge ({judge.name}) responds: \"I have carefully reviewed all arguments.\"")
    time.sleep(2)

    # **Final Verdict**
    print_courtroom_scene("verdict")
    print(f"👨‍⚖️ Judge: \"After reviewing all evidence and arguments, my verdict is: {case_data['judgment_summary']['court_decision']}\"")
    print("\n🙏 Thank you for participating in the AI Courtroom Simulation.")

if __name__ == "__main__":
    main()
