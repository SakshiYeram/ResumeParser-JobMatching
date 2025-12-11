## 🌟 Resume Parser & Job Matching System
A smart, lightweight web application that extracts skills from a resume, compares them with apredefined technical job skills dataset, and generates a match score. Built using Flask, Pandas, andPDF parsing techniques.

## ⚪ Features:
- Upload Resume (PDF)
- Predefined Job Skills CSV (no user upload needed)
- Automatic Skill Extraction & Matching
- Displays Match Percentage + Matched & Missing Skills
- Flask-based Web UI

## Project Structure:
app.py - Flask application
matcher.py - Matching logic
job_skills.csv - Skills dataset
project.sql - Optional database
static/ - CSS , JS
templates/ - HTML files

Installation:
1. Clone repo
2. Create virtual environment
3. Install dependencies
4. Run app
5. Open browser: http://127.0.0.1:5000/

How it Works:
1. Upload resume
2. Extract skills
3. Compare with job_skills.csv
4. Show match % + matched/missing skills

Tech Stack:

1)Python

2)Flask 

3)Pandas

4)PDFMiner

5)HTML/CSS

Future Enhancements:

✨Upload custom job descriptions

✨Multi-role matching

✨NLP improvements

✨Login/dashboard

✨DOCX support