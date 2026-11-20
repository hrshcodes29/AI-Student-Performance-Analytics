"""
UI Components & Chart Generators for AI Student Performance Analytics
High-end modern SaaS styling with dark glassmorphism, responsive Plotly charts, and KPI cards.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Core Color Palette
THEME = {
    "bg_dark": "#0B0F19",
    "card_bg": "#111827",
    "card_border": "#1E293B",
    "primary": "#3B82F6",
    "cyan": "#06B6D4",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "purple": "#8B5CF6",
    "text_main": "#F9FAFB",
    "text_muted": "#9CA3AF"
}

def apply_custom_css():
    """Injects high-end modern dark styling into the Streamlit app."""
    custom_css = """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }

    /* Headers styling */
    h1, h2, h3, h4 {
        color: #F9FAFB !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    /* Modern Card Container */
    .modern-card {
        background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(59, 130, 246, 0.18);
        border-radius: 14px;
        padding: 22px 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .modern-card:hover {
        border-color: rgba(59, 130, 246, 0.35);
    }

    /* KPI Metric Card */
    .kpi-card {
        background: linear-gradient(145deg, #111827 0%, #0F172A 100%);
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 18px 20px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .kpi-card:hover {
        border-color: #3B82F6;
        transform: translateY(-2px);
    }
    .kpi-title {
        color: #9CA3AF;
        font-size: 0.82rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .kpi-value {
        color: #FFFFFF;
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .kpi-subtitle {
        color: #6B7280;
        font-size: 0.78rem;
        margin-top: 6px;
    }

    /* Risk Badges */
    .badge-low {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-mod {
        background: rgba(245, 158, 11, 0.15);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-high {
        background: rgba(239, 68, 68, 0.15);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Section Header Banner */
    .header-banner {
        background: linear-gradient(90deg, rgba(30, 58, 138, 0.35) 0%, rgba(15, 23, 42, 0.1) 100%);
        border-left: 4px solid #3B82F6;
        padding: 16px 20px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 24px;
    }

    /* Custom Streamlit Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8, #1E40AF) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6) !important;
        transform: translateY(-1px) !important;
    }

    /* Sidebar Clean Styling */
    [data-testid="stSidebar"] {
        background-color: #0D1117 !important;
        border-right: 1px solid #1E293B !important;
    }
    
    /* Code and Pre blocks */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: #1E293B !important;
        color: #38BDF8 !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_kpi(col, title: str, value: str, subtitle: str = "", border_color: str = "#3B82F6"):
    """Renders a styled KPI card in a Streamlit column."""
    with col:
        html = f"""
        <div class="kpi-card" style="border-left: 3px solid {border_color};">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

def render_banner(title: str, subtitle: str, tag: str = "SYSTEM"):
    """Renders a sleek top banner for pages."""
    html = f"""
    <div class="header-banner">
        <div style="font-size: 0.72rem; color: #38BDF8; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">
            {tag}
        </div>
        <div style="font-size: 1.55rem; color: #FFFFFF; font-weight: 800; line-height: 1.2;">
            {title}
        </div>
        <div style="font-size: 0.88rem; color: #94A3B8; margin-top: 4px;">
            {subtitle}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def get_plotly_layout_defaults():
    """Returns dark cohesive theme layout dictionary for Plotly charts."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#E2E8F0", size=12),
        margin=dict(l=40, r=30, t=50, b=40),
        xaxis=dict(
            gridcolor="#1E293B",
            zerolinecolor="#334155",
            showline=True,
            linecolor="#334155"
        ),
        yaxis=dict(
            gridcolor="#1E293B",
            zerolinecolor="#334155",
            showline=True,
            linecolor="#334155"
        ),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.8)",
            bordercolor="#1E293B",
            borderwidth=1,
            font=dict(color="#CBD5E1")
        )
    )

def plot_performance_distribution(df: pd.DataFrame):
    """Histogram + Box Plot of Final Scores."""
    fig = px.histogram(
        df,
        x="final_score",
        color="risk_level",
        nbins=28,
        marginal="box",
        title="Student Performance Distribution by Risk Tier",
        labels={"final_score": "Composite Academic Score (0-100)", "risk_level": "Risk Tier"},
        color_discrete_map={
            "Low Risk": "#10B981",
            "Moderate Risk": "#F59E0B",
            "High Risk": "#EF4444"
        },
        opacity=0.85
    )
    fig.update_layout(get_plotly_layout_defaults())
    fig.update_layout(height=400)
    return fig

def plot_attendance_vs_score(df: pd.DataFrame):
    """Scatter plot: Attendance vs Final Score with trendline."""
    fig = px.scatter(
        df,
        x="attendance_rate",
        y="final_score",
        color="risk_level",
        size="study_hours_per_day",
        hover_data=["student_id", "name", "grade_level"],
        title="Attendance Rate vs Final Academic Score",
        labels={
            "attendance_rate": "Attendance Rate (%)",
            "final_score": "Final Score (0-100)",
            "study_hours_per_day": "Daily Study Hours"
        },
        color_discrete_map={
            "Low Risk": "#10B981",
            "Moderate Risk": "#F59E0B",
            "High Risk": "#EF4444"
        },
        opacity=0.85
    )
    fig.update_layout(get_plotly_layout_defaults())
    fig.update_layout(height=420)
    return fig

def plot_subject_comparison(df: pd.DataFrame):
    """Subject-wise average marks across grade levels."""
    subjects = ["math_score", "science_score", "english_score", "computer_science_score"]
    clean_labels = ["Mathematics", "Science", "English", "Computer Science"]
    
    avg_scores = [df[col].mean() for col in subjects]
    
    fig = go.Figure(data=[
        go.Bar(
            x=clean_labels,
            y=avg_scores,
            marker=dict(
                color=["#3B82F6", "#06B6D4", "#8B5CF6", "#10B981"],
                line=dict(color="#1E293B", width=1)
            ),
            text=[f"{v:.1f}%" for v in avg_scores],
            textposition="outside"
        )
    ])
    fig.update_layout(get_plotly_layout_defaults())
    fig.update_layout(
        title="Subject-Wise Class Performance Average",
        yaxis=dict(range=[0, 105]),
        height=380
    )
    return fig

def plot_risk_distribution(df: pd.DataFrame):
    """Donut chart for student risk distribution."""
    counts = df["risk_level"].value_counts().reset_index()
    counts.columns = ["risk_level", "count"]
    
    fig = px.pie(
        counts,
        names="risk_level",
        values="count",
        hole=0.55,
        title="Institutional Academic Risk Distribution",
        color="risk_level",
        color_discrete_map={
            "Low Risk": "#10B981",
            "Moderate Risk": "#F59E0B",
            "High Risk": "#EF4444"
        }
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(get_plotly_layout_defaults())
    fig.update_layout(height=380)
    return fig

def plot_student_radar(student_row: pd.Series):
    """Radar chart for an individual student across key academic pillars."""
    categories = ['Attendance', 'Study Routine', 'Prev Exam', 'Assignments', 'Math', 'Science', 'CS']
    
    # Normalize values to 0-100 scale
    att = min(float(student_row.get("attendance_rate", 75)), 100)
    study = min((float(student_row.get("study_hours_per_day", 4)) / 9.0) * 100, 100)
    prev = min(float(student_row.get("previous_exam_score", 65)), 100)
    assign = min(float(student_row.get("assignment_completion_rate", 75)), 100)
    math = min(float(student_row.get("math_score", 65)), 100)
    sci = min(float(student_row.get("science_score", 65)), 100)
    cs = min(float(student_row.get("computer_science_score", 65)), 100)
    
    values = [att, study, prev, assign, math, sci, cs]
    # close the loop
    values.append(values[0])
    cats = categories + [categories[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=cats,
        fill='toself',
        fillcolor='rgba(59, 130, 246, 0.35)',
        line=dict(color='#3B82F6', width=2),
        name=str(student_row.get("name", "Student"))
    ))
    # Benchmark trace (80%)
    bench = [80] * len(cats)
    fig.add_trace(go.Scatterpolar(
        r=bench,
        theta=cats,
        fill=None,
        line=dict(color='#10B981', width=1.5, dash='dash'),
        name="Target Benchmark (80%)"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#94A3B8", gridcolor="#1E293B"),
            angularaxis=dict(color="#F1F5F9", gridcolor="#1E293B")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#E2E8F0"),
        height=380,
        margin=dict(l=40, r=40, t=30, b=30),
        legend=dict(orientation="h", y=-0.15)
    )
    return fig

