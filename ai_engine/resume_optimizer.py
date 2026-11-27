"""
TalentSphere Enterprise 2.0 - AI Resume Bullet Optimizer
Transforms generic candidate bullet points into high-impact, ATS-optimized,
quantifiable STAR (Situation, Task, Action, Result) achievement statements.
"""

import re
from typing import Dict, Any, List

STRONG_ACTION_VERBS = [
    "Architected", "Spearheaded", "Engineered", "Orchestrated", "Pioneered",
    "Streamlined", "Accelerated", "Automated", "Optimized", "Overhauled",
    "Formulated", "Revamped", "Designed", "Implemented", "Executed"
]

METRICS_PATTERNS = [
    r"\d+%", r"\$\d+", r"\d+\s*(ms|seconds|minutes|hours|days)",
    r"\d+\s*(users|clients|teams|microservices|endpoints|records|transactions)"
]

TECH_KEYWORDS_DICT = {
    "python": ["Python", "FastAPI", "Django", "PyTorch", "NumPy", "Pandas", "Scikit-Learn"],
    "cloud": ["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform", "Microservices", "GCP", "Azure"],
    "database": ["PostgreSQL", "MongoDB", "Redis", "SQL", "Database Optimization", "Query Indexing"],
    "frontend": ["React", "TypeScript", "Next.js", "Redux", "Tailwind CSS", "Web Vitals"],
    "data": ["Data Pipeline", "ETL", "Apache Spark", "Airflow", "Predictive Modeling", "Feature Engineering"],
    "security": ["OAuth2", "JWT", "RBAC", "Zero Trust", "SSL/TLS", "SOC-2", "GDPR"]
}

class ResumeBulletOptimizer:
    """Intelligent bullet point refactoring and ATS impact scoring."""

    @classmethod
    def analyze_bullet(cls, raw_text: str) -> Dict[str, Any]:
        """Analyzes a bullet point for active verbs, metrics, and technical keywords."""
        words = re.findall(r"\b\w+\b", raw_text)
        first_word = words[0].capitalize() if words else ""
        has_action_verb = first_word in STRONG_ACTION_VERBS

        # Check for quantifiable metrics
        has_metrics = any(re.search(p, raw_text, re.IGNORECASE) for p in METRICS_PATTERNS)

        # Detect technical keywords
        detected_keywords = []
        lower_text = raw_text.lower()
        for cat, kw_list in TECH_KEYWORDS_DICT.items():
            for kw in kw_list:
                if kw.lower() in lower_text and kw not in detected_keywords:
                    detected_keywords.append(kw)

        # Calculate impact score (0-100)
        score = 40.0
        if has_action_verb:
            score += 20.0
        if has_metrics:
            score += 25.0
        if len(detected_keywords) >= 2:
            score += 15.0

        return {
            "raw_text": raw_text,
            "word_count": len(words),
            "lead_verb": first_word,
            "has_action_verb": has_action_verb,
            "has_metrics": has_metrics,
            "detected_keywords": detected_keywords,
            "impact_score": min(100.0, score)
        }

    @classmethod
    def optimize_bullet(cls, raw_text: str, domain: str = "Backend / Cloud Engineering") -> List[Dict[str, str]]:
        """Generates 3 ATS-optimized, high-impact STAR variants from a candidate's input."""
        analysis = cls.analyze_bullet(raw_text)
        detected = analysis["detected_keywords"] or ["Python", "Cloud Architecture", "REST APIs"]

        kw1 = detected[0] if len(detected) > 0 else "Python"
        kw2 = detected[1] if len(detected) > 1 else "Docker & Kubernetes"
        kw3 = detected[2] if len(detected) > 2 else "PostgreSQL"

        variants = [
            {
                "style": "Performance & Latency Optimization",
                "text": f"Architected high-throughput backend services using {kw1} and {kw2}, reducing average API response latency by 38% and eliminating memory overhead across production workloads.",
                "action_verb": "Architected",
                "metric": "38% latency reduction",
                "framework": "STAR (Action + Technical Tooling + Quantified Result)"
            },
            {
                "style": "Scalability & Microservices Automation",
                "text": f"Spearheaded automated CI/CD deployment pipelines incorporating {kw1} and {kw3}, scaling system throughput to 25,000+ concurrent transactions with 99.99% service availability.",
                "action_verb": "Spearheaded",
                "metric": "25,000+ concurrent transactions, 99.99% availability",
                "framework": "STAR (Leadership + Enterprise Scale + Metric)"
            },
            {
                "style": "System Reliability & Defect Reduction",
                "text": f"Overhauled legacy service infrastructure using containerized {kw2} orchestration, accelerating release velocity by 3x and slashing defect ticket turnaround by 45%.",
                "action_verb": "Overhauled",
                "metric": "3x release velocity, 45% defect reduction",
                "framework": "STAR (Problem Resolution + Tooling + Business ROI)"
            }
        ]

        return variants
