import re
import sys
import spacy
import pandas as pd
from pathlib import Path
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class ResumeMatcher:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sbert = SentenceTransformer('all-MiniLM-L6-v2')
        self.job_db = {}
        self.global_skills = []

    def _fuzzy_match_skills(self, skill: str, threshold: float = 0.7) -> list:
        """Use SBERT to find similar skills via cosine similarity"""
        # Encode the input skill
        skill_emb = self.sbert.encode([skill])
        
        # Calculate cosine similarity with cached global skill embeddings
        similarities = cosine_similarity(skill_emb, self.global_skill_embs)[0]
        
        # Return skills above the similarity threshold
        matched = [self.global_skills[i] for i in range(len(similarities)) if similarities[i] >= threshold]
        return matched



    def load_job_skills(self, csv_path: str) -> bool:
        """Load job skills from a CSV file and pre-encode global skills"""
        try:
            df = pd.read_csv(csv_path)
            for index, row in df.iterrows():
                req_skills = [s.strip().replace('"', '').lower() for s in row['Required Skills'].split(',')]
                opt_skills = [s.strip().replace('"', '').lower() for s in row['Optional Skills'].split(',')]
                self.job_db[row['Job Title']] = {
                    'required': req_skills,
                    'optional': opt_skills
                }
                self.global_skills.extend(req_skills + opt_skills)
            
            # Pre-encode global skills
            self.global_skills = list(set(self.global_skills))  # Remove duplicates
            self.global_skill_embs = self.sbert.encode(self.global_skills)  # Cache embeddings
            return True
        except Exception as e:
            import traceback
            print("Error loading job skills")
            traceback.print_exc()
            return False


    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Robust PDF text extraction"""
        try:
            # Validate PDF
            if not Path(pdf_path).exists():
                raise FileNotFoundError(f"File not found: {pdf_path}")
            
            with open(pdf_path, 'rb') as f:
                if f.read(4) != b'%PDF':
                    raise ValueError("Invalid PDF header")
            
            # Extract and clean text
            text = extract_text(pdf_path)
            return self._clean_text(text) if text.strip() else ""
            
        except Exception as e:
            print(f"PDF Error: {str(e)}")
            return ""

    def analyze_resume(self, pdf_path: str, target_job: str) -> dict:
        """Main analysis workflow"""
        if target_job not in self.job_db:
            raise ValueError(f"Unknown job title: {target_job}")
        
        # Process resume
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            raise ValueError("Failed to extract text from PDF")
        
        resume_skills = self._extract_skills(text)
        
        if not resume_skills:
            return {
                'job_title': target_job,
                'overall_score': 0,
                'message': "No skills detected in the resume. Please check the format or content."
            }
        
        job_data = self.job_db[target_job]
        
        # Calculate matches
        required_match = self._calculate_match(resume_skills, job_data['required'])
        optional_match = self._calculate_match(resume_skills, job_data['optional'])
        
        overall_score = round((0.7 * required_match) + (0.3 * optional_match), 1)

        return {
            'job_title': target_job,
            'overall_score': overall_score,
            'resume_skills': resume_skills,
            'missing_required': list(set(job_data['required']) - set(resume_skills)),
            'missing_optional': list(set(job_data['optional']) - set(resume_skills)),  # New
            'recommendations': self._get_recommendations(resume_skills, target_job)
        }


    # Helper methods
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return re.sub(r'\s+', ' ', text).strip()

    def _extract_skills(self, text: str) -> list:
        """Extract skills with NLP + fuzzy matching"""
        doc = self.nlp(text)
        found_skills = set()

        # Normalize all global skills to lowercase for consistency
        global_skills_lower = [s.lower() for s in self.global_skills]

        # Check noun chunks for multi-word skills
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.lower().strip()
            if chunk_text in global_skills_lower:
                found_skills.add(chunk_text)
                continue
                
            # Fuzzy match for noun chunks
            fuzzy_matches = self._fuzzy_match_skills(chunk_text)
            if fuzzy_matches:
                found_skills.update(fuzzy_matches)

        # Check individual tokens
        for token in doc:
            token_text = token.text.lower()
            
            # Check for exact matches first
            if token_text in global_skills_lower:
                found_skills.add(token_text)
                continue
                
            # Fuzzy match fallback for tokens
            fuzzy_matches = self._fuzzy_match_skills(token_text)
            if fuzzy_matches:
                found_skills.update(fuzzy_matches)
        
        return list(found_skills)


    def _calculate_match(self, resume_skills: list, job_skills: list) -> float:
        """Calculate percentage match between skill sets"""
        if not job_skills:
            return 100.0  # No skills to match = perfect match
            
        matched = len(set(resume_skills) & set(job_skills))
        return round((matched / len(job_skills)) * 100, 1)

    def _get_recommendations(self, skills: list, current_job: str, top_n: int = 3) -> list:
        """Recommend alternative job matches"""
        scores = []
        for title, data in self.job_db.items():
            if title == current_job:
                continue
                
             # Weighted scoring (70% required, 30% optional)
            required_match = self._calculate_match(skills, data['required'])
            optional_match = self._calculate_match(skills, data['optional'])
            overall_score = round((0.7 * required_match) + (0.3 * optional_match), 1)
            
            scores.append({
                'job_title': title,
                'match_score': overall_score,  # Now uses weighted score
                'required_skills': data['required'],
                'optional_skills': data['optional']
            })
        
        return sorted(scores, key=lambda x: -x['match_score'])[:top_n]


if __name__ == "_main_":
    # Configuration
    CSV_PATH = "job_skills.csv"  
    RESUME_PATH = "resume.pdf"   
    TARGET_JOB = "ML Engineer"  
    
    print("\nResume-Job Matcher\n")
    
    # Initialize matcher
    matcher = ResumeMatcher()
    
    # Load job data
    if not matcher.load_job_skills(CSV_PATH):
        sys.exit(1)
    
    # Analyze resume
    try:
        result = matcher.analyze_resume(RESUME_PATH, TARGET_JOB)
        
        # Display results
        print(f"Analysis for: {result['job_title']}")
        print(f"Overall Match: {result['overall_score']}%")
        
        print("\n Your Skills:", ', '.join(sorted(result['resume_skills'])))
        
        if result['missing_required']:
            print("\n Missing Required Skills:")
            print('\n'.join(f"- {skill}" for skill in result['missing_required']))
        else:
            print("\n All required skills present!")

        if result['missing_optional']:
            print("\n Optional Skills:")
            print('\n'.join(f"- {skill}" for skill in result['missing_optional']))
        else:
            print("\n All optional skills present!")
        
        print("\n Recommended Alternatives:")
        for job in result['recommendations']:
            print(f"- {job['job_title']} ({job['match_score']}% match)")
            
    except Exception as e:
        print(f"\n Error: {str(e)}")
        sys.exit(1)