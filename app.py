"""
TalentSphere Enterprise 2.0
AI-Powered Talent Management Platform for Employee Performance and Career Growth
Main Application Entry Point & Navigation Router
"""

import streamlit as st
from core.config import settings
from core.permissions import Role
from database.session import init_db
from ui.theme import apply_custom_theme
from ui.sidebar import render_sidebar
from modules.authentication.login_ui import render_login_page

# Import Module Renderers
from modules.admin.dashboard import render_admin_dashboard
from modules.employees.dashboard import render_employee_module
from modules.students.dashboard import render_students_module
from modules.recruitment.dashboard import render_recruitment_module
from modules.resume.dashboard import render_resume_module
from modules.performance.dashboard import render_performance_module
from modules.learning.dashboard import render_learning_module
from modules.career.dashboard import render_career_module
from modules.assessments.dashboard import render_assessments_module
from modules.reports.dashboard import render_reports_module
from modules.notifications.dashboard import render_notifications_module

# Configure Streamlit Page
st.set_page_config(
    page_title=f"{settings.APP_NAME} v{settings.APP_VERSION}",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Enterprise Theme CSS
apply_custom_theme()

# Ensure Database Tables Exist & Auto-Seed on Fresh Cloud Deployment
init_db()
from scripts.seed_database import seed_enterprise_data
seed_enterprise_data()

# Session State Initialization
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = "dashboard"

def get_role_navigation(role: str) -> list:
    """Builds the custom navigation menu based on user role."""
    if role == Role.SUPER_ADMIN.value:
        return [
            {"id": "admin", "label": "Command Center"},
            {"id": "workforce", "label": "Workforce Directory"},
            {"id": "students", "label": "Academic & Students"},
            {"id": "recruitment", "label": "Recruitment & Jobs"},
            {"id": "resume", "label": "Resume & ATS AI"},
            {"id": "performance", "label": "Performance Reviews"},
            {"id": "learning", "label": "Learning Academy"},
            {"id": "career", "label": "Career Pathways"},
            {"id": "assessments", "label": "Skills Assessment"},
            {"id": "reports", "label": "Executive Reports"},
            {"id": "notifications", "label": "Notifications"}
        ]
    elif role == Role.HR_ADMIN.value:
        return [
            {"id": "workforce", "label": "Workforce Directory"},
            {"id": "recruitment", "label": "Recruitment Hub"},
            {"id": "resume", "label": "Resume & ATS AI"},
            {"id": "performance", "label": "Performance Reviews"},
            {"id": "learning", "label": "Learning Academy"},
            {"id": "career", "label": "Career Pathways"},
            {"id": "reports", "label": "HR Reports"},
            {"id": "notifications", "label": "Notifications"}
        ]
    elif role == Role.COLLEGE_ADMIN.value:
        return [
            {"id": "students", "label": "Student Placement"},
            {"id": "assessments", "label": "Campus Assessments"},
            {"id": "resume", "label": "Resume & ATS AI"},
            {"id": "learning", "label": "Learning Academy"},
            {"id": "career", "label": "Career Pathways"},
            {"id": "reports", "label": "Placement Reports"},
            {"id": "notifications", "label": "Notifications"}
        ]
    elif role == Role.EMPLOYEE.value:
        return [
            {"id": "workforce", "label": "My Profile & Goals"},
            {"id": "learning", "label": "Learning Academy"},
            {"id": "career", "label": "Career Growth"},
            {"id": "resume", "label": "Resume Optimizer"},
            {"id": "recruitment", "label": "Internal Opportunities"},
            {"id": "notifications", "label": "Notifications"}
        ]
    elif role == Role.COLLEGE_STUDENT.value:
        return [
            {"id": "students", "label": "Placement Launchpad"},
            {"id": "resume", "label": "Resume & ATS AI"},
            {"id": "assessments", "label": "Practice Tests"},
            {"id": "learning", "label": "Skill Courses"},
            {"id": "career", "label": "Target Career Tracks"},
            {"id": "recruitment", "label": "Campus Placement Jobs"},
            {"id": "notifications", "label": "Notifications"}
        ]
    elif role == Role.HIGH_SCHOOL_STUDENT.value:
        return [
            {"id": "students", "label": "Future Pathways"},
            {"id": "career", "label": "Career Exploration"},
            {"id": "assessments", "label": "Interest Quiz"},
            {"id": "learning", "label": "Foundational Skills"},
            {"id": "notifications", "label": "Notifications"}
        ]
    else:
        return [{"id": "workforce", "label": "Dashboard"}]

def main():
    if not st.session_state["authenticated"] or not st.session_state["user"]:
        render_login_page()
        return

    user = st.session_state["user"]
    nav_items = get_role_navigation(user.get("role", ""))

    # If current nav is invalid for this role, default to first item
    valid_ids = [n["id"] for n in nav_items]
    if st.session_state["nav_selection"] not in valid_ids:
        st.session_state["nav_selection"] = valid_ids[0]

    # Render Sidebar and receive current selection
    active_nav = render_sidebar(user, nav_items, st.session_state["nav_selection"])
    st.session_state["nav_selection"] = active_nav

    # Router logic
    if active_nav == "admin":
        render_admin_dashboard(user)
    elif active_nav == "workforce":
        render_employee_module(user)
    elif active_nav == "students":
        render_students_module(user)
    elif active_nav == "recruitment":
        render_recruitment_module(user)
    elif active_nav == "resume":
        render_resume_module(user)
    elif active_nav == "performance":
        render_performance_module(user)
    elif active_nav == "learning":
        render_learning_module(user)
    elif active_nav == "career":
        render_career_module(user)
    elif active_nav == "assessments":
        render_assessments_module(user)
    elif active_nav == "reports":
        render_reports_module(user)
    elif active_nav == "notifications":
        render_notifications_module(user)
    else:
        st.error(f"Module '{active_nav}' not found.")

if __name__ == "__main__":
    main()
