# Resume Parser & Job Matching

A simple web-based application that allows users to upload resumes and match them with job descriptions to find the best skill match. Built using **Flask**, **Pandas**, and **basic file handling techniques (no NLP used)**.

---

## Features
- Upload **resume (PDF)** and **job description (CSV)**  
- Extract and compare skills  
- Display match percentage  
- Interactive web interface using Flask  

---

## Project Structure
```
ResumeParser-JobMatching/
│
├── app.py               # Main Flask application
├── matcher.py           # Core logic for skill matching
├── project.sql          # Database file (if used)
├── job_skills.csv       # Sample job skills dataset
├── static/              # CSS, JS, and images
├── templates/           # HTML templates
├── .gitignore           # Ignore unnecessary files
└── README.md            # Project documentation
```

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YourUsername/ResumeParser-JobMatching.git
cd ResumeParser-JobMatching
```

### 2. (Optional) Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # For Linux/Mac
venv\Scripts\activate       # For Windows
```

### 3. Install Required Dependencies
```bash
pip install flask pandas pdfminer.six
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your browser and go to:  
```
http://127.0.0.1:5000/
```

---

## Usage
- Upload your **resume (PDF)**.  
- Upload the **job description (CSV)**.  
- View the matched skills and match percentage.  

---

## Future Enhancements
- Add user login/signup  
- Improve matching algorithm  
- Store matches in a database  
- Support multiple job postings  

---

