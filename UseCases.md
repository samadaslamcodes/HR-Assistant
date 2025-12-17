# Use Cases: HR Assistant

## High-Level Design / Data Flow
```text
[User] -> (Uploads CV & JD) -> [Frontend UI]
                                   |
                               (POST Request)
                                   v
                            [Flask Backend]
                                   |
                          (Parses Documents)
                                   v
                          [Matching Logic] <--> [NLP Model / Skill DB]
                                   |
                            (Returns JSON)
                                   v
[User] <- (View Results) <- [Frontend UI]
```

---

## Use Case 1: Analyze Candidate Compatibility
*   **Actor:** HR Recruiter
*   **Trigger:** Recruiter receives a new application and needs to check fit against a JD.
*   **Preconditions:**
    *   App is running.
    *   Recruiter has the CV (PDF/DOCX) and JD (PDF/DOCX/TXT) files ready.
*   **Main Flow:**
    1.  Recruiter navigates to the Home/Upload page.
    2.  Recruiter clicks "Upload Resume" and selects the candidate's file.
    3.  Recruiter clicks "Upload Job Description" and selects the relevant file.
    4.  Recruiter clicks the "Analyze Compatibility" button.
    5.  System parses both files and calculates the match score.
    6.  System redirects to the Results page displaying the score and skill gaps.
*   **Alternate Flow (Invalid File):**
    1.  Recruiter uploads an unsupported file type (e.g., .jpg).
    2.  System displays an error message: "Invalid file format."
    3.  Use case restarts at step 2.

## Use Case 2: Identify Missing Skills
*   **Actor:** HR Recruiter
*   **Trigger:** Recruiter wants to know *why* a candidate got a specific score.
*   **Preconditions:** Analysis (Use Case 1) has been completed.
*   **Main Flow:**
    1.  On the Results page, Recruiter scrolls down to the "Missing Skills" section.
    2.  Recruiter views the list of skills found in the JD but not in the CV.
    3.  Recruiter uses this list to prepare interview questions (e.g., "I see you haven't mentioned Docker, do you have experience with it?").

## Use Case 3: View Project Information
*   **Actor:** New User / Stakeholder
*   **Trigger:** User wants to understand how the matching algorithm works.
*   **Preconditions:** None.
*   **Main Flow:**
    1.  User clicks the "About" link in the navigation bar.
    2.  System renders the About page.
    3.  User reads the explanation of the "Matching Engine" and "Tech Stack."
    4.  User clicks "Home" to return to the main tool.
