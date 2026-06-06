from flask import Flask, render_template, request
from resume_parser import extract_text_from_docx, extract_text_from_pdf
from gemini_service import generate_resume_report
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():

    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file."

    desired_role = request.form.get("desired_role")

    if not desired_role:
        return "Please enter a desired role."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    # Extract resume text
    if file.filename.lower().endswith(".docx"):
        resume_text = extract_text_from_docx(filepath)

    elif file.filename.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(filepath)

    else:
        return "Only PDF and DOCX files are supported."

    # Generate AI report
    report = generate_resume_report(
        resume_text,
        desired_role
    )

    # Show result page
    return render_template(
        "result.html",
        report=report,
        desired_role=desired_role
    )


if __name__ == "__main__":
    app.run(debug=True)