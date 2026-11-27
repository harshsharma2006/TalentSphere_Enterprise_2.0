"""
TalentSphere Enterprise 2.0 - AI Career Mentor & Advisory Assistant
Provides contextual career guidance, transition strategies, certification recommendations,
and technical interview preparation frameworks.
"""

from typing import Dict, Any, List

ADVICE_KNOWLEDGE_BASE = [
    {
        "keywords": ["devops", "cloud", "aws", "kubernetes", "docker"],
        "category": "Cloud & DevOps Transition",
        "title": "Roadmap to Senior Cloud & DevOps Engineer",
        "guidance": (
            "1. **Core Containerization:** Master Docker multi-stage builds and Kubernetes pod lifecycle management.\n"
            "2. **Infrastructure as Code (IaC):** Build modular Terraform configurations for VPCs, EKS/GKE clusters, and IAM policies.\n"
            "3. **Observability & Metrics:** Set up Prometheus, Grafana, and OpenTelemetry instrumentation to monitor p99 latency and error budgets.\n"
            "4. **Recommended Certifications:** AWS Certified Solutions Architect Associate, followed by Certified Kubernetes Administrator (CKA)."
        )
    },
    {
        "keywords": ["ml", "machine learning", "ai", "data science", "pytorch"],
        "category": "Machine Learning & AI Engineering",
        "title": "Transitioning from Software Engineering to AI/MLOps",
        "guidance": (
            "1. **Mathematical Foundations:** Solidify linear algebra (SVD, eigenvectors), multivariable calculus (gradients), and probability distributions.\n"
            "2. **Production Pipeline Engineering:** Don't stop at Jupyter Notebooks. Build reproducible data pipelines using DVC, MLflow, and feature stores.\n"
            "3. **Low-Latency Serving:** Learn model optimization techniques such as ONNX runtime quantization, batching, and TensorRT serving.\n"
            "4. **Recommended Course:** Take TalentSphere's *Modern Machine Learning & MLOps* 24-hour masterclass."
        )
    },
    {
        "keywords": ["interview", "star", "system design", "behavioral"],
        "category": "Interview Mastery",
        "title": "Mastering Enterprise Technical & Behavioral Interviews",
        "guidance": (
            "1. **The STAR Framework:** When answering scenario questions, spend 20% on Situation/Task, 50% on specific Actions you took, and 30% on quantifiable Results.\n"
            "2. **System Design Blueprint:** Always start by clarifying functional and non-functional requirements (RPS, latency SLA, read/write ratio) before drawing architecture diagrams.\n"
            "3. **Mock Practice:** Use TalentSphere's interactive *AI Mock Interview Simulator* to rehearse answers with live keyword and depth scoring."
        )
    },
    {
        "keywords": ["salary", "negotiation", "promotion", "leveling"],
        "category": "Career Strategy & Compensation",
        "title": "Maximizing Career Trajectory & Promotion Velocity",
        "guidance": (
            "1. **Documenting Impact:** Keep a rolling 'Brag Sheet' / achievement log documenting metrics like latency reduction, cost savings, and mentored colleagues.\n"
            "2. **Aligning with OKRs:** Ensure your quarterly projects tie directly into executive departmental goals.\n"
            "3. **Closing Skill Deficits:** Leverage the 90-Day Adaptive Career Trajectory module to systematically eliminate directional competency gaps."
        )
    }
]

class AICareerMentor:
    """Intelligent advisory assistant generating tailored career guidance."""

    @classmethod
    def get_advice(cls, user_query: str) -> Dict[str, Any]:
        """Matches user query to contextual engineering mentorship advice."""
        q_lower = user_query.lower()

        best_match = None
        max_overlap = 0

        for item in ADVICE_KNOWLEDGE_BASE:
            overlap = sum(1 for kw in item["keywords"] if kw in q_lower)
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = item

        if best_match and max_overlap > 0:
            return {
                "category": best_match["category"],
                "title": best_match["title"],
                "guidance": best_match["guidance"],
                "is_matched": True
            }

        # Fallback intelligent general guidance
        return {
            "category": "Holistic Engineering Career Development",
            "title": f"Strategic Career Recommendations for '{user_query}'",
            "guidance": (
                "1. **Continuous Competency Upgrading:** Identify high-demand technologies in your department and dedicate 4-5 hours weekly to applied projects.\n"
                "2. **High-Impact Resume Optimization:** Use the *AI Resume Bullet Optimizer* to transform plain task descriptions into quantifiable business achievements.\n"
                "3. **Mock Assessment Rehearsal:** Take practice coding and system architecture assessments under timed conditions to build test confidence.\n"
                "4. **Cross-Functional Visibility:** Present technical post-mortems and architectural proposals in team engineering forums."
            ),
            "is_matched": False
        }
