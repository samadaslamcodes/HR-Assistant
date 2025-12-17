import re
import string
import os
import logging
import pdfplumber
import docx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Try importing spacy
try:
    import spacy
    # Load the model - using 'en_core_web_md' for vectors is recommended
    # If not found, fall back to simple matching or warn
    try:
        nlp = spacy.load("en_core_web_md")
    except OSError:
        logging.warning("Spacy model 'en_core_web_md' not found. Semantic matching will be limited. Please run: python -m spacy download en_core_web_md")
        try:
            nlp = spacy.load("en_core_web_sm") # Fallback to small model
        except OSError:
            nlp = None
except ImportError:
    nlp = None

# predefined skill lists for categorization
SKILL_CATEGORIES = {
    "technical": {
        "python", "java", "c++", "javascript", "react", "angular", "vue", "node", "django", "flask", 
        "sql", "nosql", "mysql", "postgresql", "mongodb", "aws", "azure", "gcp", "docker", "kubernetes", 
        "git", "linux", "html", "css", "machine learning", "deep learning", "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch"
    },
    "soft": {
        "communication", "leadership", "teamwork", "problem solving", "critical thinking", "time management", 
        "adaptability", "creativity", "collaboration", "negotiation", "presentation", "mentoring"
    },
    "tools": {
        "jira", "confluence", "slack", "trello", "asana", "zoom", "ms office", "excel", "powerpoint", 
        "tableau", "power bi", "figma", "photoshop", "illustrator", "vscode", "pycharm"
    }
}

def get_stopwords():
    return {
        'and', 'or', 'not', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'from', 'by', 
        'with', 'as', 'of', 'for', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'but', 'if', 'then', 'else', 'when',
        'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
        'other', 'some', 'such', 'no', 'nor', 'too', 'very', 'can', 'will', 'just', 'should'
    }

