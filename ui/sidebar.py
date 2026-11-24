"""
TalentSphere Enterprise 2.0 - Sidebar & Navigation Component
"""

import streamlit as st
from ui.theme import THEME
from ui.icons import get_icon_svg
from core.permissions import Role

ROLE_DISPLAY_LABELS = {
    Role.SUPER_ADMIN.value: "Super Admin",
    Role.HR_ADMIN.value: "HR Administrator",
    Role.COLLEGE_ADMIN.value: "College Administrator",
    Role.EMPLOYEE.value: "Enterprise Employee",
    Role.COLLEGE_STUDENT.value: "College Student",
    Role.HIGH_SCHOOL_STUDENT.value: "High School Student",
}

ROLE_BADGE_CLASS = {
    Role.SUPER_ADMIN.value: "ts-badge-blue",
    Role.HR_ADMIN.value: "ts-badge-blue",
    Role.COLLEGE_ADMIN.value: "ts-badge-yellow",
    Role.EMPLOYEE.value: "ts-badge-green",
    Role.COLLEGE_STUDENT.value: "ts-badge-blue",
    Role.HIGH_SCHOOL_STUDENT.value: "ts-badge-yellow",
}

def render_sidebar(user: dict, nav_items: list, active_nav: str) -> str:
    """
    Renders the modern left sidebar navigation.
    Returns the currently selected navigation key.
    """
    with st.sidebar:
        # App Branding Header
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.75rem; padding-bottom: 1.25rem; border-bottom: 1px solid {THEME['border']};">
            <div style="background: linear-gradient(135deg, {THEME['primary']} 0%, {THEME['dark_blue']} 100%); width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center;">
                {get_icon_svg('shield_check', size=24, color='#FFFFFF')}
            </div>
            <div>
                <div style="font-weight: 700; font-size: 1.05rem; color: {THEME['dark_blue']}; line-height: 1.2;">TalentSphere</div>
                <div style="font-size: 0.725rem; color: {THEME['secondary']}; font-weight: 500; letter-spacing: 0.05em;">ENTERPRISE 2.0</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Authenticated User Badge
        role_label = ROLE_DISPLAY_LABELS.get(user.get("role"), user.get("role", "User"))
        badge_cls = ROLE_BADGE_CLASS.get(user.get("role"), "ts-badge-blue")
        full_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or user.get("username", "User")
        user_initials = "".join([p[0].upper() for p in full_name.split()[:2]]) if full_name else "U"

        st.markdown(f"""
        <div style="margin: 1.25rem 0; padding: 0.85rem; background: {THEME['light_blue']}; border-radius: 8px; border: 1px solid #BFDBFE;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 38px; height: 38px; border-radius: 50%; background: {THEME['primary']}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.95rem;">
                    {user_initials}
                </div>
                <div style="flex: 1; overflow: hidden;">
                    <div style="font-weight: 600; font-size: 0.9rem; color: {THEME['dark_blue']}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{full_name}</div>
                    <div style="font-size: 0.75rem; color: {THEME['secondary']}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{user.get('email', '')}</div>
                </div>
            </div>
            <div style="margin-top: 0.5rem;">
                <span class="ts-badge {badge_cls}">{role_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""<div style="font-size: 0.75rem; font-weight: 600; color: {THEME['secondary']}; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">NAVIGATION</div>""", unsafe_allow_html=True)

        # Navigation Options List
        options = [item["label"] for item in nav_items]
        # Match current active or default to 0
        current_index = 0
        for i, item in enumerate(nav_items):
            if item.get("id") == active_nav:
                current_index = i
                break

        selected_label = st.radio(
            label="Menu",
            options=options,
            index=current_index,
            label_visibility="collapsed",
            key="ts_nav_radio"
        )

        selected_id = nav_items[options.index(selected_label)]["id"]

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-top: 1px solid {THEME['border']}; padding-top: 1rem;'></div>", unsafe_allow_html=True)

        # System Health / Status indicator
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: {THEME['success']};"></div>
            <div style="font-size: 0.75rem; color: {THEME['secondary']};">System: <strong>Operational</strong></div>
        </div>
        """, unsafe_allow_html=True)

        # Logout button
        if st.button("Sign Out", key="sidebar_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.session_state["nav_selection"] = None
            st.rerun()

        return selected_id
