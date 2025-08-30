
-- 1. Create database
CREATE DATABASE IF NOT EXISTS resume_matching;
USE resume_matching;

-- 2. Drop old tables if they exist
DROP TABLE IF EXISTS candidates;
DROP TABLE IF EXISTS ideal_profile;

-- 3. Create candidates table
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    resume_filename VARCHAR(200),
    resume_text TEXT,
    extracted_skills JSON,
    missing_skills JSON,
    score DECIMAL(5,2),
    decision VARCHAR(50),
    job_title VARCHAR(255)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create ideal profile table
CREATE TABLE ideal_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(100),
    must_have JSON,
    nice_to_have JSON
);

-- 5. Insert sample ideal profile
INSERT INTO ideal_profile (role, must_have, nice_to_have)
VALUES ("Data Analyst", '["Python","SQL","Pandas"]', '["Tableau","PowerBI"]');

-- 6. Insert sample candidates
INSERT INTO candidates 
(name, email, resume_filename, resume_text, extracted_skills, missing_skills, score, decision)
VALUES
("Alice Sharma", "alice@example.com", "alice_resume.pdf",
 "Alice has experience with Python, SQL, and Pandas.",
 '["Python","SQL","Pandas"]',
 '["Tableau","Machine Learning"]',
 78.50, "Accepted"),

("Rahul Mehta", "rahul@example.com", "rahul_resume.pdf",
 "Rahul knows Excel and SQL but lacks Python.",
 '["SQL","Excel"]',
 '["Python","Pandas","Tableau"]',
 55.20, "Improve"),

("Sneha Kapoor", "sneha@example.com", "sneha_resume.pdf",
 "Sneha has Python, SQL, Pandas, and Tableau.",
 '["Python","SQL","Pandas","Tableau"]',
 '["PowerBI"]',
 90.10, "Accepted");

-- 7. Ranking Query
SELECT id, name, email, score, decision
FROM candidates
ORDER BY score DESC
LIMIT 5;