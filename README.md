# SkillGapAI 🚀

SkillGapAI is an intelligent career-tech platform designed to automate the process of career alignment. By analyzing the "gap" between a user's current resume and specific job market demands, the system provides a data-driven roadmap for upskilling and improves Applicant Tracking System (ATS) compatibility.

## 🌟 Key Features

* **Multi-Modal Resume Parsing:** High-accuracy text extraction from Images (OCR), PDFs, and Word documents using **Tesseract**, **PyPDF2**, and **python-docx**.
* **Dual-Engine Scoring Logic:**
    * **Keyword Extraction:** Scans for technical competencies against a predefined career taxonomy.
    * **Semantic Similarity:** Utilizes **TF-IDF Vectorization** and **Cosine Similarity** to measure contextual alignment with Job Descriptions (JD).
* **Weighted ATS Simulation:** Mimics corporate hiring software by calculating a final "Match Score" based on technical skills (60%) and semantic relevance (40%).
* **Dynamic Learning Roadmaps:** Automatically generates personalized upskilling paths with direct links to curated educational content (YouTube tutorials) for every missing skill.
* **Live Market Integration:** Real-time job fetching via the **Adzuna API**, matching users to live openings in their preferred city based on their verified skills.

## 🛠️ Technical Architecture

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | Flask (Python) |
| **NLP & Machine Learning** | Scikit-learn (TF-IDF, Cosine Similarity), NLTK, Regex |
| **Data Extraction** | Pytesseract (OCR), PyPDF2, python-docx |
| **External APIs** | Adzuna (Job Search)|
| **Frontend** | HTML5, CSS3 |

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SaiNiharikaYadav/SkillGapAI.git](https://github.com/SaiNiharikaYadav/SkillGapAI.git)
   cd SkillGapAI
