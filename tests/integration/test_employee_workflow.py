"""
Integration tests for Employee Service, Departments, and Performance Reviews
"""

import pytest
from datetime import date
from services.employee_service import EmployeeService
from services.performance_service import PerformanceService

def test_department_and_employee_workflow():
    departments = EmployeeService.get_all_departments()
    assert len(departments) > 0

    dept_id = departments[0]["id"]
    employees = EmployeeService.get_all_employees()
    assert len(employees) > 0

    first_emp = employees[0]
    emp_detail = EmployeeService.get_employee_by_id(first_emp["id"])
    assert emp_detail is not None
    assert emp_detail["employee_code"] == first_emp["employee_code"]

def test_performance_review_and_goals_workflow():
    employees = EmployeeService.get_all_employees()
    emp_id = employees[0]["id"]

    # Create Goal
    goal = PerformanceService.create_goal(
        employee_id=emp_id,
        title="Automate CI/CD Deployments",
        description="Migrate deployment scripts to GitHub Actions",
        target_date=date(2026, 12, 31),
        weightage=1.5
    )
    assert goal["id"] is not None

    # Update Goal Progress
    updated = PerformanceService.update_goal_progress(goal["id"], 50)
    assert updated is True

    # Create Performance Review
    review = PerformanceService.create_review(
        employee_id=emp_id,
        reviewer_id=None,
        review_cycle="2026 Mid-Year Review",
        overall_score=4.8,
        manager_feedback="Exceptional engineering leadership.",
        strengths="Architecture design, mentorship",
        areas_for_improvement="Delegation"
    )
    assert review["score"] == 4.8

    # Query Reviews
    emp_reviews = PerformanceService.get_all_reviews(emp_id)
    assert len(emp_reviews) > 0
    assert any(r["review_cycle"] == "2026 Mid-Year Review" for r in emp_reviews)
