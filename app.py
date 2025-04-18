import re

import fitz  # PyMuPDF
import spacy

# Load pre-trained spaCy model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    """Extract text from the PDF."""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")  # Extract plain text
        full_text += text

    return full_text


def extract_details(text):
    """Extract details like Name, Address, Skills, Experience, etc., from the resume."""
    details = {
        "Name": None,
        "Address": None,
        "University Name": None,
        "Skills": None,
        "Experience": None,
        "Email": None,
        "Phone": None,
    }

    # Use spaCy's NER to identify common named entities like names, locations, etc.
    doc = nlp(text)

    # Searching for common named entities: PERSON (Name), GPE (Location), ORG (University/College)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not details["Name"]:
            details["Name"] = ent.text
        elif ent.label_ == "GPE" and not details["Address"]:
            details["Address"] = ent.text
        elif ent.label_ == "ORG" and not details["University Name"]:
            details["University Name"] = ent.text

    # Extracting email and phone using regex patterns
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}"
    phone_regex = r"\+?\(?\d{1,4}[\)\-\s]?\d{1,3}[\-\s]?\d{4,6}"

    details["Email"] = re.search(email_regex, text)
    details["Phone"] = re.search(phone_regex, text)

    # If found, clean the details
    if details["Email"]:
        details["Email"] = details["Email"].group(0)
    else:
        details["Email"] = "Not Found"

    if details["Phone"]:
        details["Phone"] = details["Phone"].group(0)
    else:
        details["Phone"] = "Not Found"

    # Extracting Skills (can be found under keywords like 'Skills' or 'Technical Skills')
    skills_section = re.search(
        r"(Skills|Technical Skills|Expertise)[\:\-]?\s*(.*?)(?=\n|$)",
        text,
        re.IGNORECASE,
    )
    if skills_section:
        details["Skills"] = skills_section.group(2).strip()
    else:
        details["Skills"] = "Not Found"

    # Extracting Experience (searching for 'Experience' or 'Work Experience')
    experience_section = re.search(
        r"(Experience|Work\s*Experience)[\:\-]?\s*(.*?)(?=\n|$)", text, re.IGNORECASE
    )
    if experience_section:
        details["Experience"] = experience_section.group(2).strip()
    else:
        details["Experience"] = "Not Found"

    return details


# Example usage
pdf_path = "/mnt/data/Rakibul Islam.pdf"  # Replace with your PDF path
extracted_text = extract_text_from_pdf(pdf_path)
details = extract_details(extracted_text)

# Print the extracted details
for key, value in details.items():
    print(f"{key}: {value}")
