import re

def remove_chain_of_thought(response):
    """Removes internal chain-of-thought text from the response."""
    # This regex removes text between <think> and </think>, including the tags.
    cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    return cleaned_response.strip()
