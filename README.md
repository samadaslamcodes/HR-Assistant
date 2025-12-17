# HR Assistant

**HR Assistant** is an intelligent, AI-powered tool designed to streamline the recruitment process. It automatically analyzes resumes (CVs) against Job Descriptions (JDs) using Natural Language Processing (NLP) to provide a weighted compatibility score and actionable insights.

## 🚀 Features
*   **AI Semantic Matching:** Uses SpaCy to understand context, not just keywords.
*   **Multi-Format Support:** Works with PDF, DOCX, and TXT files.
*   **Detailed Analytics:** Breakdown of Match Score, Missing Skills, and Experience Level.
*   **Modern UI:** Clean, Glassmorphism-based design for a premium user experience.
*   **Privacy Focused:** Runs locally on your machine; no data is uploaded to the cloud.

## 🛠️ Tech Stack
*   **Backend:** Python, Flask
*   **AI/NLP:** SpaCy, Scikit-Learn (TF-IDF), NumPy
*   **File Parsing:** PDFPlumber, Python-Docx
*   **Frontend:** HTML5, CSS3 (Glassmorphism), JavaScript, Chart.js

## 📦 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/samadaslamcodes/Hr-Assistant.git
    cd "Hr Assistant"
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLP Model**
    ```bash
    python -m spacy download en_core_web_md
    ```

4.  **Run the Application**
    ```bash
    cd backend
    python app.py
    ```
    The app will start at `http://127.0.0.1:5001`.

## 📂 Project Structure
```
Hr Assistant/
├── backend/
│   ├── app.py           # Main Flask Server
│   ├── match.py         # Core Matching Logic
├── frontend/
│   ├── static/          # CSS, Images
│   ├── templates/       # HTML files (upload, results, about)
├── uploads/             # Temp storage for processing
├── requirements.txt     # Python Dependencies
└── README.md            # Project Documentation
```

## 📝 Example
*   **Input:** Check a "Junior Python Developer" CV against a "Senior Data Scientist" JD.
*   **Output:** Likely a **Low Score** (< 40%). The system will flag missing "Data Science", "Machine Learning", and "Senior Experience" tags.
