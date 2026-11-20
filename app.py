"""
AI Student Performance Analytics & Prediction System
Main Application Entry Point
"""

import streamlit as st
import os

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="AI Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Modern SaaS Dark Theme
from src.ui_components import apply_custom_css
apply_custom_css()

# Import Data & Views
from src.data_loader import load_default_data
from src.views import (
    page_executive_dashboard,
    page_prediction,
    page_student_explorer,
    page_at_risk,
    page_academic_insights,
    page_recommendations,
    page_model_lab,
    page_dataset_mgmt,
    page_responsible_ai
)

# Initialize Session State
if "active_df" not in st.session_state:
    st.session_state["active_df"] = load_default_data()

df = st.session_state["active_df"]

# Sidebar Navigation & Branding
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #1E293B; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: linear-gradient(135deg, #2563EB, #1D4ED8); width: 38px; height: 38px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                🎓
            </div>
            <div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.01em;">
                    EduAnalytics AI
                </div>
                <div style="font-size: 0.72rem; color: #38BDF8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">
                    Enterprise Student Intelligence
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 0.72rem; color: #64748B; text-transform: uppercase; font-weight: 700; letter-spacing: 0.08em; margin-bottom: 8px;'>NAVIGATION MENU</p>", unsafe_allow_html=True)
    
    pages = {
        "📊 Executive Dashboard": page_executive_dashboard,
        "🔮 AI Student Prediction": page_prediction,
        "🔍 Student Explorer": page_student_explorer,
        "🚨 At-Risk Student Intelligence": page_at_risk,
        "📈 Academic Insights": page_academic_insights,
        "💡 AI Recommendation Engine": page_recommendations,
        "🧠 Model Insights & AI Lab": page_model_lab,
        "🗄️ Dataset Management": page_dataset_mgmt,
        "⚖️ Responsible AI": page_responsible_ai
    }

    selected_page_name = st.radio(
        label="Select Navigation Page",
        options=list(pages.keys()),
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Sidebar Status Panel
    total_recs = len(df)
    st.markdown(f"""
    <div style="background: rgba(17, 24, 39, 0.85); border: 1px solid #1E293B; border-radius: 10px; padding: 14px; margin-top: auto;">
        <div style="font-size: 0.75rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; margin-bottom: 8px;">
            SYSTEM STATUS
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
            <span style="color: #94A3B8;">Cohort Size:</span>
            <span style="color: #F8FAFC; font-weight: 600;">{total_recs:,} Students</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
            <span style="color: #94A3B8;">ML Pipeline:</span>
            <span style="color: #10B981; font-weight: 600;">Active (Serving)</span>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
            <span style="color: #94A3B8;">Certification:</span>
            <span style="color: #38BDF8; font-weight: 600;">Microsoft AI-901</span>
        </div>
        <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #1E293B; font-size: 0.76rem; color: #64748B;">
            Developer: <strong>Harsh Chandel</strong><br>
            GitHub: <a href="https://github.com/hrshcodes29/AI-Student-Performance-Analytics" target="_blank" style="color: #38BDF8; text-decoration: none;">@hrshcodes29</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render Selected View
selected_page_module = pages[selected_page_name]
selected_page_module.render(df)

