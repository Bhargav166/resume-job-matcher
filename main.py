from flask import Flask, render_template, request, redirect
import os
from app.parser import extract_text_from_docx, extract_text_from_pdf

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
    
    return render_template("result.html", text=extracted_text)

if __name__ == "__main__":
    app.run(debug=True)