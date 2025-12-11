# ðŸŒŸ Resume Parser & Job Matching System

A smart, lightweight web application that **extracts skills from a
resume**, compares them with a **predefined technical job skills
dataset**, and generates a **match score**.\
Built using **Flask**, **Pandas**, and **PDF parsing techniques**.

------------------------------------------------------------------------

## ðŸš€ Features

âœ” Upload **Resume (PDF)**\
âœ” Predefined **Job Skills CSV** (no user upload needed)\
âœ” Automatic **Skill Extraction & Matching**\
âœ” Displays **Match Percentage + Matched & Missing Skills**\
âœ” Clean and intuitive **Flask-based Web UI**

------------------------------------------------------------------------

## ðŸ—‚ï¸ Project Structure

    ResumeParser-JobMatching/
    â”‚
    â”œâ”€â”€ app.py               # Main Flask application
    â”œâ”€â”€ matcher.py           # Core logic for skill matching
    â”œâ”€â”€ job_skills.csv       # Combined job skills dataset
    â”œâ”€â”€ project.sql          # (Optional) database file
    â”œâ”€â”€ static/              # CSS, JS, images
    â”œâ”€â”€ templates/           # HTML templates
    â”œâ”€â”€ .gitignore           
    â””â”€â”€ README.md

------------------------------------------------------------------------

## âš™ï¸ Installation & Setup

### 1. Clone the Repository

    git clone https://github.com/YourUsername/ResumeParser-JobMatching.git
    cd ResumeParser-JobMatching

### 2. (Optional) Create a Virtual Environment

    python -m venv venv
    source venv/bin/activate    # Mac/Linux
    venv\Scripts\activate       # Windows

### 3. Install Dependencies

    pip install flask pandas pdfminer.six

### 4. Run the Application

    python app.py

### 5. Open in Browser

    http://127.0.0.1:5000/

------------------------------------------------------------------------

## ðŸŽ¯ How the System Works

1.  Upload your **Resume (PDF)**\
2.  System extracts skills\
3.  Compares with built-in **job_skills.csv**\
4.  Shows:
    -   âœ” Matched Skills\
    -   âœ” Missing Skills\
    -   âœ” Match Percentage

------------------------------------------------------------------------

## ðŸ“Œ Tech Stack

-   Python\
-   Flask\
-   Pandas\
-   PDFMiner\
-   HTML / CSS

------------------------------------------------------------------------

## ðŸ”® Future Enhancements

âœ¨ Allow uploading custom job descriptions\
âœ¨ Multi-role job matching\
âœ¨ Improved NLP skill extraction\
âœ¨ Login & dashboard\
âœ¨ DOCX resume support

------------------------------------------------------------------------

## ðŸ™Œ Contributions

Pull requests and issues are welcome!