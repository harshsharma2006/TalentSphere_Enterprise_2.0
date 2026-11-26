"""
Database Seeding Script for TalentSphere Enterprise 2.0.
Provisions initial organizations, roles, verified users for all 6 personas,
departments, skills catalog, courses, and job specifications.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import datetime, date
from database.session import get_db_session, init_db
from database.models import (
    Organization, RoleModel, User, Department, Employee,
    Student, Skill, EmployeeSkill, StudentSkill,
    Course, JobDescription, Assessment, Notification, UserNotification,
    EmployeeGoal, PerformanceReview, CourseEnrollment, Certification,
    CandidateApplication, JobMatch, CareerGoal
)
from core.security import hash_password
from core.permissions import Role
from core.logging import get_logger

logger = get_logger("seeder")

def seed_enterprise_data():
    """Seeds initial demonstration and operational data."""
    init_db()

    with get_db_session() as session:
        # 1. Organizations
        if not session.query(Organization).first():
            org_corp = Organization(name="TalentSphere Global Corp", code="TS-CORP", org_type="Corporate")
            org_univ = Organization(name="Apex Institute of Technology", code="APEX-UNIV", org_type="University")
            org_hs = Organization(name="West Valley High School", code="WV-HS", org_type="High School")
            session.add_all([org_corp, org_univ, org_hs])
            session.flush()
            logger.info("Organizations seeded.")
        else:
            org_corp = session.query(Organization).filter_by(code="TS-CORP").first()
            org_univ = session.query(Organization).filter_by(code="APEX-UNIV").first()
            org_hs = session.query(Organization).filter_by(code="WV-HS").first()

        # 2. Roles
        for role_enum in Role:
            if not session.query(RoleModel).filter_by(name=role_enum.value).first():
                session.add(RoleModel(name=role_enum.value, description=f"{role_enum.value} access privileges"))
        session.flush()

        # 3. Standard Departments
        depts_data = [
            ("Engineering", "ENG"),
            ("Data Science & AI", "DS"),
            ("Human Resources", "HR"),
            ("Finance & Operations", "FIN"),
            ("Product & Design", "PROD")
        ]
        dept_entities = {}
        for d_name, d_code in depts_data:
            existing = session.query(Department).filter_by(code=d_code).first()
            if not existing:
                dept_obj = Department(name=d_name, code=d_code, organization_id=org_corp.id if org_corp else None)
                session.add(dept_obj)
                session.flush()
                dept_entities[d_code] = dept_obj
            else:
                dept_entities[d_code] = existing

        # 4. Standard Skills Taxonomy
        skills_data = [
            ("Python", "Technical"),
            ("SQL & Databases", "Technical"),
            ("Machine Learning", "Technical"),
            ("Docker & Containers", "Technical"),
            ("React & Frontend", "Technical"),
            ("Strategic Leadership", "Leadership"),
            ("Project Management", "Leadership"),
            ("Verbal & Written Communication", "Soft Skills"),
            ("Critical Thinking & Aptitude", "Soft Skills"),
            ("Financial Modeling", "Domain")
        ]
        skill_entities = {}
        for s_name, s_cat in skills_data:
            existing_s = session.query(Skill).filter_by(name=s_name).first()
            if not existing_s:
                s_obj = Skill(name=s_name, category=s_cat)
                session.add(s_obj)
                session.flush()
                skill_entities[s_name] = s_obj
            else:
                skill_entities[s_name] = existing_s

        # 5. Seed Users for All 6 Roles
        demo_users = [
            ("superadmin", "superadmin@talentsphere.local", "SuperAdmin@2026", Role.SUPER_ADMIN.value, "Dr. Robert Vance", org_corp.id if org_corp else None),
            ("hr_admin", "hr@talentsphere.local", "HRAdmin@2026", Role.HR_ADMIN.value, "Elena Rostova", org_corp.id if org_corp else None),
            ("college_admin", "college@apex.edu", "CollegeAdmin@2026", Role.COLLEGE_ADMIN.value, "Dean Marcus Sterling", org_univ.id if org_univ else None),
            ("john_employee", "john.doe@talentsphere.local", "Employee@2026", Role.EMPLOYEE.value, "John Doe", org_corp.id if org_corp else None),
            ("alex_student", "alex@apex.edu", "Student@2026", Role.COLLEGE_STUDENT.value, "Alex Mercer", org_univ.id if org_univ else None),
            ("emma_hs", "emma@westvalley.edu", "HighSchool@2026", Role.HIGH_SCHOOL_STUDENT.value, "Emma Watson", org_hs.id if org_hs else None)
        ]

        user_objects = {}
        for uname, uemail, upwd, urole, ufname, uorg in demo_users:
            u_existing = session.query(User).filter((User.username == uname) | (User.email == uemail)).first()
            if not u_existing:
                user_obj = User(
                    username=uname,
                    email=uemail,
                    password_hash=hash_password(upwd),
                    full_name=ufname,
                    role=urole,
                    organization_id=uorg,
                    is_active=True
                )
                session.add(user_obj)
                session.flush()
                user_objects[uname] = user_obj
            else:
                user_objects[uname] = u_existing

        # 6. Seed Employee Profile for john_employee
        john_user = user_objects.get("john_employee")
        if john_user and not session.query(Employee).filter_by(user_id=john_user.id).first():
            emp_john = Employee(
                user_id=john_user.id,
                employee_code="EMP-1001",
                first_name="John",
                last_name="Doe",
                email=john_user.email,
                phone="+1 (555) 019-4821",
                department_id=dept_entities["ENG"].id if "ENG" in dept_entities else None,
                designation="Senior Backend Engineer",
                employment_type="Full-Time",
                years_experience=4.5,
                current_salary=115000.0,
                status="Active"
            )
            session.add(emp_john)
            session.flush()

            # Attach skills
            if "Python" in skill_entities:
                session.add(EmployeeSkill(employee_id=emp_john.id, skill_id=skill_entities["Python"].id, proficiency_level="Advanced", years_experience=4.0))
            if "SQL & Databases" in skill_entities:
                session.add(EmployeeSkill(employee_id=emp_john.id, skill_id=skill_entities["SQL & Databases"].id, proficiency_level="Advanced", years_experience=3.5))

        # 7. Seed Student Profile for alex_student
        alex_user = user_objects.get("alex_student")
        if alex_user and not session.query(Student).filter_by(user_id=alex_user.id).first():
            std_alex = Student(
                user_id=alex_user.id,
                student_code="STU-COL-2024",
                student_type="College Student",
                first_name="Alex",
                last_name="Mercer",
                email=alex_user.email,
                institution_name="Apex Institute of Technology",
                degree_program="B.Tech Computer Science",
                major="Artificial Intelligence",
                current_year=3,
                graduation_year=2026,
                cgpa_percentage=8.85,
                placement_status="Seeking"
            )
            session.add(std_alex)
            session.flush()
            if "Python" in skill_entities:
                session.add(StudentSkill(student_id=std_alex.id, skill_id=skill_entities["Python"].id, proficiency_level="Intermediate"))

        # 8. Seed High School Student for emma_hs
        emma_user = user_objects.get("emma_hs")
        if emma_user and not session.query(Student).filter_by(user_id=emma_user.id).first():
            std_emma = Student(
                user_id=emma_user.id,
                student_code="STU-HS-902",
                student_type="High School Student",
                first_name="Emma",
                last_name="Watson",
                email=emma_user.email,
                institution_name="West Valley High School",
                degree_program="High School Diploma",
                major="Science & Mathematics Stream",
                current_year=11,
                graduation_year=2027,
                cgpa_percentage=94.0,
                placement_status="Eligible"
            )
            session.add(std_emma)
            session.flush()

        # 9. Seed Courses
        sample_courses = [
            ("Microservices Architecture & Docker", "Technical", "Comprehensive architectural guide to building containerized backend services.", 16, "Advanced", "Docker, Kubernetes, REST APIs"),
            ("Modern Machine Learning & MLOps", "Technical", "Hands-on data pipeline modeling, training, and model serving.", 24, "Advanced", "Python, Scikit-learn, PyTorch"),
            ("Enterprise Leadership & Team Dynamics", "Leadership", "Executive strategies for team delegation, sprint planning, and mentorship.", 12, "Intermediate", "Leadership, People Management"),
            ("Aptitude & Logical Reasoning Mastery", "Soft Skills", "Quantitative tricks, analytical deduction, and problem-solving practice.", 10, "Beginner", "Quantitative Aptitude, Logic")
        ]
        for c_title, c_cat, c_desc, c_dur, c_diff, c_sk in sample_courses:
            if not session.query(Course).filter_by(title=c_title).first():
                session.add(Course(
                    title=c_title,
                    category=c_cat,
                    description=c_desc,
                    duration_hours=c_dur,
                    difficulty_level=c_diff,
                    target_skills=c_sk
                ))

        # 10. Seed Job Descriptions
        sample_jobs = [
            ("Lead Machine Learning Engineer", dept_entities.get("DS"), 4.0, 130000.0, 165000.0, "Python, Machine Learning, PyTorch, SQL, Docker", "Lead development of predictive models and recommendation engines."),
            ("Senior Full-Stack Developer", dept_entities.get("ENG"), 3.0, 110000.0, 140000.0, "Python, React, TypeScript, SQL, Docker", "Build enterprise customer-facing portals and scalable APIs."),
            ("Associate Talent Acquisition Specialist", dept_entities.get("HR"), 1.5, 65000.0, 85000.0, "Recruitment, Sourcing, Communication, Interviewing", "Manage candidate pipeline and talent sourcing workflows.")
        ]
        for j_title, j_dept, j_exp, j_min, j_max, j_sk, j_desc in sample_jobs:
            if not session.query(JobDescription).filter_by(title=j_title).first():
                session.add(JobDescription(
                    organization_id=org_corp.id if org_corp else None,
                    title=j_title,
                    department_id=j_dept.id if j_dept else None,
                    experience_required=j_exp,
                    min_salary=j_min,
                    max_salary=j_max,
                    required_skills=j_sk,
                    description=j_desc,
                    status="Open"
                ))

        # 11. Seed Assessments
        sample_assessments = [
            ("Comprehensive Aptitude & Logic Assessment", "Aptitude", 30, '{"questions": [{"q": "If 5 workers build 5 tables in 5 days, how many days for 100 workers to build 100 tables?", "options": ["5 days", "20 days", "100 days"], "answer": "5 days"}]}'),
            ("Python Engineering Fundamentals", "Coding", 45, '{"questions": [{"q": "What is the time complexity of a dictionary key lookup in average case?", "options": ["O(1)", "O(log n)", "O(n)"], "answer": "O(1)"}]}'),
            ("RIASEC Career Interest Inventory", "Interest", 20, '{"questions": [{"q": "Do you prefer building software or managing finances?", "options": ["Software Engineering", "Financial Analysis"], "answer": "Software Engineering"}]}')
        ]
        for a_title, a_type, a_dur, a_json in sample_assessments:
            if not session.query(Assessment).filter_by(title=a_title).first():
                session.add(Assessment(title=a_title, assessment_type=a_type, duration_minutes=a_dur, questions_json=a_json))

        # 12. Seed Platform Notification
        if not session.query(Notification).first():
            n_obj = Notification(
                title="Welcome to TalentSphere Enterprise 2.0",
                message="Your enterprise talent platform has been successfully initialized with unified multi-role access.",
                target_group="All",
                sender_name="System Administrator"
            )
            session.add(n_obj)

        # 13. Seed Employee Goals (Matching Screenshot 7: Automate CI/CD Deployments)
        emp_john = session.query(Employee).filter_by(employee_code="EMP-1001").first()
        if emp_john and not session.query(EmployeeGoal).filter_by(employee_id=emp_john.id).first():
            goal_1 = EmployeeGoal(
                employee_id=emp_john.id,
                title="Automate CI/CD Deployments",
                description="Migrate deployment scripts to GitHub Actions",
                category="Technical",
                due_date=date(2026, 12, 31),
                status="In Progress",
                progress_pct=50
            )
            session.add(goal_1)
            session.flush()

        # 14. Seed Performance Reviews (Matching Screenshot 10: 6 Completed Reviews for John Doe)
        if emp_john and not session.query(PerformanceReview).filter_by(employee_id=emp_john.id).first():
            for _ in range(6):
                rev = PerformanceReview(
                    employee_id=emp_john.id,
                    reviewer_name="Engineering Manager",
                    review_period="2026 Mid-Year Review",
                    overall_rating=4.8,
                    technical_rating=5.0,
                    leadership_rating=4.5,
                    communication_rating=4.8,
                    achievements="Delivered microservices migration ahead of schedule with 99.9% uptime.",
                    growth_areas="Expand mentoring of junior developers in cloud infrastructure."
                )
                session.add(rev)
            session.flush()

        # 15. Seed Course Enrollment & Certification for John Doe (Matching Screenshot 5)
        course_docker = session.query(Course).filter_by(title="Microservices Architecture & Docker").first()
        john_user = session.query(User).filter_by(username="john_employee").first()
        if john_user and course_docker and not session.query(CourseEnrollment).filter_by(user_id=john_user.id, course_id=course_docker.id).first():
            enr = CourseEnrollment(
                course_id=course_docker.id,
                user_id=john_user.id,
                status="Completed",
                progress_pct=100,
                enrolled_at=datetime(2026, 1, 15, 10, 0),
                completed_at=datetime(2026, 3, 20, 16, 30)
            )
            session.add(enr)
            session.flush()

            cert = Certification(
                enrollment_id=enr.id,
                certificate_code="CERT-DOCKER-2026-001",
                certificate_name="Certified Microservices Architect",
                issued_date=datetime(2026, 3, 20, 16, 30)
            )
            session.add(cert)
            session.flush()

        # 16. Seed Candidate Application & Job Match (Matching Screenshot 4: Candidate Pipeline)
        job_hr = session.query(JobDescription).filter_by(title="Associate Talent Acquisition Specialist").first()
        if job_hr and not session.query(CandidateApplication).filter_by(candidate_email="john.doe@talentsphere.local").first():
            cand_app = CandidateApplication(
                job_id=job_hr.id,
                candidate_name="John Doe",
                candidate_email="john.doe@talentsphere.local",
                candidate_phone="+1 (555) 019-4821",
                current_role="Senior Backend Engineer",
                total_experience_years=4.5,
                skills="Python, Docker, SQL, Kubernetes, CI/CD, Microservices",
                status="Applied",
                notes="Strong engineering background with interest in technical talent acquisition."
            )
            session.add(cand_app)
            session.flush()

            match_record = JobMatch(
                job_id=job_hr.id,
                application_id=cand_app.id,
                match_score=88.0,
                matched_skills="Communication, Sourcing, Interviewing"
            )
            session.add(match_record)
            session.flush()

        # 17. Seed Career Goal for John Doe (Matching Screenshot 6)
        if john_user and not session.query(CareerGoal).filter_by(user_id=john_user.id).first():
            cg = CareerGoal(
                user_id=john_user.id,
                target_role="Senior Cloud DevOps Engineer",
                timeline="12 Months",
                career_statement="Transition into infrastructure leadership and containerization.",
                readiness_score=78.5
            )
            session.add(cg)
            session.flush()

    logger.info("Enterprise database seeding completed successfully.")

if __name__ == "__main__":
    seed_enterprise_data()
    print("✅ Seed script finished successfully.")
