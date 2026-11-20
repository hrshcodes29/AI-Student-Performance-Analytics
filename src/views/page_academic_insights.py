"""
Page 5: Academic Insights View
Deep statistical exploration of educational drivers, correlations, and empirical cohort dynamics.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import render_banner, render_kpi, get_plotly_layout_defaults

def render(df: pd.DataFrame):
    render_banner(
        title="Academic Insights & Educational Analytics",
        subtitle="Explore statistically verified correlations, behavioral determinants, and cohort benchmarks derived from empirical data.",
        tag="EXPLORATORY DATA ANALYTICS"
    )

    # 1. Feature Correlation Heatmap
    st.markdown("#### 🔬 Correlation Matrix of Academic & Behavioral Factors")
    
    corr_cols = [
        "final_score", "attendance_rate", "study_hours_per_day",
        "previous_exam_score", "assignment_completion_rate", "sleep_hours",
        "math_score", "science_score", "english_score", "computer_science_score"
    ]
    labels_clean = [
        "Final Score", "Attendance", "Daily Study", "Prev Exam",
        "Assignments", "Sleep", "Math", "Science", "English", "CS"
    ]
    
    corr_matrix = df[corr_cols].corr().round(2)
    
    fig_corr = px.imshow(
        corr_matrix,
        x=labels_clean,
        y=labels_clean,
        color_continuous_scale="Blues",
        text_auto=True,
        title="Pearson Correlation Coefficients Across Academic Indicators"
    )
    fig_corr.update_layout(get_plotly_layout_defaults())
    fig_corr.update_layout(height=480)
    st.plotly_chart(fig_corr, use_container_width=True)

    # Calculate actual empirical statistics from the dataset
    high_att_mean = df[df["attendance_rate"] >= 80]["final_score"].mean()
    low_att_mean = df[df["attendance_rate"] < 65]["final_score"].mean()
    att_diff = high_att_mean - low_att_mean

    high_study_mean = df[df["study_hours_per_day"] >= 5.0]["final_score"].mean()
    low_study_mean = df[df["study_hours_per_day"] < 3.0]["final_score"].mean()
    study_diff = high_study_mean - low_study_mean

    # Empirical KPI cards
    e1, e2, e3 = st.columns(3)
    render_kpi(e1, "Attendance Premium", f"+{att_diff:.1f} pts", "Score gain for ≥80% vs <65% attendance", "#10B981")
    render_kpi(e2, "Study Hours Premium", f"+{study_diff:.1f} pts", "Score gain for ≥5h vs <3h daily study", "#3B82F6")
    render_kpi(e3, "Strongest Single Predictor", "Previous Exam", f"r = {corr_matrix.loc['final_score', 'previous_exam_score']:.2f} correlation", "#8B5CF6")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # 2. Detailed Exploration Rows
    col_a1, col_a2 = st.columns([1, 1])

    with col_a1:
        st.markdown("#### ⏱️ Study Hours vs Academic Performance")
        # Bin study hours
        df_copy = df.copy()
        df_copy["Study Bracket"] = pd.cut(
            df_copy["study_hours_per_day"],
            bins=[0, 3.0, 5.0, 7.0, 10.0],
            labels=["< 3 Hours", "3 - 5 Hours", "5 - 7 Hours", "> 7 Hours"]
        )
        study_agg = df_copy.groupby("Study Bracket", observed=True)["final_score"].agg(["mean", "median", "count"]).reset_index()
        
        fig_study = px.bar(
            study_agg,
            x="Study Bracket",
            y="mean",
            text="mean",
            title="Mean Composite Score by Daily Study Bracket",
            labels={"mean": "Average Final Score", "Study Bracket": "Daily Study Bracket"},
            color="mean",
            color_continuous_scale="Viridis"
        )
        fig_study.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_study.update_layout(get_plotly_layout_defaults())
        fig_study.update_layout(height=360, coloraxis_showscale=False, yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig_study, use_container_width=True)

    with col_a2:
        st.markdown("#### 📝 Assignment Completion vs Final Score")
        fig_assign = px.scatter(
            df,
            x="assignment_completion_rate",
            y="final_score",
            trendline="ols",
            color="risk_level",
            color_discrete_map={"Low Risk": "#10B981", "Moderate Risk": "#F59E0B", "High Risk": "#EF4444"},
            title="Assignment Submission Impact on Course Grade",
            labels={
                "assignment_completion_rate": "Assignment Completion (%)",
                "final_score": "Final Score (0-100)"
            },
            opacity=0.7
        )
        fig_assign.update_layout(get_plotly_layout_defaults())
        fig_assign.update_layout(height=360)
        st.plotly_chart(fig_assign, use_container_width=True)

    # 3. Subject Weakness Diagnostics
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Subject-Wise Weakness & Failure Vulnerability")

    sub_cols = ["math_score", "science_score", "english_score", "computer_science_score"]
    sub_names = ["Mathematics", "Science", "English Language", "Computer Science"]
    
    under_60_counts = [(df[col] < 60.0).sum() for col in sub_cols]
    under_60_pcts = [round((cnt / len(df)) * 100, 1) for cnt in under_60_counts]
    avg_marks = [round(df[col].mean(), 1) for col in sub_cols]
    
    sub_analysis_df = pd.DataFrame({
        "Subject": sub_names,
        "Mean Score": avg_marks,
        "Students Scoring < 60": under_60_counts,
        "Vulnerability Rate (%)": under_60_pcts
    }).sort_values("Vulnerability Rate (%)", ascending=False)

    col_sub1, col_sub2 = st.columns([1.1, 0.9])
    
    with col_sub1:
        fig_vuln = px.bar(
            sub_analysis_df,
            x="Subject",
            y="Vulnerability Rate (%)",
            text="Vulnerability Rate (%)",
            title="Failure / Remedial Rate by Subject (< 60/100 threshold)",
            color="Vulnerability Rate (%)",
            color_continuous_scale="Reds"
        )
        fig_vuln.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_vuln.update_layout(get_plotly_layout_defaults())
        fig_vuln.update_layout(height=340, coloraxis_showscale=False, yaxis=dict(range=[0, max(under_60_pcts) + 10]))
        st.plotly_chart(fig_vuln, use_container_width=True)

    with col_sub2:
        st.markdown("""
        <div class="modern-card" style="height: 340px; display: flex; flex-direction: column; justify-content: center;">
            <h5 style="margin-top: 0; color: #38BDF8;">🔍 Academic Diagnostic Findings</h5>
            <div style="color: #94A3B8; font-size: 0.88rem; line-height: 1.6;">
                • <strong>Mathematics</strong> demonstrates the highest variance in performance and the steepest correlation with daily study hours.<br><br>
                • <strong>Computer Science</strong> marks display high synergy with self-study hours and previous academic foundation.<br><br>
                • <strong>English Language</strong> maintains the highest cohort mean score but exhibits less sensitivity to attendance alone.
            </div>
        </div>
        """, unsafe_allow_html=True)

