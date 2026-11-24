"""
TalentSphere Enterprise 2.0 - Notifications Module
"""

import streamlit as st
from ui.theme import THEME
from ui.components import page_header, stat_row, metric_card, empty_state
from database.session import get_db_session
from database.models.notification import Notification

def render_notifications_module(current_user: dict):
    page_header("Notification Center", "System broadcasts, review invitations, and status alerts.", "Alerts", "blue")

    with get_db_session() as db:
        notes = db.query(Notification).order_by(Notification.created_at.desc()).limit(20).all()
        if notes:
            for n in notes:
                st.markdown(f"""
                <div class="ts-card" style="border-left: 4px solid {THEME['primary']};">
                    <div style="display: flex; justify-content: space-between;">
                        <h4 style="margin: 0;">{n.title}</h4>
                        <span class="ts-badge ts-badge-blue">System Notice</span>
                    </div>
                    <p style="margin: 0.4rem 0; font-size: 0.9rem; color: {THEME['secondary']};">{n.message}</p>
                    <div style="font-size: 0.75rem; color: {THEME['secondary']};">{str(n.created_at.date()) if n.created_at else ''}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            empty_state("No Notifications", "You're all caught up! New alerts will appear here.", "bell")
