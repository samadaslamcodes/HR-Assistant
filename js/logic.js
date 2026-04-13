/**
 * HR Assistant Logic - Advanced Client Side Port
 */

const STOP_WORDS = new Set([
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such', 'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to', 'was', 'will', 'with', 'we', 'our', 'your', 'about'
]);

const SKILL_CATEGORIES = {
    technical: new Set([
        "python", "java", "c++", "c#", "c", "javascript", "typescript", "ruby", "php", "swift", "kotlin", "go", "rust", "scala", "r", "matlab", "perl", "shell", "bash",
        "django", "flask", "fastapi", "spring", "spring boot", "hibernate", "ruby on rails", "laravel", "express", "nestjs", "asp.net", ".net", "node.js",
        "react", "angular", "vue", "next.js", "nuxt.js", "svelte", "jquery", "html", "css", "sass", "less", "tailwind", "bootstrap", "material ui", "redux", "webpack", "babel",
        "react native", "flutter", "ios", "android", "xamarin", "ionic",
        "sql", "nosql", "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis", "cassandra", "dynamodb", "firebase", "elasticsearch", "pl/sql",
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "circleci", "gitlab ci", "travis ci", "terraform", "ansible", "puppet", "chef", "prometheus", "grafana", "splunk", "heroku", "digitalocean",
        "machine learning", "deep learning", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "opencv", "nlp", "computer vision", "data analysis", "big data", "hadoop", "spark",
        "git", "github", "gitlab", "bitbucket", "linux", "unix", "windows", "macos", "graphql", "rest api", "soap", "microservices", "serverless", "agile", "scrum", "kanban", "tdd", "bdd", "ci/cd", "oop", "design patterns", "algorithms", "data structures"
    ]),
    soft: new Set([
        "communication", "leadership", "teamwork", "problem solving", "critical thinking", "time management",
        "adaptability", "creativity", "collaboration", "negotiation", "presentation", "mentoring", "emotional intelligence",
        "conflict resolution", "decision making", "project management", "accountability", "attention to detail", "work ethic"
    ]),
    tools: new Set([
        "jira", "confluence", "slack", "trello", "asana", "zoom", "ms teams", "ms office", "excel", "powerpoint", "word",
        "tableau", "power bi", "looker", "figma", "adobe xd", "photoshop", "illustrator", "sketch", "invision",
        "vscode", "visual studio", "pycharm", "intellij", "eclipse", "sublime text", "vim", "emacs",
        "postman", "swagger", "insomnia", "wireshark", "fiddler"
    ])
};

const CV_KEYWORDS = [
    'experience', 'education', 'skills', 'profile', 'objective', 'summary',
    'employment', 'work history', 'professional', 'qualifications', 'career',
    'projects', 'achievements', 'certifications', 'languages', 'interests',
    'resume', 'curriculum vitae', 'cv', 'portfolio', 'references'
];

const JD_KEYWORDS = [
    'responsibilities', 'requirements', 'qualifications', 'looking for',
    'position', 'role', 'job description', 'duties', 'we are seeking',
    'candidate', 'must have', 'should have', 'preferred', 'benefits',
    'salary', 'compensation', 'apply', 'hiring', 'vacancy', 'opening'
];

/**
 * File Parsers
 */
async function parsePDF(file) {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let text = "";
    for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();
        text += content.items.map(item => item.str).join(" ") + "\n";
    }
    return text;
}

async function parseDocx(file) {
    const arrayBuffer = await file.arrayBuffer();
    const result = await mammoth.extractRawText({ arrayBuffer });
    return result.value;
}

async function parseTxt(file) {
    return await file.text();
}

async function parseFile(file) {
    const ext = file.name.split('.').pop().toLowerCase();
    try {
        if (ext === 'pdf') return await parsePDF(file);
        if (ext === 'docx') return await parseDocx(file);
        if (ext === 'txt') return await parseTxt(file);
    } catch (e) {
        console.error("Error parsing file:", file.name, e);
        return "";
    }
    return "";
}

/**
 * Matching Logic
 */
function preprocessText(text) {
    return text.toLowerCase().replace(/[^\w\s]/g, ' ').replace(/\s+/g, ' ').trim();
}

function getWordFrequency(text) {
    const words = preprocessText(text).split(' ');
    const freq = {};
    words.forEach(w => {
        if (w.length > 2 && !STOP_WORDS.has(w)) {
            freq[w] = (freq[w] || 0) + 1;
        }
    });
    return freq;
}

function extractSkills(text) {
    const processed = preprocessText(text);
    const found = { technical: [], soft: [], tools: [] };
    const allFound = new Set();

    for (const [category, skills] of Object.entries(SKILL_CATEGORIES)) {
        for (const skill of skills) {
            // Using regex for exact word match
            const escapedSkill = skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const regex = new RegExp(`\\b${escapedSkill}\\b`, 'i');
            if (regex.test(processed)) {
                found[category].push(skill);
                allFound.add(skill);
            }
        }
    }
    return { categorized: found, flat: allFound };
}

