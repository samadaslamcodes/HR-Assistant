import re
from typing import Tuple

# CV-specific keywords and patterns
CV_KEYWORDS = {
    'experience', 'education', 'skills', 'profile', 'objective', 'summary',
    'employment', 'work history', 'professional', 'qualifications', 'career',
    'projects', 'achievements', 'certifications', 'languages', 'interests',
    'resume', 'curriculum vitae', 'cv', 'portfolio', 'references'
}

# JD-specific keywords and patterns
JD_KEYWORDS = {
    'responsibilities', 'requirements', 'qualifications', 'looking for',
    'position', 'role', 'job description', 'duties', 'we are seeking',
    'candidate', 'must have', 'should have', 'preferred', 'benefits',
    'salary', 'compensation', 'apply', 'hiring', 'vacancy', 'opening'
}

# Contact information patterns (more common in CVs)
CONTACT_PATTERNS = [
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
    r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # Phone (US format)
    r'\b\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',  # International phone
    r'\blinkedin\.com/in/[\w-]+\b',  # LinkedIn
    r'\bgithub\.com/[\w-]+\b',  # GitHub
]

# Company/hiring patterns (more common in JDs)
COMPANY_PATTERNS = [
    r'\b(company|organization|firm|corporation|startup|enterprise)\b',
    r'\b(we are|we\'re|our team|our company|join us|about us)\b',
    r'\b(apply now|send resume|submit application|how to apply)\b',
]


def preprocess_text(text: str) -> str:
    """Normalize text for analysis."""
    return text.lower().strip()


def count_keywords(text: str, keywords: set) -> int:
    """Count how many keywords from the set appear in the text."""
    text_lower = preprocess_text(text)
    count = 0
    for keyword in keywords:
        if keyword in text_lower:
            count += 1
    return count


def has_contact_info(text: str) -> bool:
    """Check if text contains contact information patterns."""
    for pattern in CONTACT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def has_company_patterns(text: str) -> bool:
    """Check if text contains company/hiring patterns."""
    for pattern in COMPANY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def validate_cv(text: str) -> Tuple[bool, float, str]:
    """
    Validate if the text is a CV/Resume.
    
    Returns:
        (is_valid, confidence, reason)
    """
    if not text or len(text.strip()) < 50:
        return False, 0.0, "Document is too short (minimum 50 characters required)"
    
    word_count = len(text.split())
    if word_count < 50:
        return False, 0.0, "Document is too short (minimum 50 words required)"
    
    # Count CV-specific keywords
    cv_keyword_count = count_keywords(text, CV_KEYWORDS)
    
    # Check for contact information (strong CV indicator)
    has_contact = has_contact_info(text)
    
    # Check for company patterns (suggests it might be a JD instead)
    has_company = has_company_patterns(text)
    
    # Calculate confidence score
    confidence = 0.0
    
    # Keyword matching (max 50 points)
    confidence += min(cv_keyword_count * 10, 50)
    
    # Contact information (30 points)
    if has_contact:
        confidence += 30
    
    # Penalize if it looks like a JD (reduce confidence)
    if has_company:
        confidence -= 20
    
    # Check for typical CV sections
    text_lower = preprocess_text(text)
    cv_sections = ['experience', 'education', 'skills']
    sections_found = sum(1 for section in cv_sections if section in text_lower)
    confidence += sections_found * 10  # 10 points per section
    
    # Normalize confidence to 0-100
    confidence = max(0, min(confidence, 100))
    
    # Decision threshold
    is_valid = confidence >= 60
    
    if is_valid:
        reason = f"Valid CV detected (confidence: {confidence:.1f}%)"
    else:
        if cv_keyword_count < 3:
            reason = "This doesn't appear to be a CV. Missing typical CV sections like experience, education, or skills."
        elif has_company:
            reason = "This looks more like a Job Description than a CV."
        else:
            reason = f"Document doesn't match CV format (confidence: {confidence:.1f}%)"
    
    return is_valid, confidence, reason


