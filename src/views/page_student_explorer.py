"""
Page 3: Student Explorer View
Comprehensive searchable individual student dossier with multidimensional analytics.
"""

import streamlit as st
import pandas as pd
from src.ui_components import render_banner, render_kpi, plot_student_radar
from src.recommender import generate_academic_recommendations

def render(df: pd.DataFrame):
    render_banner(
        title="Student Explorer & Individual Dossier",
        subtitle="Search, audit, and analyze individual student academic performance, behavioral factors, and tailored support paths.",
        tag="STUDENT PROFILE EXPLORER"
    )

    # Search & Filter Controls
    scol1, scol2 = st.columns([1.5, 1])
    with scol1:
        # Autocomplete student selection
        student_list = df["student_id"] + " — " + df["name"] + " (" + df["grade_level"] + ")"
        selected_option = st.selectbox("Search & Select Student Profile", student_list, index=0)
        selected_id = selected_option.split(" — ")[0]
        student_row = df[df["student_id"] == selected_id].iloc[0]

    with scol2:
        quick_filter = st.selectbox(
            "Jump to Student by Risk Category",
            ["All Cohort", "High Risk Only", "Moderate Risk Only", "Low Risk Only"]
        )
        if quick_filter != "All Cohort":
            target_risk = quick_filter.replace(" Only", "")
            subset = df[df["risk_level"] == target_risk]
            if not subset.empty:
                st.caption(f"Cohort contains {len(subset)} students in {target_risk} tier.")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Student Dossier Header Card
    risk_level = student_row["risk_level"]
    risk_color = "#10B981" if risk_level == "Low Risk" else ("#F59E0B" if risk_level == "Moderate Risk" else "#EF4444")
    
    st.markdown(f"""
    <div class="modern-card" style="border-left: 5px solid {risk_color};">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <h3 style="margin: 0; color: #FFFFFF; font-size: 1.5rem;">{student_row['name']}</h3>
                <div style="color: #94A3B8; font-size: 0.9rem; margin-top: 4px;">
                    <strong>ID:</strong> <code>{student_row['student_id']}</code> &nbsp;|&nbsp; 
                    <strong>Cohort:</strong> {student_row['grade_level']} &nbsp;|&nbsp; 
                    <strong>Gender:</strong> {student_row['gender']} &nbsp;|&nbsp;
                    <strong>Academic Status:</strong> {student_row.get('academic_status', 'Regular')}
                </div>
            </div>
            <div style="margin-top: 8px;">
                <span class="badge-{'low' if risk_level=='Low Risk' else ('mod' if risk_level=='Moderate Risk' else 'high')}" style="font-size: 0.95rem; padding: 6px 16px;">
                    {risk_level}
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics for this Student
    k1, k2, k3, k4, k5 = st.columns(5)
    render_kpi(k1, "Final Score", f"{student_row['final_score']:.1f}%", "Overall Composite", "#3B82F6")
    render_kpi(k2, "Attendance", f"{student_row['attendance_rate']:.1f}%", "Lecture Attendance", "#10B981")
    render_kpi(k3, "Daily Study", f"{student_row['study_hours_per_day']:.1f} hrs", "Focused Self-Study", "#06B6D4")
    render_kpi(k4, "Assignments", f"{student_row['assignment_completion_rate']:.1f}%", "Submission Rate", "#8B5CF6")
    render_kpi(k5, "Sleep Hours", f"{student_row['sleep_hours']:.1f} hrs", "Average / Night", "#F59E0B")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Detailed Visuals
    rcol1, rcol2 = st.columns([1.1, 0.9])
    
    with rcol1:
        st.markdown("#### 🎯 Multidimensional Academic Radar")
        st.plotly_chart(plot_student_radar(student_row), use_container_width=True)

    with rcol2:
        st.markdown("#### 📚 Subject Marks Breakdown")
        subjects = [
            ("Mathematics", student_row["math_score"]),
            ("Science", student_row["science_score"]),
            ("English Language", student_row["english_score"]),
            ("Computer Science", student_row["computer_science_score"]),
        ]
        
        for sub_name, score in subjects:
            bar_color = "#10B981" if score >= 75 else ("#F59E0B" if score >= 60 else "#EF4444")
            st.markdown(f"""
            <div style="background: rgba(17, 24, 39, 0.6); padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border: 1px solid #1E293B;">
                <div style="display: flex; justify-content: space-between; font-size: 0.88rem; margin-bottom: 4px;">
                    <span style="color: #E2E8F0; font-weight: 600;">{sub_name}</span>
                    <span style="color: {bar_color}; font-weight: 700;">{score:.1f} / 100</span>
                </div>
                <div style="background: #1E293B; border-radius: 999px; height: 6px; overflow: hidden;">
                    <div style="background: {bar_color}; width: {min(score, 100):.1f}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid #1E293B; border-radius: 8px; padding: 12px; margin-top: 10px;">
            <div style="color: #94A3B8; font-size: 0.8rem;">
                <strong>Parent Education:</strong> {student_row['parent_education_level']} &nbsp;|&nbsp;
                <strong>Home Internet:</strong> {student_row['internet_access']} &nbsp;|&nbsp;
                <strong>Extracurriculars:</strong> {student_row['extracurricular_activities']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Personalized Support Recommendations
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🧭 Tailored Academic Action Plan")
    recs = generate_academic_recommendations(student_row.to_dict(), student_row["final_score"], student_row["risk_level"])
    
    for item in recs["recommendations"]:
        st.markdown(f"""
        <div class="modern-card" style="border-left: 4px solid {item['badge_color']}; padding: 14px 18px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-weight: 700; color: #FFFFFF; font-size: 0.95rem;">{item['icon']} {item['title']}</span>
                <span style="background: {item['badge_color']}20; color: {item['badge_color']}; font-size: 0.72rem; padding: 2px 8px; border-radius: 999px; font-weight: 600;">{item['priority']}</span>
            </div>
            <div style="color: #94A3B8; font-size: 0.84rem; margin-bottom: 6px;">{item['observation']}</div>
            <ul style="color: #E2E8F0; font-size: 0.82rem; margin: 0; padding-left: 20px;">
                {''.join(f'<li>{act}</li>' for act in item['action_items'])}
            </ul>
        </div>
        """, unsafe_allow_html=True)

