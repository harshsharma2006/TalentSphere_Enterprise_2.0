"""
TalentSphere Enterprise 2.0 - Job Matcher
TF-IDF vectorization and cosine similarity candidate ranking against job requisitions.
"""

from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JobMatcher:
    @staticmethod
    def match_resume_to_jobs(resume_text: str, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks a list of open job postings against candidate profile/resume text.
        Returns sorted list of jobs with match percentages.
        """
        if not resume_text.strip() or not jobs:
            return []

        job_texts = []
        for j in jobs:
            combined = f"{j.get('title', '')} {j.get('department', '')} {j.get('description', '')} {j.get('requirements', '')} {' '.join(j.get('required_skills', []))}"
            job_texts.append(combined)

        corpus = [resume_text] + job_texts
        tfidf = TfidfVectorizer(stop_words='english', max_features=2500)
        matrix = tfidf.fit_transform(corpus)

        resume_vec = matrix[0:1]
        job_vecs = matrix[1:]

        similarities = cosine_similarity(resume_vec, job_vecs)[0]

        scored_jobs = []
        for idx, score in enumerate(similarities):
            job = dict(jobs[idx])
            job["match_score"] = round(float(score) * 100, 1)
            scored_jobs.append(job)

        scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_jobs
