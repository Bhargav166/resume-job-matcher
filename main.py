# Python libraries
from flask import Flask, render_template, request, redirect
import os

# Custom functions
from app.parser import extract_text_from_docx, extract_text_from_pdf
from app.extractors import extract_email, extract_phone, extract_name, extract_skills

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def index():
    return render_template('upload.html')

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['resume']
    if not file:
        return "No file uploaded.", 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    if file.filename.endswith('.pdf'):
        extracted_text = extract_text_from_pdf(filepath)
    elif file.filename.endswith('.docx'):
        extracted_text = extract_text_from_docx(filepath)
    else:
        return "Unsupported file type.", 400
    
    email = extract_email(extracted_text)
    phone = extract_phone(extracted_text)
    name = extract_name(extracted_text)

    common_skills = ["Python", "Java", "SQL", "JavaScript", "C++", "React", "Django"]
    skills = extract_skills(extracted_text, common_skills)
    
    return render_template("result.html", text=extracted_text, email=email, phone=phone, name=name, skills=skills)

if __name__ == "__main__":
    app.run(debug=True)