# AI Development Log: HR Match AI

This log documents the iterative process and key prompts used to build the **HR Assistant** project using agentic AI capabilities.

## Phase 1: Foundation & Core Logic
*   **Prompt 1 (System Architecture):** "Build a Flask-based web application that parses CVs (PDF/DOCX) and compares them against a Job Description. Use SpaCy for semantic matching and scikit-learn for TF-IDF keyword analysis. Separate the frontend and backend into clean directories."
*   **Prompt 2 (Advanced Matching):** "Refine the matching algorithm in `match.py`. Implement a weighted scoring system: Semantic (30%), Technical Skills (30%), TF-IDF (20%), and Experience/Education (20%). Add logic to detect seniority levels like Junior, Mid, and Senior."

## Phase 2: User Experience & Design
*   **Prompt 3 (Glassmorphism UI):** "Create a modern, premium landing page using HTML5 and Vanilla CSS. Use a Glassmorphism aesthetic with vibrant gradients, blurred backgrounds, and smooth hover animations. Ensure it feels like a high-end SaaS product."
*   **Prompt 4 (Results Visualization):** "Design a results dashboard using Chart.js to show the match percentage in a doughnut chart. Add a 'Matched Skills' vs 'Missing Skills' section with color-coded badges (Success/Danger)."

## Phase 3: Advanced Features & Refinement
*   **Prompt 5 (Candidate Identity):** "Implement an AI-based name extraction tool. If SpaCy's NER finds a 'PERSON' entity in the first 1000 characters, use that as the candidate's name. Otherwise, fallback to the first few lines of the document."
*   **Prompt 6 (Professional Summaries):** "Write a function to generate a 2-line professional summary for each candidate. It should mentions their name, experience level, and top 3 technical strengths based on the JD match."
*   **Prompt 7 (Admin Dashboard):** "Add an Admin Dashboard accessible via the navbar. Use a global list to track all processed candidates in the session. Display each candidate in a card with their name prominently shown in a clear, bordered box."

## Phase 4: Deployment & Optimization
*   **Prompt 8 (Production Readiness):** "Configure the project for Railway deployment. Create a `railway.toml` that uses Nixpacks, installs Python 3.11, and automatically downloads the `en_core_web_md` SpaCy model during the build phase."
*   **Prompt 9 (SEO & Metadata):** "Update all templates with SEO meta tags, descriptive titles, and unique IDs for automated testing. Ensure the design is fully responsive for mobile and desktop."

## Scoring Engine Analysis
The systems calculates a **Weighted Match Score** by analyzing four key dimensions of the candidate's profile:
1.  **AI Semantic Analysis (30%):** Uses SpaCy's vector embeddings to understand the "meaning" of the CV. This detects if a candidate is a match even if they use different words (e.g., "Fullstack Developer" vs "Frontend & Backend Engineer").
2.  **Skill Overlap (30%):** Performs a direct comparison of technical tools, languages, and soft skills required by the recruiter.
3.  **TF-IDF Structural Match (20%):** Uses mathematical word-frequency models from Scikit-learn to see how well the document's structure aligns with a typical professional JD.
4.  **Credential Check (20%):** Automatically parses years of experience (Junior/Mid/Senior) and educational degrees (PhD/Masters/Bachelors) to ensure the candidate meets minimum career requirements.

---
*Created and maintained by Abdul Samad with AI assistance.*
