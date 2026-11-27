"""
TalentSphere Enterprise 2.0 - AI Interactive Mock Interview Simulator
Provides live role-specific interview simulation, automated STAR-method scoring,
keyword density verification, and actionable model responses.
"""

import re
from typing import Dict, Any, List

MOCK_INTERVIEW_BANK = {
    "Senior Backend Engineer": [
        {
            "id": 1,
            "type": "System Architecture",
            "question": "How would you design a distributed caching layer using Redis for a microservices architecture handling 100,000 requests per second?",
            "expected_concepts": ["cache invalidation", "redis cluster", "ttl", "write-through", "cache stampede", "eviction policy", "consistency"],
            "model_answer": "In a high-throughput microservices architecture, I would deploy a Redis Cluster with master-replica replication across availability zones. I'd implement a Cache-Aside or Write-Through pattern with jittered TTLs to prevent cache stampedes. For consistency, event-driven cache invalidation via Kafka/RabbitMQ guarantees eventual consistency across downstream data stores."
        },
        {
            "id": 2,
            "type": "Database & Concurrency",
            "question": "Explain database deadlocks, how relational databases detect them, and techniques to prevent them in high-concurrency payment systems.",
            "expected_concepts": ["isolation level", "acid", "lock ordering", "two-phase locking", "row lock", "retry mechanism", "idempotency"],
            "model_answer": "Deadlocks occur when two or more transactions hold locks on resources the other requires, forming a cyclic dependency. Relational engines detect this using wait-for graphs and abort the transaction with lower cost. To prevent deadlocks, we enforce strict global lock acquisition ordering, minimize transaction duration, use optimistic locking with version columns, and implement exponential backoff retries."
        }
    ],
    "Data Scientist & AI Engineer": [
        {
            "id": 3,
            "type": "Machine Learning Foundations",
            "question": "How do you detect, evaluate, and mitigate data drift and concept drift in a real-time production inference pipeline?",
            "expected_concepts": ["ks-test", "population stability index", "drift", "feature distribution", "retraining", "monitoring", "ground truth"],
            "model_answer": "Data drift refers to changes in input feature distributions P(X), whereas concept drift is changes in the relationship P(Y|X). We detect drift using statistical tests such as the Kolmogorov-Smirnov test and Population Stability Index (PSI) over rolling windows. Mitigation strategies include automated alerting via Prometheus, scheduled retraining triggers on recent golden datasets, and shadow model deployment."
        },
        {
            "id": 4,
            "type": "MLOps & Scalability",
            "question": "Explain the trade-offs between batch inference vs real-time streaming inference for an enterprise recommendation system.",
            "expected_concepts": ["latency", "throughput", "cost", "feature store", "feast", "caching", "cold start"],
            "model_answer": "Batch inference precomputes predictions offline (e.g. via Spark) and serves them from a low-latency key-value store, maximizing throughput and minimizing serving cost. However, it cannot react to intra-session behavioral signals. Real-time inference generates predictions on-the-fly via lightweight models (ONNX, Triton) and a low-latency Feature Store, providing high personalization at the cost of higher server latency and compute expenditure."
        }
    ],
    "Cloud & DevOps Engineer": [
        {
            "id": 5,
            "type": "Kubernetes & Infrastructure",
            "question": "Describe how you implement a zero-downtime blue/green or canary deployment strategy in Kubernetes for a mission-critical service.",
            "expected_concepts": ["canary", "istio", "ingress", "health check", "readiness probe", "rollback", "metrics"],
            "model_answer": "In Kubernetes, canary deployments can be orchestrated using an Ingress controller or service mesh (like Istio/Argo Rollouts). A small percentage of live traffic (e.g. 5-10%) is routed to the new canary pod replica set. Automated analysis monitors HTTP 5xx error rates and p99 latency via Prometheus. If metrics remain within SLA thresholds, traffic progressively ramps to 100%; otherwise, an automated rollback triggers instantly."
        }
    ],
    "Corporate & Behavioral (STAR Method)": [
        {
            "id": 6,
            "type": "Leadership & Incident Management",
            "question": "Describe a situation where a critical production bug reached customer-facing environments. What steps did you take to resolve it and prevent recurrence?",
            "expected_concepts": ["situation", "task", "action", "result", "post-mortem", "root cause", "monitoring", "communication"],
            "model_answer": "Situation: A database connection pool leak caused 504 gateway timeouts for 15% of checkout users. Task: I was on-call incident commander responsible for triage and restoration. Action: I rolled back the recent release within 6 minutes, drained stuck connections, and stabilized traffic. Result: Downtime was kept under 8 minutes. We held a blameless post-mortem and added automated connection pool metrics alerts and load-testing gates in CI/CD."
        }
    ]
}

