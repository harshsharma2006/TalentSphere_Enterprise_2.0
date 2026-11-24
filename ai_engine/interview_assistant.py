"""
TalentSphere Enterprise 2.0 - Interview Assistant
Mock technical, behavioral, and leadership question generator and evaluation assistant.
"""

from typing import Dict, Any, List

SAMPLE_QUESTIONS = {
    "software_engineer": [
        {"id": 1, "type": "Technical", "question": "Explain the difference between SQL and NoSQL databases. When would you select each in a distributed system?"},
        {"id": 2, "type": "System Design", "question": "How would you design a rate limiter for an API with millions of concurrent requests?"},
        {"id": 3, "type": "Behavioral", "question": "Describe a scenario where you faced a production outage. How did you diagnose, resolve, and conduct post-mortem?"}
    ],
    "data_scientist": [
        {"id": 1, "type": "Technical", "question": "How do you handle severe class imbalance in a classification dataset?"},
        {"id": 2, "type": "Math/Stats", "question": "Explain the trade-off between Bias and Variance, and techniques used to mitigate overfitting."},
        {"id": 3, "type": "Behavioral", "question": "How do you translate complex model metrics to non-technical executive stakeholders?"}
    ],
    "general": [
        {"id": 1, "type": "Behavioral", "question": "Tell me about a time you had a fundamental disagreement with a colleague on project direction."},
        {"id": 2, "type": "Leadership", "question": "How do you prioritize competing deadlines under tight resource constraints?"}
    ]
}

class InterviewAssistant:
    @staticmethod
    def get_questions_for_role(role_category: str = "software_engineer") -> List[Dict[str, Any]]:
        return SAMPLE_QUESTIONS.get(role_category, SAMPLE_QUESTIONS["general"])

    @staticmethod
    def evaluate_answer(question: str, user_answer: str) -> Dict[str, Any]:
        """Evaluates answer completeness, depth, and communication clarity."""
        words = user_answer.strip().split()
        word_count = len(words)

        if word_count < 25:
            score = 50.0
            feedback = "Answer is quite brief. Use the STAR method (Situation, Task, Action, Result) with concrete examples."
        elif word_count < 75:
            score = 75.0
            feedback = "Good response. Consider including specific metrics, trade-offs, and outcomes to demonstrate business impact."
        else:
            score = 92.0
            feedback = "Excellent response! Well-structured, thorough, and demonstrates deep domain competence."

        return {
            "score": score,
            "word_count": word_count,
            "feedback": feedback
        }
