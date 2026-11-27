"""
Authentication UI Module for TalentSphere Enterprise 2.0.
Renders the enterprise login page, registration wizard, and password update dialogs.
"""
import streamlit as st
from services.auth_service import authenticate, register_user, force_password_update
from core.exceptions import AuthenticationError
from core.permissions import Role
from ui.theme import THEME, render_badge
from ui.icons import get_icon_svg

def render_login_sidebar():
    """Keeps sidebar active and populated on the login view to prevent premature collapse."""
    with st.sidebar:
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

        st.markdown(f"""
        <div style="margin: 1.25rem 0; padding: 0.85rem; background: {THEME['light_blue']}; border-radius: 8px; border: 1px solid #BFDBFE;">
            <div style="font-weight: 600; font-size: 0.875rem; color: #1E40AF; margin-bottom: 0.35rem;">🔐 Enterprise Portal</div>
            <div style="font-size: 0.8rem; color: #475569; line-height: 1.4;">
                Sign in with enterprise credentials or use one-click demo logins below.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="font-size: 0.75rem; font-weight: 600; color: {THEME['secondary']}; text-transform: uppercase; margin-bottom: 0.5rem; letter-spacing: 0.05em;">NAVIGATION</div>
        <div style="display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.9rem; color: #64748B;">
            <div style="padding: 0.4rem 0.6rem; border-radius: 6px; background: #EFF6FF; color: #1D4ED8; font-weight: 700;">🔘 Sign In Portal</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Command Center</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Workforce Directory</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Academic & Students</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Recruitment & Jobs</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Resume & ATS AI</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Performance Reviews</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Learning Academy</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Career Pathways</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Skills Assessment</div>
            <div style="padding: 0.4rem 0.6rem; color: #334155;">⚪ Executive Reports</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""<div style="font-size: 0.75rem; font-weight: 600; color: {THEME['secondary']}; text-transform: uppercase; margin-top: 1.25rem; margin-bottom: 0.5rem; letter-spacing: 0.05em;">QUICK 1-CLICK DEMO</div>""", unsafe_allow_html=True)
        if st.button("🛡️ Super Admin (Dr. Vance)", key="sb_quick_superadmin", use_container_width=True):
            user = authenticate("superadmin", "SuperAdmin@2026")
            st.session_state["authenticated"] = True
            st.session_state["user"] = user
            st.session_state["current_role"] = user["role"]
            st.session_state["user_id"] = user["id"]
            st.session_state["nav_selection"] = "admin"
            st.rerun()

        if st.button("👔 Employee (John Doe)", key="sb_quick_employee", use_container_width=True):
            user = authenticate("john_employee", "Employee@2026")
            st.session_state["authenticated"] = True
            st.session_state["user"] = user
            st.session_state["current_role"] = user["role"]
            st.session_state["user_id"] = user["id"]
            st.session_state["nav_selection"] = "workforce"
            st.rerun()

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='border-top: 1px solid {THEME['border']}; padding-top: 1rem;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 8px; height: 8px; border-radius: 50%; background: {THEME['success']};"></div>
            <div style="font-size: 0.75rem; color: {THEME['secondary']};">System: <strong>Operational</strong></div>
        </div>
        """, unsafe_allow_html=True)

def render_login_page():
    """Renders the enterprise SaaS authentication portal."""
    render_login_sidebar()

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

            # 1-Click Demo Login Shortcuts
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            with st.expander("⚡ One-Click Demo Logins & Credentials", expanded=True):
                st.caption("Click any role below to sign in instantly and explore its role-specific dashboard:")
                demo_roles = [
                    ("👔 Corporate Employee", "john_employee", "Employee@2026", "John Doe (Sr. Backend Engineer)"),
                    ("🛡️ Super Admin", "superadmin", "SuperAdmin@2026", "Dr. Robert Vance (Governance)"),
                    ("👥 HR Administrator", "hr_admin", "HRAdmin@2026", "Elena Rostova (Recruitment/ATS)"),
                    ("🎓 College Student", "alex_student", "Student@2026", "Alex Mercer (Placement Portal)"),
                    ("🏛️ College Admin", "college_admin", "CollegeAdmin@2026", "Dean Marcus Sterling (Apex Univ)"),
                    ("🎒 High School Student", "emma_hs", "HighSchool@2026", "Emma Watson (Future Pathways)"),
                ]
                d_c1, d_c2 = st.columns(2)
                for idx, (label, uname, pw, desc) in enumerate(demo_roles):
                    target_col = d_c1 if idx % 2 == 0 else d_c2
                    with target_col:
                        if st.button(label, key=f"quick_login_{uname}", use_container_width=True, help=f"Username: {uname} | Password: {pw}"):
                            try:
                                u = authenticate(uname, pw)
                                st.session_state["authenticated"] = True
                                st.session_state["user"] = u
                                st.session_state["current_role"] = u["role"]
                                st.session_state["user_id"] = u["id"]
                                st.rerun()
                            except Exception as ex:
                                st.error(str(ex))
                        st.markdown(f"<div style='font-size:0.75rem; color:#64748B; margin-top:-4px; margin-bottom:8px;'><code>{uname}</code> / <code>{pw}</code><br/>{desc}</div>", unsafe_allow_html=True)

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
