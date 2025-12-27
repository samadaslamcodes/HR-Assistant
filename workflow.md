# HR Match AI: Technical Workflow & Architecture

This document provides a comprehensive overview of the technical architecture, toolset, and step-by-step workflow of the **HR Assistant** project.

---

## 🏗️ Technical Architecture

The project follows a **Client-Server Architecture** with a clear separation between the presentation layer and the intelligence engine.

### 1. Backend: The Intelligence Hub (Python & Flask)
- **Flask Framework**: Acts as the backbone, handling HTTP requests, file uploads, and routing.
- **Python Ecosystem**: Leverages high-performance libraries for data processing and text extraction.
- **File Parsers**:
    - `pdfplumber`: Accurate extraction of text from PDF CVs.
    - `python-docx`: Parsing of Microsoft Word documents.

### 2. AI Engine: The Decision Maker (NLP & Machine Learning)
- **SpaCy (Advanced NLP)**: Uses the `en_core_web_md` model. It performs **Semantic Similarity** checks using vector embeddings to understand the context/meaning of words rather than just character matching.
- **Scikit-Learn (TF-IDF)**: Implements *Term Frequency-Inverse Document Frequency* to calculate the structural relevance of the CV against the JD.
- **Smart Heuristics**: Custom logic for extracting candidate names, detecting seniority levels (Junior vs. Senior), and identifying education degrees (PhD, Masters, etc.).

### 3. Frontend: Premium User Experience (HTML, CSS, JS)
- **Design Language**: **Glassmorphism**. Uses high-end CSS effects like `backdrop-filter: blur()`, gradients, and sleek typography.
- **Data Visualization**: **Chart.js** renders interactive doughnut charts for immediate match score visibility.
- **Dynamic Content**: Vanilla JavaScript handles real-time UI updates, such as the Admin Dashboard toggles and form validations.

---

## 🔄 The 5-Step Workflow

### Step 1: Data Input (Ingestion)
The user provides CVs (PDF, DOCX, or TXT) and a Job Description (File or Text). The Flask backend validates the file types and sizes.

### Step 2: Text Normalization (Preprocessing)
The raw text is cleaned—removing special characters, converting to lowercase, and eliminating "noise" (stopwords). This ensures the AI model focuses only on meaningful skills and experience.

### Step 3: AI-Powered Analysis
- **Semantic Check**: The AI compares the *vector space* of the CV and JD. If a JD asks for "Python Expert" and the CV says "Proficient in Django/Backend," the system recognizes the high similarity.
- **Skill Extraction**: Cross-matches technical, soft, and tool-based skills against pre-defined industry categories.

### Step 4: Scoring Calibration (The 4 Pillars)
The final match percentage is calculated using a weighted average:
- **30% Semantic Similarity**: Logic and meaning.
- **30% Technical Overlap**: Hard skills matching.
- **20% TF-IDF Score**: Keyword relevance and density.
- **20% Credentials**: Validation of Experience and Education.

### Step 5: Dashboard Visualization (Output)
The results are rendered into a recruiter-friendly dashboard. It highlights:
- **Strengths**: Where the candidate excels.
- **Skill Gaps**: What is missing compared to the JD.
- **Career Path**: Their seniority level and academic background.

---

## ☁️ Deployment & Production
- **Platform**: Hosted on **Railway**.
- **Server**: Uses **Gunicorn** (Green Unicorn) for production-grade reliability.
- **Nixpacks**: Automatically configures the Python environment and downloads the required AI models (`en_core_web_md`) during the build process.

---
*Developed by Abdul Samad — Revolutionizing Recruitment with AI.*
