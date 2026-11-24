"""
TalentSphere Enterprise 2.0 - Employee Service
Handles Employee profiles, department directories, and organizational hierarchy.
"""

from datetime import date
from typing import List, Optional, Dict, Any
from database.session import get_db_session
from database.models.employee import Employee, Department
from database.models.user import User
from core.exceptions import EntityNotFoundError, ValidationError
from core.logging import get_logger

logger = get_logger("employee_service")

class EmployeeService:
    @staticmethod
    def get_all_departments() -> List[Dict[str, Any]]:
        with get_db_session() as db:
            depts = db.query(Department).all()
            return [
                {
                    "id": d.id,
                    "name": d.name,
                    "code": d.code,
                    "employee_count": len(d.employees) if d.employees else 0
                }
                for d in depts
            ]

    @staticmethod
    def create_department(name: str, code: str) -> Dict[str, Any]:
        with get_db_session() as db:
            existing = db.query(Department).filter(Department.code == code).first()
            if existing:
                raise ValidationError("code", f"Department code '{code}' already exists.")
            dept = Department(name=name, code=code)
            db.add(dept)
            db.commit()
            db.refresh(dept)
            return {"id": dept.id, "name": dept.name, "code": dept.code}

    @staticmethod
    def get_all_employees(department_id: Optional[int] = None) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            query = db.query(Employee)
            if department_id:
                query = query.filter(Employee.department_id == department_id)
            employees = query.all()

            results = []
            for emp in employees:
                dept_name = emp.department.name if emp.department else "General"
                results.append({
                    "id": emp.id,
                    "user_id": emp.user_id,
                    "employee_code": emp.employee_code,
                    "first_name": emp.first_name,
                    "last_name": emp.last_name,
                    "full_name": emp.full_name,
                    "email": emp.email,
                    "phone": emp.phone or "",
                    "designation": emp.designation,
                    "department_id": emp.department_id,
                    "department": dept_name,
                    "employment_type": emp.employment_type,
                    "status": emp.status,
                    "work_location": "Remote / HQ",
                    "manager": "Enterprise HR"
                })
            return results

    @staticmethod
    def get_employee_by_id(employee_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            emp = db.query(Employee).filter(Employee.id == employee_id).first()
            if not emp:
                return None
            return {
                "id": emp.id,
                "user_id": emp.user_id,
                "employee_code": emp.employee_code,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "full_name": emp.full_name,
                "email": emp.email,
                "phone": emp.phone,
                "designation": emp.designation,
                "department_id": emp.department_id,
                "department": emp.department.name if emp.department else "General",
                "employment_type": emp.employment_type,
                "status": emp.status,
                "work_location": "Remote / HQ"
            }

    @staticmethod
    def get_employee_by_user_id(user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            emp = db.query(Employee).filter(Employee.user_id == user_id).first()
            if not emp:
                return None
            return EmployeeService.get_employee_by_id(emp.id)

    @staticmethod
    def create_employee(
        user_id: int,
        employee_code: str,
        designation: str,
        department_id: Optional[int] = None,
        work_location: str = "Remote",
        first_name: str = "",
        last_name: str = "",
        email: str = ""
    ) -> Dict[str, Any]:
        with get_db_session() as db:
            existing = db.query(Employee).filter(Employee.employee_code == employee_code).first()
            if existing:
                raise ValidationError("employee_code", f"Employee code '{employee_code}' already exists.")

            user = db.query(User).filter(User.id == user_id).first()
            if user:
                fn = first_name or user.first_name or user.username
                ln = last_name or user.last_name or "Employee"
                em = email or user.email
            else:
                fn = first_name or "New"
                ln = last_name or "Employee"
                em = email or f"{employee_code.lower()}@talentsphere.io"

            emp = Employee(
                user_id=user_id if user else None,
                employee_code=employee_code,
                first_name=fn,
                last_name=ln,
                email=em,
                designation=designation,
                department_id=department_id,
                employment_type="Full-Time",
                status="Active"
            )
            db.add(emp)
            db.commit()
            db.refresh(emp)
            logger.info(f"Created employee record {emp.id} ({emp.employee_code})")
            return {"id": emp.id, "employee_code": emp.employee_code}
