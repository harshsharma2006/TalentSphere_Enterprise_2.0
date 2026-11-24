"""
TalentSphere Enterprise 2.0 - Skill Analyzer
Performs competency benchmarking and skill gap diagnostics.
"""

from typing import List, Dict, Any

class SkillAnalyzer:
    @staticmethod
    def analyze_skill_gap(current_skills: List[str], target_role_skills: List[str]) -> Dict[str, Any]:
        """
        Calculates skill match percentage, identifying matched and missing competencies.
        """
        curr_set = set(s.lower().strip() for s in current_skills)
        target_set = set(s.lower().strip() for s in target_role_skills)

        if not target_set:
            return {
                "readiness_percentage": 100.0,
                "matched_skills": list(curr_set),
                "missing_skills": [],
                "gap_count": 0
            }

        matched = curr_set.intersection(target_set)
        missing = target_set.difference(curr_set)

        readiness = round((len(matched) / len(target_set)) * 100, 1)

        return {
            "readiness_percentage": readiness,
            "matched_skills": [s.title() for s in matched],
            "missing_skills": [s.title() for s in missing],
            "gap_count": len(missing)
        }
