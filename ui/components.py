"""
TalentSphere Enterprise 2.0 - Reusable UI Components
"""

import streamlit as st
from ui.theme import THEME
from ui.icons import get_icon_svg

def page_header(title: str, subtitle: str = None, badge_text: str = None, badge_type: str = "blue"):
    """Renders a standard enterprise page header with optional subtitle and status badge."""
    badge_html = f'<span class="ts-badge ts-badge-{badge_type}" style="margin-left: 0.75rem; vertical-align: middle;">{badge_text}</span>' if badge_text else ""
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem; border-bottom: 1px solid {THEME['border']}; padding-bottom: 1rem;">
        <h1 style="margin: 0; display: inline-block;">{title}</h1>{badge_html}
        {f'<p style="margin: 0.35rem 0 0 0; color: {THEME["secondary"]}; font-size: 0.95rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def metric_card(title: str, value: str, subtitle: str = None, icon_name: str = None, border_color: str = None):
    """Renders a clean KPI metric card."""
    accent = border_color if border_color else THEME['primary']
    icon_html = f'<div style="float: right; opacity: 0.75;">{get_icon_svg(icon_name, size=24, color=accent)}</div>' if icon_name else ''
    sub_html = f'<div class="ts-metric-sub">{subtitle}</div>' if subtitle else ''
    
    st.markdown(f"""
    <div class="ts-metric-card" style="border-left-color: {accent};">
        {icon_html}
        <div class="ts-metric-title">{title}</div>
        <div class="ts-metric-val">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def stat_row(metrics: list):
    """Renders a row of metric cards.
    metrics: list of dicts with keys: title, value, subtitle (optional), icon (optional), color (optional)
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        with col:
            metric_card(
                title=m.get("title", ""),
                value=str(m.get("value", "")),
                subtitle=m.get("subtitle"),
                icon_name=m.get("icon"),
                border_color=m.get("color")
            )

def profile_card(name: str, role_title: str, email: str, org_name: str = "TalentSphere Global", stats: list = None):
    """Renders an executive or employee summary profile card."""
    initials = "".join([part[0].upper() for part in name.split()[:2]]) if name else "TS"
    stats_html = ""
    if stats:
        stats_items = "".join([f'<div style="text-align: center;"><div style="font-weight: 700; color: {THEME["dark_blue"]}; font-size: 1.1rem;">{s.get("val")}</div><div style="font-size: 0.75rem; color: {THEME["secondary"]};">{s.get("label")}</div></div>' for s in stats])
        stats_html = f'<div style="display: flex; gap: 1.5rem; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed {THEME["border"]};">{stats_items}</div>'

    st.markdown(f"""
    <div class="ts-card">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="width: 56px; height: 56px; border-radius: 50%; background: linear-gradient(135deg, {THEME['primary']} 0%, {THEME['dark_blue']} 100%); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.25rem;">
                {initials}
            </div>
            <div style="flex: 1;">
                <h3 style="margin: 0; color: {THEME['text']}; font-size: 1.2rem;">{name}</h3>
                <div style="font-size: 0.85rem; color: {THEME['secondary']};">{role_title} • {org_name}</div>
                <div style="font-size: 0.8rem; color: {THEME['primary']};">{email}</div>
            </div>
        </div>
        {stats_html}
    </div>
    """, unsafe_allow_html=True)

def empty_state(title: str, message: str, icon_name: str = "search"):
    """Renders a graceful empty state container."""
    icon_svg = get_icon_svg(icon_name, size=40, color=THEME['secondary'])
    st.markdown(f"""
    <div style="text-align: center; padding: 2.5rem 1.5rem; background: #FFFFFF; border: 1px dashed {THEME['border']}; border-radius: 12px; margin: 1rem 0;">
        <div style="margin-bottom: 0.75rem;">{icon_svg}</div>
        <h4 style="margin: 0 0 0.35rem 0; color: {THEME['text']};">{title}</h4>
        <p style="margin: 0; color: {THEME['secondary']}; font-size: 0.9rem;">{message}</p>
    </div>
    """, unsafe_allow_html=True)

def badge(text: str, variant: str = "blue") -> str:
    """Returns HTML for inline status badge."""
    return f'<span class="ts-badge ts-badge-{variant}">{text}</span>'
