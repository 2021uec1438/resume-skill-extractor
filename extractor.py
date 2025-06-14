import pdfplumber
import re

COMMON_SKILLS = [
    "python", "java", "c++", "javascript", "sql", "excel", "machine learning",
    "data analysis", "communication", "project management", "leadership",
    "html", "css", "react", "node.js", "aws", "docker", "git"
]

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_emails(text):
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(pattern, text)

def extract_phone_numbers(text):
    # Regex to match 10-digit numbers, with or without country code
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\d{10}'
    matches = re.findall(phone_pattern, text)
    
    # Combine country code (optional) and 10-digit number using a second regex
    full_pattern = r'(\+?\d{1,3}[-.\s]?)?(\d{10})'
    full_matches = re.findall(full_pattern, text)
    
    # Join each tuple into full phone numbers
    phones = [''.join(parts).strip() for parts in full_matches]
    return phones

def extract_name(text):
    lines = text.strip().split('\n')
    return lines[0] if lines else "Not found"

def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill in COMMON_SKILLS if skill in text_lower]

def extract_experience(text):
    keywords = ["intern", "engineer", "developer", "worked at", "experience", "company"]
    return [line for line in text.split('\n') if any(k in line.lower() for k in keywords)]