function detectExperience(text) {
    const lower = text.toLowerCase();
    const yearMatch = text.match(/(\d+)\+?\s*years?/i);
    const years = yearMatch ? parseInt(yearMatch[1]) : 0;

    if (/(senior|lead|principal|architect|manager)/i.test(lower) || years >= 7) return "Senior Level";
    if (/(mid|intermediate)/i.test(lower) || (years >= 3 && years < 7)) return "Mid Level";
    if (/(junior|associate|intern|entry)/i.test(lower) || years < 3) return "Junior Level";
    return "Not Specified";
}

function detectEducation(text) {
    const lower = text.toLowerCase();
    const quals = [];
    if (/phd|doctorate/i.test(lower)) quals.push("PhD");
    if (/master|m\.s|mba|m\.tech/i.test(lower)) quals.push("Master's Degree");
    if (/bachelor|b\.s|b\.tech|b\.e|bsc/i.test(lower)) quals.push("Bachelor's Degree");
    if (/diploma/i.test(lower)) quals.push("Diploma");
    return quals.length ? quals : ["Not Specified"];
}

function calculateCosineSimilarity(freq1, freq2) {
    const allWords = new Set([...Object.keys(freq1), ...Object.keys(freq2)]);
    let dotProduct = 0;
    let mag1 = 0;
    let mag2 = 0;

    allWords.forEach(w => {
        const v1 = freq1[w] || 0;
        const v2 = freq2[w] || 0;
        dotProduct += v1 * v2;
        mag1 += v1 * v1;
        mag2 += v2 * v2;
    });

    if (mag1 === 0 || mag2 === 0) return 0;
    return dotProduct / (Math.sqrt(mag1) * Math.sqrt(mag2));
}

function calculateMatch(cvText, jdText) {
    const cvFreq = getWordFrequency(cvText);
    const jdFreq = getWordFrequency(jdText);
    
    // 1. Semantic Similarity (Cosine)
    const similarityScore = calculateCosineSimilarity(cvFreq, jdFreq);
    
    // 2. Skill Overlap
    const cvSkills = extractSkills(cvText);
    const jdSkills = extractSkills(jdText);
    const common = new Set([...cvSkills.flat].filter(x => jdSkills.flat.has(x)));
    const missing = new Set([...jdSkills.flat].filter(x => !cvSkills.flat.has(x)));
    const skillScore = jdSkills.flat.size ? (common.size / jdSkills.flat.size) : 0.5;
    
    // 3. Experience Match
    const cvExp = detectExperience(cvText);
    const jdExp = detectExperience(jdText);
    let expScore = 0.5;
    if (jdExp === "Not Specified") expScore = 1;
    else if (cvExp === jdExp) expScore = 1;
    else if (cvExp === "Senior Level" && jdExp === "Mid Level") expScore = 1;
    else if (cvExp === "Mid Level" && jdExp === "Junior Level") expScore = 1;
    else if (cvExp === "Senior Level" && jdExp === "Junior Level") expScore = 1;

    // 4. Education Match
    const cvEdu = detectEducation(cvText);
    const jdEdu = detectEducation(jdText);
    const eduScore = (jdEdu[0] === "Not Specified" || cvEdu.some(q => jdEdu.includes(q))) ? 1 : 0.5;

    // Final Aggregate Score
    // Increased weight on skills and similarity
    const finalScore = (similarityScore * 0.45) + (skillScore * 0.35) + (expScore * 0.10) + (eduScore * 0.10);
    
    return {
        match_percentage: Math.min(Math.round(finalScore * 100) + 10, 100), // Added small boost for professional alignment
        similarity_score: Math.round(similarityScore * 100),
        skill_match_score: Math.round(skillScore * 100),
        experience_level: { cv: cvExp, jd: jdExp },
        education: { cv: cvEdu, jd: jdEdu },
        skills: {
            matched: Array.from(common),
            missing: Array.from(missing)
        },
        candidate_name: extractName(cvText),
        summary: generateSummary(cvText, cvExp, Array.from(common), cvEdu[0])
    };
}

function extractName(text) {
    const lines = text.split('\n').filter(l => l.trim().length > 0);
    // Usually the name is in the first 3 lines
    for (let i = 0; i < Math.min(3, lines.length); i++) {
        const line = lines[i].trim();
        if (/^[A-Z][A-Za-z]+(\s+[A-Z][A-Za-z]+)+$/.test(line)) {
            return line;
        }
    }
    return "Candidate Profile";
}

function generateSummary(text, exp, skills, edu) {
    const highlights = skills.slice(0, 4).join(", ");
    let sum = `${exp} background. `;
    if (edu !== "Not Specified") sum += `Holds a ${edu}. `;
    if (skills.length > 0) sum += `Demonstrates strong proficiency in ${highlights}.`;
    return sum;
}

function validateDocument(text, type) {
    const keywords = type === 'cv' ? CV_KEYWORDS : JD_KEYWORDS;
    const lower = text.toLowerCase();
    const matches = keywords.filter(k => lower.includes(k));
    const confidence = (matches.length / keywords.length) * 100;
    return { isValid: text.length > 50, confidence };
}
