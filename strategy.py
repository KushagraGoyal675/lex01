import random

def suggest_strategy(role):
    """AI suggests strategies for the Prosecutor or Defendant."""
    strategies = {
        "Prosecutor": [
            "Focus on inconsistencies in the Defendant’s statement.",
            "Use forensic evidence to strengthen your case.",
            "Challenge the credibility of the Defendant’s alibi."
        ],
        "Defendant": [
            "Highlight lack of evidence against you.",
            "Argue that prosecution is speculative.",
            "Emphasize any procedural errors in the case."
        ]
    }
    return random.choice(strategies.get(role, ["Present a strong argument."]))
