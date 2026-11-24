"""
Integration tests for Learning Academy, PDF Generation, and CSV Export
"""

import pytest
from services.learning_service import LearningService
from services.report_service import ReportService
from services.employee_service import EmployeeService
from services.student_service import StudentService

def test_learning_course_enrollment_workflow():
    courses = LearningService.get_all_courses()
    assert len(courses) > 0

    test_course_id = courses[0]["id"]
    test_user_id = 1

    # Enroll user
    enrollment = LearningService.enroll_user(test_user_id, test_course_id)
    assert enrollment["id"] is not None

    # Update progress
    updated = LearningService.update_progress(enrollment["id"], 100)
    assert updated is True

    # Verify enrollment list
    user_courses = LearningService.get_user_enrollments(test_user_id)
    assert any(uc["course_id"] == test_course_id and uc["status"] == "COMPLETED" for uc in user_courses)

def test_report_generation_pdf_and_csv():
    employees = EmployeeService.get_all_employees()
    students = StudentService.get_all_students()

    # 1. Talent PDF Report
    pdf_bytes = ReportService.generate_talent_summary_pdf(employees)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF-")

    # 2. Student Placement PDF Report
    placement_pdf = ReportService.generate_students_placement_pdf(students)
    assert isinstance(placement_pdf, bytes)
    assert len(placement_pdf) > 500
    assert placement_pdf.startswith(b"%PDF-")

    # 3. CSV Export
    csv_str = ReportService.export_csv(employees)
    assert isinstance(csv_str, str)
    assert "employee_code" in csv_str
