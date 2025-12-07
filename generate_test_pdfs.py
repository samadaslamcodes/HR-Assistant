from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_pdf(filename, text_lines):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 40
    
    for line in text_lines:
        c.drawString(40, y, line)
        y -= 20
        
    c.save()
    print(f"Created {filename}")

cv_content = [
    "John Doe",
    "Python Developer",
    "Email: john.doe@example.com",
    "",
    "Experience:",
    "- 5 years of experience in Python and Django development.",
    "- Proficient in RESTful API design and SQL databases.",
    "- Experience with Docker, Kubernetes, and AWS.",
    "- Worked on Machine Learning projects using Scikit-Learn.",
    "",
    "Skills:",
    "- Python, Django, Flask",
    "- JavaScript, React",
    "- PostgreSQL, Redis",
    "- Git, CI/CD",
    "- Communication, Team Leadership"
]

jd_content = [
    "Job Title: Senior Python Engineer",
    "",
    "Responsibilities:",
    "- Develop scalable backend services using Python and Django/Flask.",
    "- API development and integration.",
    "- Optimize database queries and performance.",
    "",
    "Requirements:",
    "- 4+ years of experience with Python.",
    "- Strong knowledge of web frameworks (Django, Flask).",
    "- Experience with cloud platforms (AWS, Azure).",
    "- Familiarity with containerization (Docker, Kubernetes).",
    "- Good communication skills and problem-solving ability.",
    "",
    "Nice to have:",
    "- Experience with React or Angular.",
    "- Machine Learning knowledge."
]

if __name__ == "__main__":
    create_pdf("sample_cv.pdf", cv_content)
    create_pdf("sample_jd.pdf", jd_content)
