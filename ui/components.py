"""
TalentSphere Enterprise 2.0 - Reusable UI Components
Calibrated to match exact Enterprise Design System specifications.
"""

import streamlit as st
from ui.theme import THEME
from ui.icons import get_icon_svg

def page_header(title: str, subtitle: str = None, badge_text: str = None, badge_type: str = "blue"):
    """
    Renders an enterprise page header matching exact screenshot specifications:
    - Large Title (h1)
    - Distinct status badge directly below title
    - Explanatory subtitle below badge
    - Clean whitespace without distracting horizontal borders
    """
    badge_html = f'<div style="margin: 0.5rem 0 0.6rem 0;"><span class="ts-badge ts-badge-{badge_type}">{badge_text}</span></div>' if badge_text else ""
    sub_html = f'<p style="margin: 0; color: #64748B; font-size: 0.95rem; line-height: 1.5;">{subtitle}</p>' if subtitle else ""
    
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin: 0; font-size: 1.95rem; font-weight: 700; color: #1E293B; letter-spacing: -0.02em;">{title}</h1>
        {badge_html}
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def metric_card(title: str, value: str, subtitle: str = None, icon_name: str = None, border_color: str = None):
    """
    Renders an enterprise KPI stat card matching exact screenshot specifications:
    - Vertical colored left-accent bar (3px)
    - Top-left aligned icon colored to match the accent
    - Small bold uppercase metric title
    - High-contrast prominent metric value
    - Descriptive muted subtitle
    """
    accent = border_color if border_color else THEME['primary']
    icon_html = f'<div style="color: {accent}; margin-bottom: 0.65rem; display: flex; align-items: center;">{get_icon_svg(icon_name, size=22, color=accent)}</div>' if icon_name else ''
    sub_html = f'<div class="ts-metric-sub">{subtitle}</div>' if subtitle else ''
    
    st.markdown(f"""
    <div class="ts-metric-card" style="border-left: 3px solid {accent} !important;">
        {icon_html}
        <div class="ts-metric-title">{title}</div>
        <div class="ts-metric-val">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def stat_row(metrics: list):
    """
    Renders a responsive horizontal row of metric cards.
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
    """
    Renders an executive/employee summary profile card matching screenshot specifications:
    - Circular deep-navy avatar with white capitalized initials
    - Prominent bold employee name, role title & department, and email
    - Dotted horizontal rule separator
    - Multi-column horizontal stats with large bold values and small labels
    """
    initials = "".join([part[0].upper() for part in name.split()[:2]]) if name else "TS"
    stats_html = ""
    if stats:
        stats_items = "".join([
            f'<div style="text-align: left;">'
            f'<div style="font-weight: 800; color: #0F172A; font-size: 1.15rem; line-height: 1.2;">{s.get("val")}</div>'
            f'<div style="font-size: 0.775rem; color: #64748B; margin-top: 0.25rem; font-weight: 500;">{s.get("label")}</div>'
            f'</div>'
            for s in stats
        ])
        stats_html = f'<div style="display: flex; gap: 3.5rem; margin-top: 1.25rem; padding-top: 1rem; border-top: 1px dotted #E2E8F0;">{stats_items}</div>'

    subtitle_line = f"{role_title} • {org_name}" if org_name else role_title

    st.markdown(f"""
    <div class="ts-card" style="padding: 1.75rem 2rem;">
        <div style="display: flex; align-items: center; gap: 1.25rem;">
            <div style="width: 54px; height: 54px; border-radius: 50%; background: #174A82; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.25rem;">
                {initials}
            </div>
            <div style="flex: 1;">
                <h3 style="margin: 0 0 0.25rem 0; color: #0F172A; font-size: 1.35rem; font-weight: 700;">{name}</h3>
                <div style="font-size: 0.85rem; color: #475569; margin-bottom: 0.2rem;">{subtitle_line}</div>
                <div style="font-size: 0.825rem; color: #2563EB;">{email}</div>
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
