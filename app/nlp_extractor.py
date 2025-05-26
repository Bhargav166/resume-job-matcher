import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_email(text):
    # Use regex (still very effective for emails)
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else None

def extract_phone(text):
    # Use regex (optional: add NER-based fallback)
    match = re.search(r'\+?\d[\d\s\-()]{8,}\d', text)
    return match.group(0) if match else None

def extract_name(text):
    """
    Use NER to find first PERSON entity in the top of the resume.
    Prioritize PERSON with 2-3 words
    Ignore obvious tool names
    """
    doc = nlp(text)
    lines = text.strip().split("\n")
    first_lines = "\n".join(lines[:15])
    header_doc = nlp(first_lines)

    ignore_list = {"jenkins", "gitlab", "taas"}

    # Check for Person entity and not in Ignore list of tech tools
    for ent in header_doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            if 1 < len(name.split()) <= 3 and name.lower() not in ignore_list:
                return name

    # Backup for proper case name
    for line in lines:
        words = line.strip().split()
        if 1 < len(words) <= 3 and all(word.istitle() for word in words):
            return line.strip()
        
    return lines[0] if lines else None

def extract_skills(text, skill_set):
    """
    Match provided skill_set against noun chunks and tokens.
    """
    doc = nlp(text)
    found_skills = set()

    skill_set_lower = {skill.lower() for skill in skill_set}

    # Check for skills in phrases
    for chunk in doc.noun_chunks:
        if chunk.text.lower() in skill_set_lower:
            found_skills.add(chunk.text)

    # Check Single word skills 
    for token in doc:
        if token.text.lower() in skill_set_lower:
            found_skills.add(token.text)

    return list(found_skills)

