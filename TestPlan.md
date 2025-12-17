# Test Plan: HR Assistant

## Test Environment
*   **OS:** Windows 10/11
*   **Browser:** Chrome / Edge (Latest)
*   **Server:** Local Flask Dev Server (Port 5001)

## Test Cases

| ID | Test Case | Type | Input Data | Steps | Expected Output | Actual Output |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | **Successful Match Analysis** | Positive | **CV:** `John_Doe_React.pdf` (Valid)<br>**JD:** `React_Dev_JD.docx` (Valid) | 1. Open Home Page<br>2. Upload CV<br>3. Upload JD<br>4. Submit | Redirect to Results page; Score > 0%; Skills listed. | Will match after execution. |
| **TC-02** | **Invalid File Format** | Negative | **CV:** `image.png`<br>**JD:** `job.txt` | 1. Open Home Page<br>2. Upload PNG as CV<br>3. Submit | Error message: "Allowed file types are pdf, docx, txt" | Will match after execution. |
| **TC-03** | **Missing File Upload** | Edge | **CV:** `None`<br>**JD:** `job.pdf` | 1. Open Home Page<br>2. Upload JD only<br>3. Submit | Browser validation or Error: "No selected file" | Will match after execution. |
| **TC-04** | **Zero Match (Irrelevant CV)** | Normal | **CV:** `Chef_Resume.pdf`<br>**JD:** `Accountant_JD.docx` | 1. Upload Chef CV<br>2. Upload Accountant JD<br>3. Submit | Results page loads; Score < 20%; "Key Skills Missing" populated. | Will match after execution. |
| **TC-05** | **Navigation Links** | UI | **Link:** "About" | 1. Click "About" in Navbar | Navigate to About page. | Will match after execution. |
