# main.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Resume Parser is up and running!"

if __name__ == "__main__":
    app.run(debug=True)
