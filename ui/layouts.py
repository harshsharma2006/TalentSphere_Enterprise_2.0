"""
TalentSphere Enterprise 2.0 - Layout Helpers
"""

import streamlit as st

def container_card():
    """Returns a styled HTML wrapper beginning for a card."""
    return st.container()

def split_layout(left_ratio: int = 2, right_ratio: int = 1):
    """Returns two columns with given ratio."""
    return st.columns([left_ratio, right_ratio])

def three_column_layout():
    """Returns three equal columns."""
    return st.columns(3)

def four_column_layout():
    """Returns four equal columns."""
    return st.columns(4)
