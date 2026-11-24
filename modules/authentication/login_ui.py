"""
Authentication UI Module for TalentSphere Enterprise 2.0.
Renders the enterprise login page, registration wizard, and password update dialogs.
"""
import streamlit as st
from services.auth_service import authenticate, register_user, force_password_update
from core.exceptions import AuthenticationError
from core.permissions import Role
from ui.theme import render_badge

def render_login_page():
    """Renders the enterprise SaaS authentication portal."""
    col_l, col_center, col_r = st.columns([1, 2.2, 1])

    with col_center:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Brand Heading
        st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 56px; height: 56px; border-radius: 14px; background: linear-gradient(135deg, #1E40AF, #2563EB); color: white; font-size: 26px; font-weight: 800; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25); margin-bottom: 12px;">
                TS
            </div>
            <div style="font-size: 2rem; font-weight: 800; color: #0F172A; letter-spacing: -0.5px;">TalentSphere Enterprise 2.0</div>
            <div style="font-size: 0.95rem; color: #64748B; font-weight: 500; margin-top: 4px;">AI-Powered Talent Management & Career Acceleration Platform</div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_register = st.tabs(["Sign In to Platform", "Create New Account"])

        with tab_login:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:24px 28px; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);">
                <div style="font-size:1.15rem; font-weight:700; color:#0F172A; margin-bottom:4px;">Sign In</div>
                <div style="font-size:0.85rem; color:#64748B; margin-bottom:16px;">Enter your enterprise credentials to access your workspace.</div>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                ident = st.text_input("Username or Work Email", placeholder="e.g. superadmin or email@domain.com")
                pwd = st.text_input("Password", type="password", placeholder="Enter your password")

                submitted = st.form_submit_button("Sign In to Workspace", use_container_width=True)

                if submitted:
                    try:
                        user = authenticate(ident, pwd)
                        st.session_state["authenticated"] = True
                        st.session_state["user"] = user
                        st.session_state["current_role"] = user["role"]
                        st.session_state["user_id"] = user["id"]
                        st.success(f"Welcome back, {user['full_name']}!")
                        st.rerun()
                    except AuthenticationError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Sign-in error: {e}")

            st.markdown("</div>", unsafe_allow_html=True)

        with tab_register:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:24px 28px; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);">
                <div style="font-size:1.15rem; font-weight:700; color:#0F172A; margin-bottom:4px;">Registration Portal</div>
                <div style="font-size:0.85rem; color:#64748B; margin-bottom:16px;">Enroll as a new Employee, College Student, or High School Student.</div>
            """, unsafe_allow_html=True)

            with st.form("register_form"):
                reg_name = st.text_input("Full Name *", placeholder="e.g. Maya Lin")
                reg_uname = st.text_input("Username *", placeholder="e.g. mayalin")
                reg_email = st.text_input("Email Address *", placeholder="e.g. maya@example.com")
                reg_role = st.selectbox(
                    "Profile Type *",
                    [Role.EMPLOYEE.value, Role.COLLEGE_STUDENT.value, Role.HIGH_SCHOOL_STUDENT.value, Role.HR_ADMIN.value, Role.COLLEGE_ADMIN.value]
                )
                reg_pwd = st.text_input("Password *", type="password", placeholder="Min 8 chars, 1 uppercase, 1 digit, 1 symbol")
                reg_pwd_confirm = st.text_input("Confirm Password *", type="password")

                st.caption("Password must be 8+ characters, including uppercase, lowercase, numbers, and special characters.")

                if st.form_submit_button("Register Account", use_container_width=True):
                    if reg_pwd != reg_pwd_confirm:
                        st.error("Passwords do not match.")
                    else:
                        try:
                            res = register_user(
                                username=reg_uname,
                                email=reg_email,
                                password=reg_pwd,
                                full_name=reg_name,
                                role=reg_role
                            )
                            st.success(f"Account '{reg_uname}' created successfully! You may now sign in.")
                        except Exception as e:
                            st.error(str(e))

            st.markdown("</div>", unsafe_allow_html=True)

def render_force_password_change_modal(user: dict):
    """Renders mandatory password update screen when default credentials are in use."""
    st.markdown("""
    <div style="max-width: 500px; margin: 40px auto; background: #FFFFFF; border: 2px solid #2563EB; border-radius: 14px; padding: 28px; box-shadow: 0 8px 24px rgba(37,99,235,0.1);">
        <div style="font-size: 1.3rem; font-weight: 800; color: #0F172A; margin-bottom: 6px;">Security Notice: Default Password In Use</div>
        <div style="font-size: 0.875rem; color: #475569; margin-bottom: 18px;">For platform security, you must replace the default initial password before proceeding.</div>
    """, unsafe_allow_html=True)

    with st.form("force_password_change_form"):
        new_pwd = st.text_input("New Strong Password *", type="password")
        confirm_pwd = st.text_input("Confirm New Password *", type="password")

        if st.form_submit_button("Update Password and Continue", use_container_width=True):
            if new_pwd != confirm_pwd:
                st.error("Passwords do not match.")
            else:
                ok, msg = force_password_update(user["id"], new_pwd)
                if ok:
                    st.success("Password updated successfully!")
                    st.session_state["user"]["must_change_password"] = False
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)
