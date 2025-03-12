import random

def handle_objection(objection_by, reason):
    """AI handles objections with legal reasoning."""
    print(f"🔴 Objection by {objection_by.name}: {reason}")

    # AI-driven logic to check objection validity
    valid_reasons = ["Hearsay", "Leading question", "Irrelevant", "Speculative"]
    if any(word.lower() in reason.lower() for word in valid_reasons):
        response = "Objection sustained."
    else:
        response = "Objection overruled."

    print(f"⚖️ Judge: {response}\n")
