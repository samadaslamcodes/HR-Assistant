/**
 * HR Assistant UI - Super Stable Edition
 */

// State Management
let processedCandidates = [];
window.jdMode = 'file';

/**
 * Handle File Selection - CV
 * Linked directly via 'onchange' in HTML for 100% reliability.
 */
window.handleCvChange = function() {
    const input = document.getElementById('cv-input');
    const list = document.getElementById('cv-file-list');
    
    if (!input || !list) {
        console.error("Input or List container not found!");
        return;
    }

    const files = Array.from(input.files);
    console.log("Selected CVs:", files.length);

    if (files.length === 0) {
        list.innerHTML = '';
        return;
    }

    // Render the list of files to the UI
    list.innerHTML = files.map(f => `
        <div class="p-3 mb-2 bg-white border rounded-4 shadow-sm small d-flex justify-content-between align-items-center animate-entry">
            <span><i class="bi bi-file-earmark-person-fill text-primary me-2"></i><strong>${f.name}</strong></span>
            <span class="badge bg-light text-dark border-0 shadow-none" style="font-size: 0.7rem;">${Math.round(f.size/1024)} KB</span>
        </div>
    `).join('');
};

/**
 * Handle File Selection - JD
 * Linked directly via 'onchange' in HTML.
 */
window.handleJdChange = function() {
    const input = document.getElementById('jd-input');
    const display = document.getElementById('jd-selected-filename');
    
    if (!input || !display) return;

    const files = Array.from(input.files);
    if (files[0]) {
        console.log("Selected JD:", files[0].name);
        display.innerHTML = `
            <div class="p-3 bg-success bg-opacity-10 text-success rounded-4 border border-success border-opacity-25 small fw-bold animate-entry">
                <i class="bi bi-check-circle-fill me-2"></i>${files[0].name}
            </div>
        `;
    } else {
        display.innerHTML = '';
    }
};

/**
 * Navigation Logic
 */
window.showSection = function(sectionId) {
    const sections = ['upload-section', 'results-section', 'reviews-section', 'influence-section', 'admin-section'];
    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.setProperty('display', (id === sectionId) ? 'block' : 'none', 'important');
    });
    window.scrollTo(0, 0);
};

/**
 * Analyze Action
 */
window.startAnalysis = async function() {
    const cvInput = document.getElementById('cv-input');
    const jdInput = document.getElementById('jd-input');
    const jdTextInput = document.getElementById('jd-text-input');
    const loader = document.getElementById('loading-overlay');
    
    if (!cvInput || cvInput.files.length === 0) {
        alert("Please select at least one CV.");
        return;
    }

    loader.style.display = 'flex';

    try {
        let jdText = "";
        if (window.jdMode === 'file') {
            if (!jdInput.files[0]) throw new Error("Please select a Job Description file.");
            jdText = await parseFile(jdInput.files[0]);
        } else {
            jdText = jdTextInput.value.trim();
            if (!jdText) throw new Error("Please enter Job Description text.");
        }

        const currentResults = [];
        const files = Array.from(cvInput.files);

        for (let i = 0; i < files.length; i++) {
            const cvText = await parseFile(files[i]);
            const results = calculateMatch(cvText, jdText);
            results.filename = files[i].name;
            results.id = Date.now() + i;
            currentResults.push(results);
            processedCandidates.push(results);
        }

        renderResults(currentResults);
        showSection('results-section');

    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        loader.style.display = 'none';
    }
};

/**
 * Render Results
 */
