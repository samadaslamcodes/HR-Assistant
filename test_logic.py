
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from match import calculate_cv_jd_match, read_file

def test_match():
    cv_path = os.path.join('uploads', 'cv_1_high_match_cv.pdf')
    jd_text = "We are looking for a Python Developer with experience in Django and SQL."
    
    if not os.path.exists(cv_path):
        print(f"CV not found at {cv_path}")
        return

    print(f"Reading CV from {cv_path}...")
    cv_text = read_file(cv_path)
    print(f"CV text length: {len(cv_text)}")
    
    print("Calculating match...")
    results = calculate_cv_jd_match(cv_text, jd_text)
    
    print(f"Match Score: {results['match_percentage']}%")
    print(f"Common Skills: {results['skills']['matched']}")

if __name__ == "__main__":
    test_match()
