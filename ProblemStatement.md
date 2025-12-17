# Problem Statement: HR Assistant

## 1. User & Pain Points
**Target User:** HR Managers, Recruiters, and Hiring Teams.

**Pain Points:**
*   **High Volume Fatigue:** Manually screening hundreds of resumes for a single opening is time-consuming and prone to "reviewer fatigue."
*   **Keyword Limitations:** Traditional ATS tools reject qualified candidates if they don't use exact keyword matches (e.g., "React" vs. "React.js").
*   **Unconscious Bias:** Human reviewers may unconsciously overlook candidates based on formatting, name, or background.
*   **Lack of Insight:** Simple "yes/no" tools don't explain *why* a candidate is a good or bad fit.

## 2. Why It Matters
Efficient hiring is critical for business success. Delayed hiring results in lost productivity, while poor hiring decisions cost time and money. By automating the initial screening with semantic intelligence, we save HR time, ensure fair evaluation for all candidates, and surface the best talent faster.

## 3. MVP Goal (Minimum Viable Product)
To build a web-based "HR Assistant" that allows users to upload a Resume (CV) and a Job Description (JD), and instantly receives a compatibility score along with a detailed breakdown of missing skills, implementing semantic matching to look beyond simple keywords.

## 4. Scope
*   **In-Scope:**
    *   Parsing PDF, DOCX, and TXT files.
    *   Semantic text analysis using NLP (SpaCy).
    *   Calculating weighted match scores (Semantic, Skills, Education, Experience).
    *   Interactive Web UI for uploads and result visualization.
    *   Basic "About" information page.

*   **Out-of-Scope:**
    *   User authentication/login system (Multi-tenancy).
    *   Database storage of historical candidates.
    *   Automated email sending to candidates.
    *   Resume background checks or verification.

## 5. Assumptions
*   Resumes are text-readable (not scanned images).
*   The Job Description is in English.
*   Users have internet access for initial model downloading (though the app runs locally).
*   The available CPU resources are sufficient for basic NLP processing.
