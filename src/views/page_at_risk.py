"""
Page 4: At-Risk Student Intelligence View
Early-warning detection, vulnerability factor analysis, and prioritized intervention registry.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.ui_components import render_banner, render_kpi, get_plotly_layout_defaults

def render(df: pd.DataFrame):
    render_banner(
        title="At-Risk Student Intelligence & Early Warning System",
        subtitle="Proactively identify vulnerable students, isolate root risk factors, and coordinate targeted educational interventions.",
        tag="ACADEMIC EARLY WARNING SYSTEM"
    )

    # Filter Controls
    fcol1, fcol2, fcol3 = st.columns([1, 1, 1])
    with fcol1:
        tier_choice = st.selectbox("Select Risk Severity Tier", ["All At-Risk (High + Moderate)", "High Risk Only", "Moderate Risk Only", "All Cohort"])
    with fcol2:
        grade_choice = st.selectbox("Filter by Grade / Class", ["All Grades"] + sorted(list(df["grade_level"].unique())))
    with fcol3:
        max_attendance = st.slider("Attendance Threshold Filter (≤ %)", 40.0, 100.0, 75.0, 1.0)

    # Filter DataFrame
    at_risk_df = df.copy()
    if tier_choice == "High Risk Only":
        at_risk_df = at_risk_df[at_risk_df["risk_level"] == "High Risk"]
    elif tier_choice == "Moderate Risk Only":
        at_risk_df = at_risk_df[at_risk_df["risk_level"] == "Moderate Risk"]
    elif tier_choice == "All At-Risk (High + Moderate)":
        at_risk_df = at_risk_df[at_risk_df["risk_level"].isin(["High Risk", "Moderate Risk"])]
        
    if grade_choice != "All Grades":
        at_risk_df = at_risk_df[at_risk_df["grade_level"] == grade_choice]
        
    at_risk_df = at_risk_df[at_risk_df["attendance_rate"] <= max_attendance]

    # Metrics
    total_flagged = len(at_risk_df)
    high_count = len(at_risk_df[at_risk_df["risk_level"] == "High Risk"])
    avg_score_risk = at_risk_df["final_score"].mean() if total_flagged > 0 else 0
    avg_att_risk = at_risk_df["attendance_rate"].mean() if total_flagged > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    render_kpi(k1, "Flagged Students", f"{total_flagged}", "Meeting filter criteria", "#EF4444")
    render_kpi(k2, "High-Risk Priority", f"{high_count}", "Immediate intervention required", "#DC2626")
    render_kpi(k3, "Mean Score of Flagged", f"{avg_score_risk:.1f}%", "Cohort composite", "#F59E0B")
    render_kpi(k4, "Mean Attendance", f"{avg_att_risk:.1f}%", "Attendance deficit", "#3B82F6")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    if total_flagged == 0:
        st.info("No students match the selected risk criteria. Try expanding the attendance threshold or risk tiers.")
        return

    # Visual Breakdown of Risk Factors
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.markdown("#### 🚨 Distribution of Flagged Students by Grade")
        grade_dist = at_risk_df.groupby(["grade_level", "risk_level"]).size().reset_index(name="count")
        fig_bar = px.bar(
            grade_dist,
            x="grade_level",
            y="count",
            color="risk_level",
            barmode="group",
            color_discrete_map={"High Risk": "#EF4444", "Moderate Risk": "#F59E0B", "Low Risk": "#10B981"},
            title="At-Risk Volume by Academic Grade"
        )
        fig_bar.update_layout(get_plotly_layout_defaults())
        fig_bar.update_layout(height=340)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.markdown("#### 🔍 Primary Contributing Vulnerability Drivers")
        # Compute frequency of vulnerability conditions
        crit_att = (at_risk_df["attendance_rate"] < 65.0).sum()
        low_study = (at_risk_df["study_hours_per_day"] < 3.0).sum()
        miss_assign = (at_risk_df["assignment_completion_rate"] < 65.0).sum()
        weak_subs = (at_risk_df["subjects_needing_improvement"] >= 2).sum()
        sleep_dep = (at_risk_df["sleep_hours"] < 6.0).sum()
        
        drivers_df = pd.DataFrame({
            "Risk Driver": [
                "Critical Attendance (<65%)",
                "Weak in ≥2 Subjects",
                "Low Assignment Rate (<65%)",
                "Low Study Hours (<3h/day)",
                "Sleep Deprivation (<6h)"
            ],
            "Affected Students": [crit_att, weak_subs, miss_assign, low_study, sleep_dep]
        }).sort_values("Affected Students", ascending=True)

        fig_driver = px.bar(
            drivers_df,
            x="Affected Students",
            y="Risk Driver",
            orientation="h",
            color="Affected Students",
            color_continuous_scale="Reds",
            title="Frequency of Risk Factors in Cohort"
        )
        fig_driver.update_layout(get_plotly_layout_defaults())
        fig_driver.update_layout(height=340, coloraxis_showscale=False)
        st.plotly_chart(fig_driver, use_container_width=True)

    # Interactive Table of Identified Students
    st.markdown("#### 📋 Prioritized Intervention Registry")
    
    # Formulate intervention priority tags
    def assign_intervention(row):
        if row["risk_level"] == "High Risk":
            if row["attendance_rate"] < 65.0:
                return "1-on-1 Faculty Mentorship & Attendance Contract"
            elif row["subjects_needing_improvement"] >= 2:
                return "Intensive Subject Tutoring & Remedial Sessions"
            else:
                return "Comprehensive Academic Counseling"
        elif row["risk_level"] == "Moderate Risk":
            if row["assignment_completion_rate"] < 70.0:
                return "Assignment Submission Catch-Up Plan"
            else:
                return "Study Group Placement & Fortnightly Check-in"
        else:
            return "Standard Academic Progress Monitoring"

    display_df = at_risk_df[[
        "student_id", "name", "grade_level", "attendance_rate",
        "study_hours_per_day", "assignment_completion_rate",
        "subjects_needing_improvement", "final_score", "risk_level"
    ]].copy()
    display_df["Recommended Intervention Strategy"] = at_risk_df.apply(assign_intervention, axis=1)

    st.dataframe(
        display_df.rename(columns={
            "student_id": "Student ID",
            "name": "Full Name",
            "grade_level": "Grade Cohort",
            "attendance_rate": "Attendance (%)",
            "study_hours_per_day": "Study (h/d)",
            "assignment_completion_rate": "Assignments (%)",
            "subjects_needing_improvement": "Weak Subs",
            "final_score": "Score (%)",
            "risk_level": "Risk Tier"
        }),
        use_container_width=True,
        height=320
    )

    # Download Report Button
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    dcol1, dcol2 = st.columns([1, 2])
    with dcol1:
        st.download_button(
            label="📥 Download At-Risk CSV Report",
            data=csv_data,
            file_name="at_risk_students_intelligence_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    with dcol2:
        st.caption("ℹ️ The exported report contains individual risk scores, underlying vulnerability metrics, and designated intervention strategies.")

    # Institutional Standard Operating Procedure (SOP)
    st.markdown("""
    <div class="modern-card" style="margin-top: 15px; border-left: 4px solid #F59E0B;">
        <h5 style="margin-top: 0; color: #F59E0B;">📘 Institutional Counselor Protocol & Intervention Guidelines</h5>
        <div style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
            <strong>Step 1: Early Outreach:</strong> Academic mentors initiate contact with students within 3 business days of high-risk classification.<br>
            <strong>Step 2: Root-Cause Discovery:</strong> Ascertain whether academic decline is driven by conceptual gaps, attendance issues, or external life circumstances.<br>
            <strong>Step 3: Agreed Action Plan:</strong> Formulate a signed academic recovery agreement with concrete weekly milestones.<br>
            <strong>Step 4: Bi-Weekly Monitoring:</strong> Re-evaluate student performance metrics at 14-day intervals to verify progress.
        </div>
    </div>
    """, unsafe_allow_html=True)

