"""
Page 6: AI Recommendation Engine View
Dynamic prescriptive learning plans tailored to student metrics, weaknesses, and targets.
"""

import streamlit as st
import pandas as pd
from src.ui_components import render_banner, render_kpi
from src.recommender import generate_academic_recommendations

def render(df: pd.DataFrame):
    render_banner(
        title="AI Academic Recommendation Engine",
        subtitle="Data-driven prescriptive intelligence transforming analytical diagnostics into structured, actionable student improvement paths.",
        tag="PRESCRIPTIVE AI GUIDANCE"
    )

    # Mode Selector
    mode = st.radio(
        "Select Recommendation Target Source",
        ["Select from Cohort Database", "Build Custom Student Profile"],
        horizontal=True
    )

    if mode == "Select from Cohort Database":
        student_list = df["student_id"] + " — " + df["name"] + " (" + df["risk_level"] + ")"
        chosen = st.selectbox("Choose Student to Generate Action Plan", student_list, index=0)
        chosen_id = chosen.split(" — ")[0]
        student_row = df[df["student_id"] == chosen_id].iloc[0]
        student_dict = student_row.to_dict()
    else:
        st.markdown("##### 🛠️ Custom Profile Input")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            att = st.slider("Attendance Rate (%)", 40.0, 100.0, 68.0, 1.0, key="rec_att")
            study = st.slider("Study Hours/Day", 1.0, 9.5, 2.5, 0.5, key="rec_study")
        with c2:
            prev = st.slider("Previous Exam Score", 30.0, 100.0, 58.0, 1.0, key="rec_prev")
            assign = st.slider("Assignment Rate (%)", 30.0, 100.0, 65.0, 1.0, key="rec_assign")
        with c3:
            math = st.number_input("Math Score", 0.0, 100.0, 52.0, 1.0, key="rec_math")
            sci = st.number_input("Science Score", 0.0, 100.0, 56.0, 1.0, key="rec_sci")
        with c4:
            eng = st.number_input("English Score", 0.0, 100.0, 65.0, 1.0, key="rec_eng")
            cs = st.number_input("CS Score", 0.0, 100.0, 50.0, 1.0, key="rec_cs")
            
        student_dict = {
            "student_id": "SIM-PROFILE",
            "name": "Custom Profile",
            "attendance_rate": att,
            "study_hours_per_day": study,
            "previous_exam_score": prev,
            "assignment_completion_rate": assign,
            "sleep_hours": 6.5,
            "math_score": math,
            "science_score": sci,
            "english_score": eng,
            "computer_science_score": cs,
            "risk_level": "Moderate Risk" if prev >= 60 else "High Risk"
        }

    # Generate Recommendations
    rec_result = generate_academic_recommendations(
        student_dict,
        predicted_score=float(student_dict.get("final_score", student_dict.get("previous_exam_score", 65))),
        predicted_risk=student_dict.get("risk_level", "Moderate Risk")
    )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Summary Metrics Card
    curr_score = rec_result["current_score"]
    gain = rec_result["estimated_gain"]
    target_score = rec_result["target_potential_score"]

    k1, k2, k3, k4 = st.columns(4)
    render_kpi(k1, "Baseline Score", f"{curr_score:.1f}%", "Current evaluation", "#3B82F6")
    render_kpi(k2, "Potential Score Gain", f"+{gain:.1f} pts", "With prescribed regimen", "#10B981")
    render_kpi(k3, "Projected Target Score", f"{target_score:.1f}%", "Realistic semester target", "#06B6D4")
    render_kpi(k4, "Action Directives", f"{rec_result['total_recommendations']}", "Identified intervention areas", "#8B5CF6")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 📋 Comprehensive Prescriptive Intervention Plan")

    for idx, rec in enumerate(rec_result["recommendations"], 1):
        st.markdown(f"""
        <div class="modern-card" style="border-left: 5px solid {rec['badge_color']}; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <div>
                    <span style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em; color: #94A3B8; font-weight: 700;">
                        DIRECTIVE #{idx} &nbsp;•&nbsp; {rec['category']}
                    </span>
                    <h4 style="margin: 4px 0 0 0; color: #FFFFFF; font-size: 1.15rem;">
                        {rec['icon']} {rec['title']}
                    </h4>
                </div>
                <span style="background: {rec['badge_color']}25; color: {rec['badge_color']}; border: 1px solid {rec['badge_color']}40; padding: 4px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;">
                    {rec['priority']}
                </span>
            </div>
            
            <p style="color: #94A3B8; font-size: 0.9rem; margin-top: 8px; margin-bottom: 12px;">
                <strong>Diagnostic Context:</strong> {rec['observation']}
            </p>

            <div style="background: rgba(15, 23, 42, 0.75); border-radius: 8px; padding: 12px 16px; border: 1px solid #1E293B;">
                <div style="color: #38BDF8; font-weight: 600; font-size: 0.85rem; margin-bottom: 6px;">
                    🎯 Prescribed Action Steps:
                </div>
                <ul style="color: #E2E8F0; font-size: 0.88rem; margin: 0; padding-left: 20px; line-height: 1.6;">
                    {''.join(f'<li>{action}</li>' for action in rec['action_items'])}
                </ul>
            </div>

            <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #10B981; font-weight: 600; font-size: 0.82rem;">
                    📈 Projected Gain: {rec['estimated_impact']}
                </span>
                <span style="color: #64748B; font-size: 0.78rem;">
                    Recommended Review Interval: 14 Days
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Printable summary download
    summary_text = f"""ACADEMIC IMPROVEMENT ACTION PLAN
Student: {student_dict.get('name', 'Student')} (ID: {student_dict.get('student_id', 'N/A')})
Baseline Score: {curr_score:.1f}%
Projected Target Score: {target_score:.1f}% (Potential Gain: +{gain:.1f} pts)

PRESCRIPTIONS:
"""
    for idx, rec in enumerate(rec_result["recommendations"], 1):
        summary_text += f"\n{idx}. [{rec['priority']}] {rec['title']}\n"
        summary_text += f"   Context: {rec['observation']}\n"
        for act in rec["action_items"]:
            summary_text += f"   - {act}\n"
            
    st.download_button(
        label="📄 Export Action Plan as Text File",
        data=summary_text,
        file_name=f"academic_action_plan_{student_dict.get('student_id', 'student')}.txt",
        mime="text/plain"
    )

