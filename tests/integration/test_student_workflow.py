"""
Integration tests for Student Service, Academic Departments, and Placement Scoring
"""

import pytest
from services.student_service import StudentService

def test_student_and_placement_workflow():
    students = StudentService.get_all_students()
    assert len(students) > 0

    first_stu = students[0]
    stu_id = first_stu["id"]

    # Update placement score
    updated = StudentService.update_placement_score(stu_id, 92.5)
    assert updated is True

    # Verify score update
    stu_detail = StudentService.get_student_by_user_id(first_stu["user_id"])
    assert stu_detail is not None
    assert stu_detail["placement_readiness_score"] == 92.5

def test_academic_departments_listing():
    depts = StudentService.get_academic_departments()
    assert len(depts) > 0
    dept_names = [d["name"] for d in depts]
    assert "Computer Science & Engineering" in dept_names
