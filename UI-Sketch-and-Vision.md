# UI Sketch & Vision

## 1. Design Philosophy
The future UI of **HR Assistant** will double down on **Immersive Minimalism**.
*   **Glassmorphism 2.0:** Deeper blurs, subtle noise textures, and dynamic gradients that shift based on the match score (e.g., Red gradient for low match, Green for high).
*   **Dashboard-First:** Moving away from a simple "Upload -> Result" flow to a persistent dashboard where recruiters can manage open roles.

## 2. Future Wireframe (ASCII Sketch)

```text
+-------------------------------------------------------------+
|  [Logo] HR Assistant       [Dashboard] [Jobs] [Candidates]  |
+-------------------------------------------------------------+
|                                                             |
|  Welcome back, Recruiter!                                   |
|                                                             |
|  +---------------------------+  +------------------------+  |
|  |  Active Job: Python Dev   |  |  Quick Upload          |  |
|  |  [View Job Description]   |  |  [ Drag & Drop CV ]    |  |
|  +---------------------------+  |  [ Select Job ID  ]    |  |
|                                 |  [   ANALYZE      ]    |  |
|  +---------------------------+  +------------------------+  |
|  |  Recent Matches           |                              |
|  |  1. Samad (92%) [View] |                              |
|  |  2. Ali Smi (85%) [View] |                              |
|  |  3. Daniyal (42%) [View] |                              |
|  +---------------------------+                              |
|                                                             |
+-------------------------------------------------------------+
```

## 3. Key UI Decisions
*   **Split Screen Results:** Instead of a long scroll, the "Results" page should eventually show the CV text on the left and the AI analysis on the right, highlighting keywords in real-time overlapping the original document.
*   **Dark Mode Toggle:** Essential for developer/recruiter eye strain reduction.
*   **Micro-Interactions:** Buttons should have haptic-like visual feedback (shrink on click) to feel responsive.
