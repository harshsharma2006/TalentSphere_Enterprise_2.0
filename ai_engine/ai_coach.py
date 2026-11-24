"""
TalentSphere Enterprise 2.0 - AI Career Coach
Strategic mentoring and personalized milestone roadmap generator.
"""

from typing import List, Dict, Any

class AICareerCoach:
    @staticmethod
    def generate_growth_plan(target_role: str, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generates a progressive 90-day action plan to bridge skill gaps."""
        plan = []
        if not missing_skills:
            return [
                {"phase": "Month 1", "focus": "Leadership & Domain Mastery", "actions": ["Mentor junior engineers", "Contribute to enterprise architectural RFCs"]},
                {"phase": "Month 2", "focus": "Strategic Impact", "actions": ["Lead cross-functional initiatives", "Optimize system reliability metrics"]},
                {"phase": "Month 3", "focus": "Promotion Readiness", "actions": ["Present quarterly achievements to leadership", "Formalize promotion dossier"]}
            ]

        # Phase 1: Core Fundamentals
        core_targets = missing_skills[:2]
        plan.append({
            "phase": "Month 1 (Days 1 - 30)",
            "focus": f"Foundational Mastery: {', '.join(core_targets)}",
            "actions": [
                f"Complete certified coursework in {core_targets[0]}.",
                f"Build a standalone working POC implementing {core_targets[-1]}.",
                "Dedicate 5 hours weekly to hands-on laboratory exercises."
            ]
        })

        # Phase 2: Integration & Application
        sec_targets = missing_skills[2:4] if len(missing_skills) > 2 else core_targets
        plan.append({
            "phase": "Month 2 (Days 31 - 60)",
            "focus": f"Integration & Tooling: {', '.join(sec_targets)}",
            "actions": [
                "Integrate newly acquired skills into an enterprise-scale capstone project.",
                "Participate in code reviews and architectural discussions.",
                "Conduct mock technical interview sessions."
            ]
        })

        # Phase 3: Certification & Review
        plan.append({
            "phase": "Month 3 (Days 61 - 90)",
            "focus": "Career Readiness & Verification",
            "actions": [
                "Obtain industry certification or complete peer-reviewed project assessment.",
                f"Update ATS resume with concrete achievements matching {target_role}.",
                "Schedule a 1-on-1 career progression review with your manager or placement advisor."
            ]
        })

        return plan
