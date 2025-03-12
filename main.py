import time
from roles import extract_text_from_pdf, identify_roles_with_regex
from agents import CourtAgent
from objections import handle_objection
from strategy import suggest_strategy

# Load case data and extract roles from PDF
text = extract_text_from_pdf("data/cou.pdf")
court_roles = identify_roles_with_regex(text)

# Initialize AI courtroom agents
judge = CourtAgent(court_roles["Judge"], "Judge")
prosecutor = CourtAgent(court_roles["Prosecutor"], "Prosecutor")
defense = CourtAgent(court_roles["Defense"], "Defense Attorney")
defendant = CourtAgent(court_roles["Defendant"], "Defendant")

# Let the user choose a role: Prosecutor or Defendant
user_role = input("Choose your role (Prosecutor/Defendant): ").strip().capitalize()
if user_role not in ["Prosecutor", "Defendant"]:
    print("Invalid role selected. Defaulting to Prosecutor.")
    user_role = "Prosecutor"

user_agent = prosecutor if user_role == "Prosecutor" else defendant

print(f"\n🎭 You are {user_agent.name}, acting as the {user_role}.\n")

# Provide strategy suggestions to the user
print(f"💡 Suggested Strategy: {suggest_strategy(user_role)}\n")

# Opening Statement by the user
print(f"⚖️ {user_agent.name} (Your Turn):")
user_statement = input("📢 Your opening statement (or type 'suggest' for a default argument): ")
if user_statement.lower() == "suggest":
    user_statement = suggest_strategy(user_role)
print("\n-- AI Response (filtered) --")
print(judge.respond(user_statement))
print("\n")

# Handle an objection (simulate an objection by opposing counsel)
handle_objection(defense if user_role == "Prosecutor" else prosecutor, "Speculation")
time.sleep(2)

# Cross-examination: if user is Prosecutor, ask question to Defendant; otherwise, let AI ask.
if user_role == "Prosecutor":
    question = input(f"⚔️ You (Prosecutor): Ask a question to {defendant.name} (or type 'suggest' for a default question): ")
    if question.lower() == "suggest":
        question = "What evidence supports your claim?"
    answer = defendant.respond(question, additional_info="Answer truthfully.")
else:
    question = prosecutor.respond("Ask a challenging question to the defendant.")
    answer = input(f"⚔️ You (Defendant): {question}\n💬 Your Answer (or type 'suggest' for a default answer): ")
    if answer.lower() == "suggest":
        answer = "I maintain that the evidence against me is insufficient and circumstantial."
print(f"  💬 {defendant.name}: {answer}\n")

# Continue conversation rounds until the user decides to finish
while True:
    cont = input("Do you want to continue the conversation? (yes/no): ").strip().lower()
    if cont in ["no", "n"]:
        break
    # Choose a conversation round type: additional argument or cross-examination question
    round_type = input("Type 'argument' to make another statement or 'question' to ask a new question: ").strip().lower()
    if round_type == "argument":
        new_statement = input("Enter your statement (or type 'suggest' for a default argument): ")
        if new_statement.lower() == "suggest":
            new_statement = suggest_strategy(user_role)
        print("\n-- AI Response (filtered) --")
        print(judge.respond(new_statement))
    elif round_type == "question":
        if user_role == "Prosecutor":
            new_question = input(f"⚔️ You (Prosecutor): Ask a question to {defendant.name} (or type 'suggest' for a default question): ")
            if new_question.lower() == "suggest":
                new_question = "Can you explain your alibi in detail?"
            new_answer = defendant.respond(new_question, additional_info="Answer truthfully.")
            print(f"  💬 {defendant.name}: {new_answer}\n")
        else:
            new_question = prosecutor.respond("Ask a challenging question to the defendant.")
            new_answer = input(f"⚔️ You (Defendant): {new_question}\n💬 Your Answer (or type 'suggest' for a default answer): ")
            if new_answer.lower() == "suggest":
                new_answer = "I maintain that the evidence is purely circumstantial and lacks credibility."
            print(f"  💬 {defendant.name}: {new_answer}\n")
    else:
        print("Invalid option. Please choose either 'argument' or 'question'.")
    print("\n")

# Judge delivers the final verdict
print("🏛️ Final Verdict:")
print(judge.respond("Deliver the verdict"))
