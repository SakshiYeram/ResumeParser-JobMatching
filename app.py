from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import json
import pymysql
from pdfminer.high_level import extract_text
from matcher import ResumeMatcher  # Your ML script

app = Flask(__name__)

# ---------------- Upload Folder ----------------
UPLOAD_FOLDER = os.path.abspath("uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- Database Connection ----------------
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Sakshi@123",
    database="resume_matching",
    cursorclass=pymysql.cursors.DictCursor
)

# ---------------- ML Setup ----------------
CSV_PATH = os.path.join(os.path.dirname(__file__), "job_skills.csv")
matcher = ResumeMatcher()
if not matcher.load_job_skills(CSV_PATH):
    raise RuntimeError(f"Failed to load job skills CSV at {CSV_PATH}")

# Temporary in-memory storage for analysis
results = []

# ---------------- Routes ----------------

# Home → Upload Page
@app.route("/")
def home():
    return render_template("upload.html")


# Upload Resume
@app.route("/upload", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return "No file uploaded", 400
    file = request.files["resume"]
    if file.filename == "":
        return "No selected file", 400
    
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    try:
        # Extract text from PDF
        resume_text = extract_text(filepath)

         # Get target job dynamically from the form
        target_job = request.form.get("target_job", "ML Engineer")  # default to ML Engineer if nothing selected
        

        # Analyze resume for the selected job
        result = matcher.analyze_resume(filepath, target_job)

 
        # Combine missing required & optional skills
        missing_skills = result["missing_required"] + result["missing_optional"]

        # Save to Database
        with db.cursor() as cursor:
            sql = """
            INSERT INTO candidates 
            (name, resume_filename, resume_text, extracted_skills, missing_skills, score, decision)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                file.filename,
                file.filename,
                resume_text,
                json.dumps(result["resume_skills"]),
                json.dumps(missing_skills),
                result["overall_score"],
                "Pending" # Initial decision
            ))
            db.commit()

        # Save result temporarily for analysis
        results.append({
            "name": file.filename,
            "job_title": result["job_title"],
            "score": result["overall_score"],
            "skills": result["resume_skills"],
            "missing_skills": missing_skills,
            "recommendations": result["recommendations"]
        })

        return redirect(url_for("analysis_page"))

    except Exception as e:
        return f"Error analyzing resume: {e}", 500


# Analysis Page
@app.route("/analysis")
def analysis_page():
    if not results:
        return "No analysis yet. Please upload a resume first.", 400

    result = results[-1]

    # Map variables to match your HTML template
    return render_template(
        "analysis.html",
        job_title=result.get("job_title", ""),
        score=result.get("score", 0),
        skills_detected=result.get("skills", []),
        missing_required=result.get("missing_skills", [])
    )


# Ranking Page

@app.route("/ranking")
def ranking_page():
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT name, resume_filename, score, extracted_skills, missing_skills 
            FROM candidates 
            ORDER BY score DESC
        """)
        ranking_data = cursor.fetchall()

        # Convert JSON fields to Python lists and add job_title for template
        for candidate in ranking_data:
            candidate['skills_detected'] = json.loads(candidate['extracted_skills']) if candidate['extracted_skills'] else []
            candidate['missing_required'] = json.loads(candidate['missing_skills']) if candidate['missing_skills'] else []
            candidate['job_title'] = "ML Engineer"  # Replace with dynamic job if available

    return render_template("ranking.html", ranking_data=ranking_data)

# Delete Resume
@app.route("/delete/<resume_filename>", methods=["POST"])
def delete_resume(resume_filename):
    try:
        # 1. Remove from database
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM candidates WHERE resume_filename=%s", (resume_filename,))
            db.commit()

        # 2. Remove file from uploads folder
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume_filename)
        if os.path.exists(filepath):
            os.remove(filepath)

        # 3. Remove from temporary results list
        global results
        results = [r for r in results if r["name"] != resume_filename]

        return redirect(url_for("ranking_page"))

    except Exception as e:
        return f"Error deleting resume: {e}", 500


# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
