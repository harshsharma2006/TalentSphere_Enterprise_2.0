"""
TalentSphere Enterprise 2.0 - Resume Analyzer
Handles document ingestion (PDF, DOCX, TXT), contact extraction, and skill parsing.
"""

import re
import io
from typing import Dict, Any, List
from pypdf import PdfReader
import docx

# Standard enterprise skill dictionary for parsing
COMMON_SKILLS_TAXONOMY = {
    # Engineering & Tech
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift",
    "html", "css", "react", "vue", "angular", "node.js", "django", "fastapi", "flask", "spring", "express",
    "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "sqlite",
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ci/cd", "linux",
    # Data & AI
    "machine learning", "deep learning", "nlp", "computer vision", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "data analysis", "tableau", "power bi", "statistics", "data engineering",
    # Management & Soft Skills
    "agile", "scrum", "project management", "leadership", "communication", "problem solving",
    "critical thinking", "collaboration", "system design", "product management", "jira"
}

class ResumeAnalyzer:
    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes, filename: str) -> str:
        """Extracts plain text from PDF, DOCX, or TXT file bytes."""
        text = ""
        lower_name = filename.lower()
        try:
            if lower_name.endswith(".pdf"):
                reader = PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            elif lower_name.endswith(".docx"):
                doc = docx.Document(io.BytesIO(file_bytes))
                for p in doc.paragraphs:
                    text += p.text + "\n"
            else:
                text = file_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            text = f"Error extracting text from file: {str(e)}"
        
        return text.strip()

    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        """Extracts email and phone numbers from resume text using regex patterns."""
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)

        return {
            "email": emails[0] if emails else "",
            "phone": phones[0] if phones else ""
        }

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Matches skill taxonomy keywords against document text."""
        lower_text = text.lower()
        matched = []
        for skill in COMMON_SKILLS_TAXONOMY:
            # Word boundary matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, lower_text):
                matched.append(skill.title() if len(skill) > 3 else skill.upper())
        return sorted(list(set(matched)))

    @staticmethod
    def parse_resume(file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Full resume parsing pipeline."""
        text = ResumeAnalyzer.extract_text_from_bytes(file_bytes, filename)
        contacts = ResumeAnalyzer.extract_contact_info(text)
        skills = ResumeAnalyzer.extract_skills(text)
        word_count = len(text.split())

        return {
            "filename": filename,
            "raw_text": text,
            "word_count": word_count,
            "email": contacts["email"],
            "phone": contacts["phone"],
            "detected_skills": skills
        }
