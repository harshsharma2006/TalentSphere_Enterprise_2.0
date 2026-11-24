"""
TalentSphere Enterprise 2.0 - Employees Module
Handles HR Admin Employee Directory and Employee Self-Service Dashboard.
"""

import streamlit as st
import pandas as pd
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, profile_card, empty_state
from services.employee_service import EmployeeService
from services.performance_service import PerformanceService
from services.career_service import CareerService
from services.report_service import ReportService
from core.permissions import Role

def render_employee_module(current_user: dict):
    is_hr = current_user.get("role") in [Role.SUPER_ADMIN.value, Role.HR_ADMIN.value]

    if is_hr:
        render_hr_employee_management(current_user)
    else:
        render_employee_self_service(current_user)

def render_hr_employee_management(current_user: dict):
    page_header("Enterprise Workforce Directory", "Manage employee profiles, departments, designations, and talent records.", "HR Admin", "blue")

    employees = EmployeeService.get_all_employees()
    departments = EmployeeService.get_all_departments()

    stat_row([
        {"title": "Total Employees", "value": len(employees), "subtitle": "Full workforce count", "icon": "users", "color": THEME["primary"]},
        {"title": "Departments", "value": len(departments), "subtitle": "Operational units", "icon": "briefcase", "color": THEME["dark_blue"]},
        {"title": "Remote / Hybrid", "value": len([e for e in employees if e.get("work_location") in ["Remote", "Hybrid"]]), "subtitle": "Flexible workforce", "icon": "compass", "color": THEME["success"]},
        {"title": "Active Reviews", "value": len(PerformanceService.get_all_reviews()), "subtitle": "Cycles in progress", "icon": "award", "color": THEME["warning"]},
    ])

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Employee Directory", "Add New Employee", "Export Talent Reports"])

    with tab1:
        st.subheader("Workforce Records")
        if employees:
            df = pd.DataFrame(employees)
            cols = ["employee_code", "full_name", "designation", "department", "email", "work_location", "manager"]
            avail = [c for c in cols if c in df.columns]

            # Search bar
            search = st.text_input("Filter by Name, Designation, or Department", placeholder="Search...", key="emp_search")
            if search:
                term = search.lower()
                df = df[df["full_name"].str.lower().str.contains(term) | df["designation"].str.lower().str.contains(term) | df["department"].str.lower().str.contains(term)]

            st.dataframe(df[avail], use_container_width=True, hide_index=True)
        else:
            empty_state("No Employees Found", "Add employee records or seed demo data.")

    with tab2:
        st.subheader("Add Employee Record")
        from services.auth_service import AuthService
        users = [u for u in AuthService.list_users() if u.get("role") == Role.EMPLOYEE.value]

        with st.form("create_emp_form"):
            col1, col2 = st.columns(2)
            with col1:
                assigned_user_id = st.selectbox(
                    "Select Associated User Account*",
                    options=[u["id"] for u in users] if users else [0],
                    format_func=lambda uid: f"{[u['full_name'] for u in users if u['id'] == uid][0]} ({[u['email'] for u in users if u['id'] == uid][0]})" if users else "No unassigned employee users"
                )
                emp_code = st.text_input("Employee Code*", placeholder="e.g. EMP-1002")
                designation = st.text_input("Designation / Title*", placeholder="e.g. Senior Software Engineer")
            with col2:
                dept_id = st.selectbox(
                    "Department",
                    options=[d["id"] for d in departments],
                    format_func=lambda did: [d["name"] for d in departments if d["id"] == did][0]
                )
                location = st.selectbox("Work Location", ["Remote", "Hybrid", "New York HQ", "San Francisco Office", "London Hub"])

            submitted = st.form_submit_button("Register Employee", use_container_width=True)
            if submitted:
                if not emp_code or not designation or not users:
                    st.error("Please fill in all required fields.")
                else:
                    try:
                        res = EmployeeService.create_employee(
                            user_id=assigned_user_id,
                            employee_code=emp_code,
                            designation=designation,
                            department_id=dept_id,
                            work_location=location
                        )
                        st.success(f"Employee {emp_code} registered successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with tab3:
        st.subheader("Executive Talent Reports")
        st.write("Generate and download confidential PDF talent records or export CSV files for enterprise HRIS systems.")

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            if st.button("Generate Talent Summary PDF", use_container_width=True):
                pdf_bytes = ReportService.generate_talent_summary_pdf(employees)
                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=pdf_bytes,
                    file_name="TalentSphere_Workforce_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with col_p2:
            csv_str = ReportService.export_csv(employees)
            st.download_button(
                label="⬇️ Export Directory to CSV",
                data=csv_str,
                file_name="TalentSphere_Employees.csv",
                mime="text/csv",
                use_container_width=True
            )

def render_employee_self_service(current_user: dict):
    page_header("Employee Self-Service Portal", "Personal performance, assigned KPI goals, and professional development.", "Employee", "green")

    emp = EmployeeService.get_employee_by_user_id(current_user["id"])
    emp_id = emp["id"] if emp else 1

    profile_card(
        name=f"{current_user.get('first_name', '')} {current_user.get('last_name', '')}".strip() or current_user.get("username"),
        role_title=emp.get("designation", "Software Engineer") if emp else "Enterprise Employee",
        email=current_user.get("email"),
        org_name=emp.get("department", "Engineering") if emp else "TalentSphere Global",
        stats=[
            {"label": "Code", "val": emp.get("employee_code", "EMP-001") if emp else "EMP-001"},
            {"label": "Location", "val": emp.get("work_location", "Remote") if emp else "Remote"},
            {"label": "Status", "val": "Active"}
        ]
    )

    tab1, tab2, tab3 = st.tabs(["Active Goals", "Performance Reviews", "Career Pathways"])

    with tab1:
        st.subheader("My Assigned KPI Goals")
        goals = PerformanceService.get_employee_goals(emp_id)
        if goals:
            for g in goals:
                st.markdown(f"""
                <div class="ts-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="margin: 0;">{g['title']}</h4>
                        <span class="ts-badge ts-badge-blue">{g['status']}</span>
                    </div>
                    <p style="color: {THEME['secondary']}; margin: 0.5rem 0; font-size: 0.9rem;">{g['description']}</p>
                    <div style="font-size: 0.8rem; color: {THEME['secondary']}; margin-bottom: 0.25rem;">Target Date: {g['target_date']} • Weight: {g['weightage']}</div>
                </div>
                """, unsafe_allow_html=True)
                new_prog = st.slider(f"Update Progress for '{g['title']}'", 0, 100, g["progress_percentage"], key=f"goal_prog_{g['id']}")
                if new_prog != g["progress_percentage"]:
                    PerformanceService.update_goal_progress(g["id"], new_prog)
                    st.success("Progress saved!")
                    st.rerun()
        else:
            empty_state("No Active Goals", "Work with your manager to establish quarterly goals.")

    with tab2:
        st.subheader("Performance Review History")
        reviews = PerformanceService.get_all_reviews(emp_id)
        if reviews:
            for r in reviews:
                st.markdown(f"""
                <div class="ts-card" style="border-left: 4px solid {THEME['primary']};">
                    <div style="display: flex; justify-content: space-between;">
                        <h4 style="margin: 0;">Cycle: {r['review_cycle']}</h4>
                        <div style="font-weight: 700; font-size: 1.15rem; color: {THEME['primary']};">Score: {r['overall_score']} / 5.0</div>
                    </div>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem;"><strong>Manager Feedback:</strong> {r['manager_feedback']}</p>
                    <p style="margin: 0; font-size: 0.85rem; color: {THEME['secondary']};">Strengths: {r['strengths']} • Areas for Improvement: {r['areas_for_improvement']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("No Reviews on File", "Annual performance cycle evaluations will appear here.")

    with tab3:
        st.subheader("Career Progression Plan")
        c_goals = CareerService.get_career_goals(current_user["id"])
        if c_goals:
            for cg in c_goals:
                st.markdown(f"""
                <div class="ts-card">
                    <h4>Target: {cg['target_role']}</h4>
                    <p>Timeline: {cg['target_timeline_months']} months • Progress: {cg['progress_percentage']}%</p>
                    <ul>
                        {''.join([f'<li>{a}</li>' for a in cg.get('action_items', [])])}
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active career goals saved yet. Navigate to Career Planning to set a roadmap.")
