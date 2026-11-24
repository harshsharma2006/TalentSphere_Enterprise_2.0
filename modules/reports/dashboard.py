"""
TalentSphere Enterprise 2.0 - Notifications & Reports Module
"""

import streamlit as st
import pandas as pd
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from database.session import get_db_session
from database.models.notification import Notification
from services.employee_service import EmployeeService
from services.student_service import StudentService
from services.report_service import ReportService

def render_notifications_module(current_user: dict):
    page_header("Notification Center", "System broadcasts, review invitations, and status alerts.", "Alerts", "blue")

    with get_db_session() as db:
        notes = db.query(Notification).filter(Notification.user_id == current_user["id"]).order_by(Notification.created_at.desc()).all()
        if notes:
            for n in notes:
                st.markdown(f"""
                <div class="ts-card" style="border-left: 4px solid {THEME['primary']};">
                    <div style="display: flex; justify-content: space-between;">
                        <h4 style="margin: 0;">{n.title}</h4>
                        <span class="ts-badge ts-badge-{'blue' if not n.is_read else 'gray'}">{'Unread' if not n.is_read else 'Read'}</span>
                    </div>
                    <p style="margin: 0.4rem 0; font-size: 0.9rem; color: {THEME['secondary']};">{n.message}</p>
                    <div style="font-size: 0.75rem; color: {THEME['secondary']};">{str(n.created_at.date()) if n.created_at else ''}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("No Notifications", "You're all caught up! New alerts will appear here.", "bell")

def render_reports_module(current_user: dict):
    page_header("Enterprise Reports & Intelligence", "Generate executive talent PDFs and export datasets.", "Reporting", "blue")

    employees = EmployeeService.get_all_employees()
    students = StudentService.get_all_students()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="ts-card">
            <h4>Workforce Talent Review PDF</h4>
            <p style="color: {THEME['secondary']}; font-size: 0.9rem;">Complete directory with designations, departments, and headcount analytics.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Workforce PDF", key="btn_rep_wf", use_container_width=True):
            pdf_bytes = ReportService.generate_talent_summary_pdf(employees)
            st.download_button("⬇️ Download Workforce PDF", pdf_bytes, "TalentSphere_Workforce.pdf", "application/pdf", use_container_width=True)

    with col2:
        st.markdown(f"""
        <div class="ts-card">
            <h4>Student Placement Readiness PDF</h4>
            <p style="color: {THEME['secondary']}; font-size: 0.9rem;">Campus placement percentages, GPA distribution, and career readiness scores.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Placement PDF", key="btn_rep_pl", use_container_width=True):
            pdf_bytes = ReportService.generate_students_placement_pdf(students)
            st.download_button("⬇️ Download Placement PDF", pdf_bytes, "TalentSphere_Placement.pdf", "application/pdf", use_container_width=True)