class InterviewSimulator:
    """Evaluates candidate interview responses using semantic depth, STAR structure, and key concepts."""

    @classmethod
    def get_roles(cls) -> List[str]:
        return list(MOCK_INTERVIEW_BANK.keys())

    @classmethod
    def get_questions_for_role(cls, role: str) -> List[Dict[str, Any]]:
        return MOCK_INTERVIEW_BANK.get(role, MOCK_INTERVIEW_BANK["Senior Backend Engineer"])

    @classmethod
    def evaluate_response(cls, question_obj: Dict[str, Any], answer_text: str) -> Dict[str, Any]:
        """Performs multi-criteria evaluation of user interview response."""
        words = re.findall(r"\b\w+\b", answer_text)
        word_count = len(words)
        lower_ans = answer_text.lower()

        expected = question_obj.get("expected_concepts", [])
        matched_concepts = [c for c in expected if c.lower() in lower_ans]
        concept_coverage_pct = round((len(matched_concepts) / max(len(expected), 1)) * 100, 1)

        # Structure analysis (STAR indicators)
        star_indicators = {
            "Situation": any(k in lower_ans for k in ["situation", "scenario", "context", "problem", "faced", "when"]),
            "Task / Goal": any(k in lower_ans for k in ["task", "goal", "objective", "needed to", "responsible for"]),
            "Action": any(k in lower_ans for k in ["implemented", "designed", "architected", "built", "executed", "configured", "deployed"]),
            "Result / Metric": any(k in lower_ans for k in ["result", "reduced", "improved", "saved", "latency", "%", "uptime", "outcome"])
        }
        star_score = (sum(star_indicators.values()) / 4.0) * 100

        # Depth score based on technical concepts and word count
        if word_count < 25:
            depth_score = 40.0
        elif word_count < 70:
            depth_score = 70.0
        elif word_count < 150:
            depth_score = 90.0
        else:
            depth_score = 95.0

        # Composite score
        overall_score = round(0.40 * concept_coverage_pct + 0.35 * star_score + 0.25 * depth_score, 1)

        feedback_list = []
        if concept_coverage_pct >= 70:
            feedback_list.append(f"Strong technical vocabulary: Demonstrated command of {len(matched_concepts)} domain concepts.")
        else:
            feedback_list.append(f"Technical gap: Try incorporating core concepts such as: {', '.join(set(expected) - set(matched_concepts))}.")

        if star_score >= 75:
            feedback_list.append("Excellent narrative structure following the STAR method.")
        else:
            missing_star = [k for k, v in star_indicators.items() if not v]
            feedback_list.append(f"Structural suggestion: Strengthen your {', '.join(missing_star)} to provide tangible evidence of business impact.")

        return {
            "overall_score": min(100.0, max(10.0, overall_score)),
            "word_count": word_count,
            "concept_coverage_pct": concept_coverage_pct,
            "matched_concepts": matched_concepts,
            "missing_concepts": list(set(expected) - set(matched_concepts)),
            "star_indicators": star_indicators,
            "star_score": star_score,
            "feedback": feedback_list,
            "model_answer": question_obj.get("model_answer", "")
        }
