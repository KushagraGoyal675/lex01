import time
import json
import os
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

courtroom_phases = [
    "Opening Statement", "Cross-Examination", "Evidence Submission",
    "Legal Precedents", "Closing Argument", "Verdict"
]

phase_index = 0  # Tracks current phase
case_data = None  # Stores loaded case data


def llm_generate_response(prompt):
    """Calls the Groq API to generate a response."""
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mixtral-8x7b-32768", "messages": [{"role": "system", "content": prompt}], "temperature": 0.5}
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
    except requests.RequestException as e:
        return f"⚠ API Error: {str(e)}"


def load_case_data():
    """Loads case data from a JSON file."""
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if not file_path:
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", f"Unable to load or parse {file_path}.")
        return None


def start_simulation():
    """Loads and displays case details."""
    global case_data, phase_index
    case_data = load_case_data()
    phase_index = 0
    if case_data:
        case_title.set(f"📜 Case: {case_data['case_title']}")
        case_details.insert(tk.END, f"Loaded case: {case_data['case_title']} ({case_data['date']})\n")
        proceed_to_next_phase()
    else:
        case_details.insert(tk.END, "⚠ No case data loaded!\n")


def proceed_to_next_phase():
    """Moves to the next phase of the courtroom trial."""
    global phase_index
    if not case_data:
        messagebox.showwarning("Warning", "Load a case first!")
        return

    if phase_index >= len(courtroom_phases):
        case_details.insert(tk.END, "\n⚖️ **Case Closed!** The trial has concluded.\n")
        return

    phase = courtroom_phases[phase_index]
    user_role = role_var.get()
    user_argument = user_argument_entry.get("1.0", tk.END).strip()
    case_facts = {"title": case_data["case_title"], "arguments": case_data.get("key_arguments", "No details provided.")}

    prompt_templates = {
        "Opening Statement": f"Generate an opening statement for {user_role} in the case '{case_facts['title']}'. Arguments: {case_facts['arguments']}.",
        "Cross-Examination": f"Generate a tough cross-examination question for the opposing party in '{case_facts['title']}'.",
        "Evidence Submission": f"Summarize key evidence supporting {user_role} in '{case_facts['title']}'.",
        "Legal Precedents": f"List similar past legal cases relevant to '{case_facts['title']}' and their impact.",
        "Closing Argument": f"Generate a persuasive closing argument for {user_role} in '{case_facts['title']}'.",
        "Verdict": f"Act as a judge and give a verdict for '{case_facts['title']}' based on arguments: {case_facts['arguments']}."
    }

    if user_argument:
        prompt_templates[phase] += f"\nUser's Additional Argument: {user_argument}"

    response = llm_generate_response(prompt_templates[phase])

    case_details.insert(tk.END, f"\n🔹 **{phase} (AI Response):**\n{response}\n")
    case_details.see(tk.END)

    phase_index += 1  # Move to next phase


def export_case_discussion():
    """Exports the case discussion to a text file."""
    content = case_details.get("1.0", tk.END)
    if not content.strip():
        messagebox.showwarning("Warning", "No case discussion to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Success", "Case discussion saved successfully!")


# GUI Setup
root = tk.Tk()
root.title("⚖ AI Courtroom Simulation ⚖")
root.geometry("800x600")

# Title
tk.Label(root, text="⚖ AI Courtroom Simulation ⚖", font=("Arial", 16, "bold")).pack(pady=5)

# Load Case Button
load_button = tk.Button(root, text="📂 Load Case", command=start_simulation)
load_button.pack()

# Case Title
case_title = tk.StringVar()
tk.Label(root, textvariable=case_title, font=("Arial", 12)).pack()

# Case Details Text Area
case_details = scrolledtext.ScrolledText(root, width=90, height=12, wrap=tk.WORD)
case_details.pack(pady=5)

# User Input for Custom Arguments
tk.Label(root, text="Your Additional Argument:").pack()
user_argument_entry = scrolledtext.ScrolledText(root, width=80, height=3, wrap=tk.WORD)
user_argument_entry.pack()

# Role Selection
tk.Label(root, text="Choose Role:").pack()
role_var = tk.StringVar(value="Appellant")
roles = ["Appellant", "Respondent", "Judge"]
for role in roles:
    tk.Radiobutton(root, text=role, variable=role_var, value=role).pack()

# Proceed to Next Phase Button
proceed_button = tk.Button(root, text="✅ Yes (Proceed)", command=proceed_to_next_phase)
proceed_button.pack(pady=5)

# Export Discussion Button
export_button = tk.Button(root, text="📜 Export Discussion", command=export_case_discussion)
export_button.pack(pady=5)

# Run GUI
root.mainloop()