def validate_jd(text: str) -> Tuple[bool, float, str]:
    """
    Validate if the text is a Job Description.
    
    Returns:
        (is_valid, confidence, reason)
    """
    if not text or len(text.strip()) < 50:
        return False, 0.0, "Document is too short (minimum 50 characters required)"
    
    word_count = len(text.split())
    if word_count < 50:
        return False, 0.0, "Document is too short (minimum 50 words required)"
    
    # Count JD-specific keywords
    jd_keyword_count = count_keywords(text, JD_KEYWORDS)
    
    # Check for company/hiring patterns (strong JD indicator)
    has_company = has_company_patterns(text)
    
    # Check for contact information (suggests it might be a CV instead)
    has_contact = has_contact_info(text)
    
    # Calculate confidence score
    confidence = 0.0
    
    # Keyword matching (max 50 points)
    confidence += min(jd_keyword_count * 10, 50)
    
    # Company/hiring patterns (30 points)
    if has_company:
        confidence += 30
    
    # Penalize if it looks like a CV (reduce confidence)
    if has_contact:
        confidence -= 20
    
    # Check for typical JD sections
    text_lower = preprocess_text(text)
    jd_sections = ['responsibilities', 'requirements', 'qualifications']
    sections_found = sum(1 for section in jd_sections if section in text_lower)
    confidence += sections_found * 10  # 10 points per section
    
    # Normalize confidence to 0-100
    confidence = max(0, min(confidence, 100))
    
    # Decision threshold
    is_valid = confidence >= 60
    
    if is_valid:
        reason = f"Valid Job Description detected (confidence: {confidence:.1f}%)"
    else:
        if jd_keyword_count < 3:
            reason = "This doesn't look like a Job Description. Missing typical JD sections like responsibilities, requirements, or qualifications."
        elif has_contact:
            reason = "This looks more like a CV/Resume than a Job Description."
        else:
            reason = f"Document doesn't match Job Description format (confidence: {confidence:.1f}%)"
    
    return is_valid, confidence, reason


def get_document_type(text: str) -> str:
    """
    Auto-detect document type.
    
    Returns:
        "CV", "JD", or "UNKNOWN"
    """
    cv_valid, cv_conf, _ = validate_cv(text)
    jd_valid, jd_conf, _ = validate_jd(text)
    
    if cv_valid and cv_conf > jd_conf:
        return "CV"
    elif jd_valid and jd_conf > cv_conf:
        return "JD"
    elif cv_conf > 40 or jd_conf > 40:
        # Partial match - return the higher one
        return "CV" if cv_conf > jd_conf else "JD"
    else:
        return "UNKNOWN"


# Test function
if __name__ == "__main__":
    # Test CV
    sample_cv = """
    John Doe
    Email: john.doe@example.com
    Phone: +1-555-123-4567
    
    Professional Summary:
    Experienced software engineer with 5 years of experience in Python development.
    
    Work Experience:
    - Senior Developer at Tech Corp (2020-2023)
    - Junior Developer at StartupXYZ (2018-2020)
    
    Education:
    Bachelor of Science in Computer Science
    
    Skills:
    Python, JavaScript, React, Django, SQL
    """
    
    # Test JD
    sample_jd = """
    Job Title: Senior Python Developer
    
    We are looking for an experienced Python developer to join our team.
    
    Responsibilities:
    - Develop and maintain web applications
    - Write clean, maintainable code
    - Collaborate with team members
    
    Requirements:
    - 5+ years of Python experience
    - Strong knowledge of Django/Flask
    - Excellent communication skills
    
    Benefits:
    - Competitive salary
    - Health insurance
    - Remote work options
    
    How to Apply:
    Send your resume to careers@company.com
    """
    
    # Test random text
    random_text = "This is just some random text that doesn't look like a CV or JD."
    
    print("=== Testing CV Validation ===")
    is_valid, conf, reason = validate_cv(sample_cv)
    print(f"Valid: {is_valid}, Confidence: {conf:.1f}%, Reason: {reason}")
    print(f"Auto-detected type: {get_document_type(sample_cv)}\n")
    
    print("=== Testing JD Validation ===")
    is_valid, conf, reason = validate_jd(sample_jd)
    print(f"Valid: {is_valid}, Confidence: {conf:.1f}%, Reason: {reason}")
    print(f"Auto-detected type: {get_document_type(sample_jd)}\n")
    
    print("=== Testing Random Text ===")
    is_valid, conf, reason = validate_cv(random_text)
    print(f"CV Valid: {is_valid}, Confidence: {conf:.1f}%, Reason: {reason}")
    is_valid, conf, reason = validate_jd(random_text)
    print(f"JD Valid: {is_valid}, Confidence: {conf:.1f}%, Reason: {reason}")
    print(f"Auto-detected type: {get_document_type(random_text)}")