function renderResults(results) {
    const container = document.getElementById('results-container');
    container.innerHTML = '';
    results.sort((a, b) => b.match_percentage - a.match_percentage);

    let html = `
        <div class="text-center mb-5 animate-entry">
            <h1 class="fw-bold mb-1">Match Report</h1>
            <p class="text-muted">Top recommendations for your role</p>
        </div>
    `;

    results.forEach((res, index) => {
        const color = res.match_percentage >= 70 ? '#10b981' : (res.match_percentage >= 40 ? '#f59e0b' : '#ef4444');
        html += `
            <div class="glass-card mb-4 border-start border-5 animate-entry" style="border-color: ${color}; animation-delay: ${index * 0.1}s">
                <div class="row align-items-center">
                    <div class="col-md-2 text-center"><div class="h2 fw-bold mb-0" style="color: ${color}">${res.match_percentage}%</div><small class="text-muted fw-bold">SCORE</small></div>
                    <div class="col-md-7">
                        <h4 class="fw-bold mb-1">${res.candidate_name}</h4>
                        <p class="text-muted small mb-2">${res.filename}</p>
                        <div class="d-flex gap-2">
                            <span class="badge bg-light text-dark border">Exp: ${res.experience_level.cv}</span>
                            <span class="badge bg-light text-dark border">Edu: ${res.education.cv[0]}</span>
                        </div>
                    </div>
                    <div class="col-md-3 text-md-end text-center mt-3 mt-md-0">
                        <button class="btn btn-primary rounded-pill px-4 btn-sm" onclick="window.toggleDetails('details-${res.id}')">View Details</button>
                    </div>
                </div>
                <div id="details-${res.id}" class="mt-4 pt-4 border-top" style="display: none;">
                    <p class="text-muted small mb-3">${res.summary}</p>
                    <div class="row g-3">
                        <div class="col-6"><h6 class="fw-bold text-success mb-2 small"><i class="bi bi-patch-check-fill me-1"></i>Aligned Skills</h6><div class="d-flex flex-wrap gap-1">${(res.skills.matched || []).map(s => `<span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 px-2 py-1 rounded-pill" style="font-size: 0.65rem;">${s}</span>`).join('') || '<span class="text-muted small">None</span>'}</div></div>
                        <div class="col-6"><h6 class="fw-bold text-danger mb-2 small"><i class="bi bi-patch-exclamation-fill me-1"></i>Skill Gaps</h6><div class="d-flex flex-wrap gap-1">${(res.skills.missing || []).map(s => `<span class="badge bg-danger bg-opacity-10 text-danger border border-danger border-opacity-25 px-2 py-1 rounded-pill" style="font-size: 0.65rem;">${s}</span>`).join('') || '<span class="text-muted small">None</span>'}</div></div>
                    </div>
                    <div class="row g-3 mt-2 pt-3 border-top border-light">
                        <div class="col-6 border-end">
                            <h6 class="fw-bold text-primary mb-2 small"><i class="bi bi-file-earmark-person-fill me-1"></i>CV Skills (Mentioned)</h6>
                            <div class="d-flex flex-wrap gap-1">${(res.skills.cv_skills || []).map(s => `<span class="badge bg-primary bg-opacity-10 text-primary border border-primary border-opacity-25 px-2 py-1 rounded-pill" style="font-size: 0.65rem;">${s}</span>`).join('') || '<span class="text-muted small">None</span>'}</div>
                        </div>
                        <div class="col-6">
                            <h6 class="fw-bold text-dark mb-2 small"><i class="bi bi-briefcase-fill me-1"></i>JD Skills (Required)</h6>
                            <div class="d-flex flex-wrap gap-1">${(res.skills.jd_skills || []).map(s => `<span class="badge bg-dark bg-opacity-10 text-dark border border-dark border-opacity-25 px-2 py-1 rounded-pill" style="font-size: 0.65rem;">${s}</span>`).join('') || '<span class="text-muted small">None</span>'}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    html += `<div class="text-center mt-5"><button class="btn btn-dark rounded-pill px-5 py-3" onclick="location.reload()">Start New Analysis</button></div>`;
    container.innerHTML = html;
}

window.toggleDetails = (id) => {
    const el = document.getElementById(id);
    if (el) {
        el.style.display = el.style.display === 'none' ? 'block' : 'none';
        if (el.style.display === 'block') {
            el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    }
};

// Handle Form Submission
document.addEventListener('submit', (e) => {
    if (e.target.id === 'uploadForm') {
        e.preventDefault();
        window.startAnalysis();
    }
});
