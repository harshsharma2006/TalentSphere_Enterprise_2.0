"""
TalentSphere Enterprise 2.0 - Career Recommender
AI recommendations for career roadmaps based on skills, RIASEC traits, and interests.
"""

from typing import List, Dict, Any

CAREER_PROFILES = [
    {
        "role": "Cloud DevOps Engineer",
        "category": "Cloud & Infrastructure",
        "description": "Design and manage scalable cloud platforms, automated CI/CD pipelines, and infrastructure as code.",
        "skills": ["AWS", "Docker", "Kubernetes", "Linux", "Git", "Terraform", "CI/CD", "Python"],
        "riasec": ["Realistic", "Investigative"]
    },
    {
        "role": "Full-Stack Software Engineer",
        "category": "Software Engineering",
        "description": "Develop client-facing web applications and robust backend APIs using modern frameworks.",
        "skills": ["Python", "FastAPI", "React", "JavaScript", "SQL", "Git", "Docker", "HTML", "CSS"],
        "riasec": ["Investigative", "Artistic"]
    },
    {
        "role": "AI / Machine Learning Engineer",
        "category": "Data Science & AI",
        "description": "Train, deploy, and evaluate deep learning models and predictive analytics systems.",
        "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "SQL"],
        "riasec": ["Investigative", "Realistic"]
    },
    {
        "role": "Cybersecurity Analyst",
        "category": "Security & Defense",
        "description": "Protect critical infrastructure from vulnerabilities, monitor threat alerts, and perform security audits.",
        "skills": ["Linux", "Networking", "Cryptography", "Python", "Incident Response", "SIEM"],
        "riasec": ["Investigative", "Conventional"]
    },
    {
        "role": "Product & Agile Project Manager",
        "category": "Product Leadership",
        "description": "Lead cross-functional engineering teams, define sprint roadmaps, and communicate business metrics.",
        "skills": ["Agile", "Scrum", "Project Management", "Leadership", "Communication", "Jira"],
        "riasec": ["Enterprising", "Social"]
    }
]

class CareerRecommender:
    @staticmethod
    def recommend_roles(user_skills: List[str], riasec_traits: List[str] = None) -> List[Dict[str, Any]]:
        """
        Recommends best-fit career roles based on user skill overlap and RIASEC personality traits.
        """
        clean_user_skills = set(s.lower() for s in user_skills)
        recommendations = []

        for profile in CAREER_PROFILES:
            profile_skills = set(s.lower() for s in profile["skills"])
            overlap = clean_user_skills.intersection(profile_skills)
            skill_score = (len(overlap) / len(profile_skills)) * 80 if profile_skills else 0

            trait_bonus = 0
            if riasec_traits:
                matched_traits = [t for t in riasec_traits if t in profile["riasec"]]
                trait_bonus = (len(matched_traits) / len(profile["riasec"])) * 20

            total_score = round(min(100.0, skill_score + trait_bonus), 1)

            recommendations.append({
                "role": profile["role"],
                "category": profile["category"],
                "description": profile["description"],
                "match_percentage": total_score,
                "matched_skills": [s.title() for s in overlap],
                "missing_skills": [s for s in profile["skills"] if s.lower() not in clean_user_skills]
            })

        recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
        return recommendations
