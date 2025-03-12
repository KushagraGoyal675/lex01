import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF case file."""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def identify_roles_with_regex(text):
    """Extracts courtroom role names from text using regex."""
    roles = {
        "Judge": re.search(r"Judge\s+(\w+\s\w+)", text),
        "Prosecutor": re.search(r"Prosecutor\s+(\w+\s\w+)", text),
        "Defense": re.search(r"Defense\s+Attorney\s+(\w+\s\w+)", text),
        "Defendant": re.search(r"Defendant\s+(\w+\s\w+)", text),
    }
    return {role: match.group(1) if match else get_fallback_name(role) for role, match in roles.items()}

def get_fallback_name(role):
    """Assigns default names if they cannot be extracted."""
    fallback_names = {
        "Judge": "Justice Xavier",
        "Prosecutor": "John Smith",
        "Defense": "Emily Johnson",
        "Defendant": "Alex Carter"
    }
    return fallback_names.get(role, "Unknown")
