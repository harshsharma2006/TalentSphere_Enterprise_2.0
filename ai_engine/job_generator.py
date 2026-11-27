"""
TalentSphere Enterprise 2.0 - AI Job Requisition Generator
Generates structured enterprise job descriptions, skill matrices, responsibilities,
and competitive compensation benchmarks based on role profile and seniority.
"""

from typing import Dict, Any, List

ROLE_TEMPLATES = {
    "software": {
        "title_default": "Senior Backend Engineer",
        "skills": "Python, FastAPI, Docker, Kubernetes, PostgreSQL, Redis, Microservices, CI/CD, AWS",
        "experience": 4.5,
        "salary_min": 110000.0,
        "salary_max": 145000.0,
        "description": "We are seeking an experienced Backend Engineer to lead the architecture, design, and deployment of mission-critical distributed microservices. You will collaborate with cross-functional teams to build resilient REST/gRPC APIs, optimize database queries, and champion DevOps best practices.",
        "responsibilities": [
            "Architect and maintain high-throughput backend services using Python and containerized microservices.",
            "Design scalable relational and NoSQL database schemas with automated migration pipelines.",
            "Implement automated unit, integration, and performance test suites ensuring 90%+ code coverage.",
            "Collaborate with DevOps to streamline CI/CD deployments across multi-cloud environments."
        ]
    },
    "ai_ml": {
        "title_default": "Lead Machine Learning Engineer",
        "skills": "Python, PyTorch, Scikit-learn, MLOps, Docker, MLflow, Feature Store, SQL, Ray",
        "experience": 5.0,
        "salary_min": 135000.0,
        "salary_max": 175000.0,
        "description": "Join our AI innovation team to architect and scale predictive models, NLP screening algorithms, and automated competency gap diagnostics. You will bridge experimental data science with production-grade inference microservices.",
        "responsibilities": [
            "Design, train, and deploy enterprise machine learning pipelines with low-latency inference.",
            "Implement automated data drift, model drift, and performance monitoring telemetry.",
            "Collaborate with product leadership to translate business objectives into algorithmic solutions.",
            "Conduct code and architecture reviews championing clean code and mathematical rigor."
        ]
    },
    "devops": {
        "title_default": "Senior Cloud DevOps & SRE Engineer",
        "skills": "Kubernetes, Terraform, AWS, Docker, Prometheus, Grafana, Linux, CI/CD, Python",
        "experience": 4.0,
        "salary_min": 115000.0,
        "salary_max": 150000.0,
        "description": "Lead the modernization of our infrastructure as code (IaC), container orchestration, and observability stack. You will ensure 99.99% availability, zero-downtime deployment pipelines, and zero-trust security postures.",
        "responsibilities": [
            "Manage enterprise Kubernetes clusters across production and staging environments.",
            "Automate infrastructure provisioning using modular Terraform and GitOps practices.",
            "Build proactive alerting and observability dashboards using Prometheus and Grafana.",
            "Conduct disaster recovery rehearsals, chaos engineering tests, and security audits."
        ]
    },
    "hr": {
        "title_default": "Associate Talent Acquisition Specialist",
        "skills": "Technical Sourcing, Candidate Screening, Boolean Search, Applicant Tracking Systems, Behavioral Interviewing",
        "experience": 2.0,
        "salary_min": 65000.0,
        "salary_max": 88000.0,
        "description": "Drive high-impact talent acquisition across technical and corporate departments. You will manage end-to-end recruitment pipelines, leverage AI screening intelligence, and deliver exceptional candidate experiences.",
        "responsibilities": [
            "Source, engage, and screen qualified talent for technical and corporate vacancies.",
            "Leverage TalentSphere AI matching intelligence to evaluate resume hygiene and competency fit.",
            "Coordinate interview loops with hiring managers and lead offer negotiation workflows.",
            "Analyze recruitment telemetry to optimize time-to-hire and diversity metrics."
        ]
    }
}

class JobRequisitionGenerator:
    """Generates structured job requisitions based on industry benchmarks."""

    @classmethod
    def generate_job_spec(cls, role_type: str, custom_title: str = "", seniority: str = "Senior") -> Dict[str, Any]:
        key = "software"
        if "data" in role_type.lower() or "ml" in role_type.lower() or "ai" in role_type.lower():
            key = "ai_ml"
        elif "cloud" in role_type.lower() or "devops" in role_type.lower() or "infra" in role_type.lower():
            key = "devops"
        elif "hr" in role_type.lower() or "talent" in role_type.lower() or "recruit" in role_type.lower():
            key = "hr"

        tmpl = ROLE_TEMPLATES[key]
        title = custom_title.strip() if custom_title.strip() else tmpl["title_default"]

        exp = tmpl["experience"]
        s_min = tmpl["salary_min"]
        s_max = tmpl["salary_max"]

        if seniority == "Lead / Principal":
            exp += 2.0
            s_min += 25000.0
            s_max += 35000.0
        elif seniority == "Junior / Associate":
            exp = max(1.0, exp - 2.5)
            s_min = max(45000.0, s_min - 35000.0)
            s_max = max(65000.0, s_max - 40000.0)

        full_desc = f"{tmpl['description']}\n\nKey Responsibilities:\n" + "\n".join([f"• {r}" for r in tmpl["responsibilities"]])

        return {
            "title": title,
            "required_skills": tmpl["skills"],
            "experience_required": exp,
            "min_salary": s_min,
            "max_salary": s_max,
            "description": full_desc,
            "employment_type": "Full-Time",
            "seniority": seniority
        }
