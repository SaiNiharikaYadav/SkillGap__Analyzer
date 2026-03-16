from flask import Flask, render_template, request
import os
import PyPDF2
import docx
import re
import requests
import pytesseract
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
 # Set the path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Test if it works by printing the version
print("Tesseract Version:", pytesseract.get_tesseract_version())

# --- SETUP ---
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)

# Adzuna API - Replace with your actual credentials
ADZUNA_APP_ID = "49ccafa2"
ADZUNA_APP_KEY = "5e0debab14598e8b361a86ce98b95be3"

CAREER_ROLES = {
    "data scientist": ["python", "machine learning", "statistics", "deep learning", "sql", "pytorch", "tensorflow", "nlp"],
    "frontend developer": ["html", "css", "javascript", "react", "vue", "angular", "typescript", "tailwind"],
    "data analyst": ["excel", "sql", "python", "tableau", "power bi", "statistics", "data visualization"],
    "backend developer": ["python", "node.js", "express", "django", "flask", "postgresql", "mongodb", "rest api"],
    "devops engineer": ["docker", "kubernetes", "jenkins", "aws", "terraform", "ansible", "ci/cd", "linux"]
}

# --- CORE FUNCTIONS ---
def extract_text(file):
    filename = file.filename.lower()
    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join([p.extract_text() for p in reader.pages if p.extract_text()])
    elif filename.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        return pytesseract.image_to_string(Image.open(file))
    return ""

def clean_text(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-zA-Z0-9\s/]', '', text.lower())).strip()

def extract_skills(text):
    all_skills = set([s for skills in CAREER_ROLES.values() for s in skills])
    return [s for s in all_skills if re.search(rf"\b{re.escape(s)}\b", text)]

def get_recommendations(skills, city):
    if not skills: return []
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {'app_id': ADZUNA_APP_ID, 'app_key': ADZUNA_APP_KEY, 'what': " ".join(skills[:2]), 'where': city, 'results_per_page': 3, 'content-type': 'application/json'}
    try:
        return requests.get(url, params=params).json().get('results', [])
    except: return []

# --- ROUTES ---
@app.route("/")
def home():
    return render_template("index.html", roles=[r.title() for r in CAREER_ROLES.keys()])

@app.route("/analyze", methods=["POST"])
def analyze():
    # Gather inputs
    resume_file = request.files["resume"]
    jd_file = request.files["jobdesc"]
    target_role = request.form.get("target_role", "").lower()
    city = request.form.get("city", "India")

    # 1. Process files
    r_text = clean_text(extract_text(resume_file))
    j_text = clean_text(extract_text(jd_file))
    
    # 2. Skill Extraction
    r_skills = extract_skills(r_text)
    j_skills = extract_skills(j_text)
    r_skills_set, j_skills_set = set(r_skills), set(j_skills)
    
    # 3. Calculate Scores
    # Skill Match Score (0.6 weight)
    matching_skills = r_skills_set.intersection(j_skills_set)
    skill_match_score = (len(matching_skills) / len(j_skills_set)) * 100 if len(j_skills_set) > 0 else 0
    
    # Similarity Score (0.4 weight)
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([r_text, j_text])
    sim_score = round(float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]) * 100, 2)
    
    # Final Weighted ATS Score
    final_ats_score = round((0.6 * skill_match_score) + (0.4 * sim_score), 2)
    
    # 4. Gap Analysis
    missing = list(set(CAREER_ROLES.get(target_role, [])) - r_skills_set)
    matching_skills = list(r_skills_set.intersection(j_skills_set))
    return render_template("result.html", 
                           score=sim_score, 
                           ats_score=final_ats_score, # Using weighted score
                           resume_skills=r_skills, 
                           missing_skills=missing,
                           matching_skills=matching_skills,
                           target_role=target_role.title(),
                           roadmap=[{"skill": s, "url": f"https://www.youtube.com/results?search_query={s}+tutorial"} for s in missing],
                           live_jobs=get_recommendations(r_skills, city))
if __name__ == "__main__":
    app.run(debug=True, port=5500)