def read_txt(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file: {e}")
        return ""

def read_pdf(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t: text += t + "\n"
    except Exception as e:
        print(f"Error reading PDF file: {e}")
    return text

def read_docx(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
    return text

def read_file(filepath):
    if not os.path.exists(filepath):
        return ""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    if ext == '.txt': return read_txt(filepath)
    elif ext == '.pdf': return read_pdf(filepath)
    elif ext == '.docx': return read_docx(filepath)
    return ""

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def detect_experience_level(text):
    """
    Heuristic to detect experience level: Junior, Mid, Senior.
    """
    text_lower = text.lower()
    if any(k in text_lower for k in ["senior", "lead", "principal", "manager", "architect", "10+", "7+"]):
        return "Senior"
    elif any(k in text_lower for k in ["mid", "intermediate", "3+", "4+", "5+"]):
        return "Mid-Level"
    elif any(k in text_lower for k in ["junior", "associate", "intern", "trainee", "entry", "0-2", "1+"]):
        return "Junior"
    return "Not Specified"

def extract_categorized_skills(text):
    """
    Extracts skills from text and categorizes them.
    """
    found_skills = {
        "technical": set(),
        "soft": set(),
        "tools": set()
    }
    
    text_processed = preprocess_text(text)
    
    # Check for multi-word skills first (simple check)
    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            if skill in text_processed:
                found_skills[category].add(skill)
                
    return found_skills

def get_semantic_similarity(text1, text2):
    """
    Calculates semantic similarity using spaCy word vectors.
    """
    if not nlp:
        return 0.0
    
    doc1 = nlp(text1[:100000]) # Limit length for performance
    doc2 = nlp(text2[:100000])
    
    return doc1.similarity(doc2)

def detect_education(text):
    """
    Heuristic to detect education level/qualifications.
    """
    text_lower = text.lower()
    qualifications = []
    
    if any(k in text_lower for k in ["phd", "doctorate", "ph.d"]):
        qualifications.append("PhD")
    if any(k in text_lower for k in ["master", "m.s", "mba", "m.tech", "post graduate"]):
        qualifications.append("Master's")
    if any(k in text_lower for k in ["bachelor", "b.s", "b.tech", "b.e", "undergraduate", "bsc"]):
        qualifications.append("Bachelor's")
    if any(k in text_lower for k in ["diploma", "associate degree"]):
        qualifications.append("Diploma")
        
    return qualifications if qualifications else ["Not Specified"]

def get_tfidf_similarity(text1, text2):
    """
    Calculates TF-IDF Cosine Similarity.
    """
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        return 0.0

def calculate_experience_match(cv_exp, jd_exp):
    """
    Returns a score (0.0 to 1.0) based on experience level match.
    """
    if jd_exp == "Not Specified":
        return 1.0 # No requirement means perfect match
    if cv_exp == jd_exp:
        return 1.0
    
    levels = ["Junior", "Mid-Level", "Senior"]
    try:
        cv_idx = levels.index(cv_exp)
        jd_idx = levels.index(jd_exp)
        diff = abs(cv_idx - jd_idx)
        if diff == 1: return 0.5 # Close match (e.g. Mid vs Senior)
        return 0.0 # Mismatch (e.g. Junior vs Senior)
    except ValueError:
        return 0.5 # Fallback if unknown format

def calculate_education_match(cv_edu, jd_edu):
    """
    Returns score (0.0 to 1.0) based on degree overlap.
    """
    # jd_edu is a list like ['Bachelor\'s', 'Not Specified']
    if "Not Specified" in jd_edu or not jd_edu:
        return 1.0
        
    # Check if any CV qualification meets any JD requirement
    # Simple strict string match for now
    match_found = False
    for req in jd_edu:
        if req in cv_edu:
            match_found = True
            break
    
    
    return 1.0 if match_found else 0.0

def calculate_cv_jd_match(cv_text, jd_text):
    """
    Advanced matching function combining:
    1. Semantic Similarity (spaCy)
    2. TF-IDF Similarity
    3. Skill Overlap
    4. Experience Match
    5. Education Match
    """
    if not cv_text or not jd_text:
        # Return a safe empty structure so the template doesn't crash
        return {
            "match_percentage": 0,
            "confidence_score": 0,
            "semantic_score": 0,
            "tfidf_score": 0,
            "skill_match_score": 0,
            "experience_level": {"cv": "Unknown", "jd": "Unknown"},
            "education": {"cv": ["Not Detected"], "jd": ["Not Specified"]},
            "skills": {
                "matched": [],
                "missing": [],
                "cv_categorized": {},
                "jd_categorized": {}
            },
            "details": "Could not read text from files."
        }

    # 1. Experience Level
    cv_exp = detect_experience_level(cv_text)
    jd_exp = detect_experience_level(jd_text)
    exp_score = calculate_experience_match(cv_exp, jd_exp)

    # 2. Skill Extraction
    cv_skills = extract_categorized_skills(cv_text)
    jd_skills = extract_categorized_skills(jd_text)
    
    # Flatten skills for overlap calc
    cv_flat = set().union(*cv_skills.values())
    jd_flat = set().union(*jd_skills.values())
    
    common_skills = cv_flat.intersection(jd_flat)
    missing_skills = jd_flat - cv_flat
    
    skill_match_ratio = len(common_skills) / len(jd_flat) if jd_flat else 0.0

    # 3. Education Match
    cv_edu = detect_education(cv_text)
    jd_edu = detect_education(jd_text)
    edu_score = calculate_education_match(cv_edu, jd_edu)

    # 4. Semantic & TF-IDF
    semantic_score = get_semantic_similarity(cv_text, jd_text)
    tfidf_score = get_tfidf_similarity(cv_text, jd_text)
    
    # Weighted Final Score Logic
    # New Standard Config:
    # Semantic: 30%, TF-IDF: 20%, Skills: 30%, Exp: 10%, Edu: 10%
    
    weights = {
        "semantic": 0.30,
        "tfidf": 0.20,
        "skills": 0.30, 
        "exp": 0.10,
        "edu": 0.10
    }

    # Dynamic adjustment for missing vectors (Low Semantic but High Skills)
    if semantic_score < 0.1 and skill_match_ratio > 0.3:
        print("Warning: Low semantic score detected. Adjusting weights.")
        # Redistribute semantic weight to Skills and TF-IDF
        weights = {
            "semantic": 0.0,
            "tfidf": 0.35,
            "skills": 0.45,
            "exp": 0.10,
            "edu": 0.10
        }

    final_score = (semantic_score * weights["semantic"]) + \
                  (tfidf_score * weights["tfidf"]) + \
                  (skill_match_ratio * weights["skills"]) + \
                  (exp_score * weights["exp"]) + \
                  (edu_score * weights["edu"])
    
    # Dampen 100% and invalid 0%
    # Ensure a small baseline for document structure match if non-empty
    if final_score < 0.05: final_score = 0.05
    if final_score > 0.98: final_score = 0.98 
    
    # Confidence Score (based on agreement between semantic and TF-IDF)
    divergence = abs(semantic_score - tfidf_score)
    confidence = 1.0 - divergence

    return {
        "match_percentage": round(final_score * 100, 2),
        "confidence_score": round(confidence * 100, 2),
        "semantic_score": round(semantic_score * 100, 2),
        "tfidf_score": round(tfidf_score * 100, 2),
        "skill_match_score": round(skill_match_ratio * 100, 2),
        "experience_level": {
            "cv": cv_exp,
            "jd": jd_exp
        },
        "education": {
            "cv": detect_education(cv_text),
            "jd": detect_education(jd_text)
        },
        "skills": {
            "matched": list(common_skills),
            "missing": list(missing_skills),
            "cv_categorized": {k: list(v) for k, v in cv_skills.items()},
            "jd_categorized": {k: list(v) for k, v in jd_skills.items()}
        }
    }

if __name__ == "__main__":
    # Sample Data
    sample_cv = """
    Experienced Python Developer with 5 years of experience in Data Science.
    Skilled in Django, Flask, SQL, and Machine Learning.
    """
    
    sample_jd = """
    We are looking for a Python Developer.
    Must have experience with Data Science, Machine Learning, and SQL.
    Nice to have: Django or Flask knowledge.
    """
    
    print("--- HR CV-JD Match Assistant ---")
    print("Processing match...")
    
    results = calculate_cv_jd_match(sample_cv, sample_jd)
    
    print(f"\nMatch Percentage: {results['match_percentage']}%")
    print(f"Confidence Score: {results['confidence_score']}%")
    print(f"Experience Level: CV={results['experience_level']['cv']}, JD={results['experience_level']['jd']}")
    print(f"Matched Skills: {', '.join(results['skills']['matched'])}")
    print(f"Missing Skills: {', '.join(results['skills']['missing'])}")
