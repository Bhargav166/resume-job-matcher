import re

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s-]{8,}\d', text)
    return match.group(0) if match else None

def extract_name(text):
    lines = text.strip().split("\n")
    return lines[0] if lines else None

def extract_skills(text, skill_set):
    found_skills = []
    for skill in skill_set:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills