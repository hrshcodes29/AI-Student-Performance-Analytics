"""
Page 2: AI Student Prediction View
Interactive prediction engine with feature impact analysis and personalized guidance.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.ui_components import render_banner, get_plotly_layout_defaults
from src.ml_pipeline import predict_single_student
from src.recommender import generate_academic_recommendations

def render(df: pd.DataFrame):
    render_banner(
        title="AI Student Performance & Risk Predictor",
        subtitle="Leverage trained supervised machine learning algorithms to forecast academic outcomes and identify risk indicators.",
        tag="PREDICTIVE INFERENCE ENGINE"
    )

    # Preset profiles for evaluator convenience
    st.markdown("#### ⚡ Quick Preset Demonstrations")
    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
    
    preset = None
    with pcol1:
        if st.button("🌟 High-Performing Student", use_container_width=True):
            preset = {
                "study_hours": 6.8, "attendance": 94.5, "prev_score": 88.0,
                "assignment_rate": 95.0, "sleep": 7.5, "math": 90.0,
                "science": 92.0, "english": 86.0, "cs": 94.0,
                "grade": "Grade 12", "gender": "Female", "parent_edu": "Master's"
            }
    with pcol2:
        if st.button("⚖️ Moderate-Risk Student", use_container_width=True):
            preset = {
                "study_hours": 3.8, "attendance": 72.0, "prev_score": 64.0,
                "assignment_rate": 70.0, "sleep": 6.5, "math": 62.0,
                "science": 65.0, "english": 68.0, "cs": 60.0,
                "grade": "Grade 11", "gender": "Male", "parent_edu": "Bachelor's"
            }
    with pcol3:
        if st.button("🚨 High-Risk Student", use_container_width=True):
            preset = {
                "study_hours": 1.8, "attendance": 54.0, "prev_score": 46.0,
                "assignment_rate": 45.0, "sleep": 5.0, "math": 44.0,
                "science": 48.0, "english": 52.0, "cs": 42.0,
                "grade": "Grade 10", "gender": "Male", "parent_edu": "High School"
            }
    with pcol4:
        if st.button("🔄 Reset to Default Values", use_container_width=True):
            st.session_state["pred_loaded"] = False
            preset = None

    if preset:
        st.session_state["pred_preset"] = preset
        st.session_state["pred_loaded"] = True

    current_preset = st.session_state.get("pred_preset", {})

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Input Form
    with st.form("student_prediction_form"):
        st.markdown("#### 📝 Student Academic Profile Input")
        
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student Identifier", value="STU-PRED-2026")
            name = st.text_input("Student Full Name", value="Alex Morgan")
            gender = st.selectbox("Gender", ["Female", "Male", "Non-Binary"], index=0 if current_preset.get("gender") == "Female" else 1)
            grade_level = st.selectbox(
                "Grade / Academic Cohort",
                ["Grade 10", "Grade 11", "Grade 12", "Undergrad Year 1", "Undergrad Year 2"],
                index=2 if not current_preset else ["Grade 10", "Grade 11", "Grade 12", "Undergrad Year 1", "Undergrad Year 2"].index(current_preset.get("grade", "Grade 12"))
            )
            study_hours = st.slider(
                "Daily Study Hours (Focused Study)",
                min_value=1.0, max_value=9.5,
                value=float(current_preset.get("study_hours", 4.5)),
                step=0.1
            )
            attendance_rate = st.slider(
                "Class Attendance Rate (%)",
                min_value=40.0, max_value=100.0,
                value=float(current_preset.get("attendance", 82.0)),
                step=0.5
            )
            prev_exam = st.slider(
                "Previous Semester Exam Score (%)",
                min_value=30.0, max_value=100.0,
                value=float(current_preset.get("prev_score", 70.0)),
                step=0.5
            )

        with col2:
            assignment_rate = st.slider(
                "Assignment Completion Rate (%)",
                min_value=30.0, max_value=100.0,
                value=float(current_preset.get("assignment_rate", 80.0)),
                step=0.5
            )
            sleep_hours = st.slider(
                "Average Sleep Hours / Night",
                min_value=4.0, max_value=10.0,
                value=float(current_preset.get("sleep", 7.0)),
                step=0.5
            )
            parent_edu = st.selectbox(
                "Parent Education Level",
                ["High School", "Associate", "Bachelor's", "Master's", "Doctorate"],
                index=2 if not current_preset else ["High School", "Associate", "Bachelor's", "Master's", "Doctorate"].index(current_preset.get("parent_edu", "Bachelor's"))
            )
            internet_access = st.selectbox("High-Speed Internet Access at Home", ["Yes", "No"], index=0)
            extracurricular = st.selectbox("Participates in Extracurriculars", ["Yes", "No"], index=0)
            
            st.markdown("**Subject-Level Diagnostic Marks (0-100)**")
            scol1, scol2 = st.columns(2)
            with scol1:
                math_score = st.number_input("Mathematics", 0.0, 100.0, float(current_preset.get("math", 72.0)), 1.0)
                science_score = st.number_input("Science", 0.0, 100.0, float(current_preset.get("science", 74.0)), 1.0)
            with scol2:
                english_score = st.number_input("English", 0.0, 100.0, float(current_preset.get("english", 76.0)), 1.0)
                cs_score = st.number_input("Computer Science", 0.0, 100.0, float(current_preset.get("cs", 78.0)), 1.0)

        submit_btn = st.form_submit_button("🚀 Run AI Prediction Analysis", use_container_width=True)

    # If submitted or preset loaded
    if submit_btn or st.session_state.get("pred_loaded", False):
        weak_count = sum(1 for s in [math_score, science_score, english_score, cs_score] if s < 60.0)
        
        student_input = {
            "student_id": student_id,
            "name": name,
            "gender": gender,
            "grade_level": grade_level,
            "study_hours_per_day": study_hours,
            "attendance_rate": attendance_rate,
            "previous_exam_score": prev_exam,
            "assignment_completion_rate": assignment_rate,
            "parent_education_level": parent_edu,
            "internet_access": internet_access,
            "extracurricular_activities": extracurricular,
            "sleep_hours": sleep_hours,
            "math_score": math_score,
            "science_score": science_score,
            "english_score": english_score,
            "computer_science_score": cs_score,
            "subjects_needing_improvement": weak_count
        }

        # Run Inference
        with st.spinner("Analyzing profile through trained machine learning models..."):
            try:
                results = predict_single_student(student_input)
            except Exception as e:
                st.error(f"Inference error: {str(e)}")
                return

        predicted_score = results["predicted_score"]
        predicted_risk = results["predicted_risk"]
        probs = results.get("risk_probabilities", {})
        feature_contribs = results["feature_contributions"]

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("### 🎯 Machine Learning Prediction Results")

        # Results Display Card
        rcol1, rcol2, rcol3 = st.columns([1, 1, 1])
        
        # Risk Badge color
        risk_color = "#10B981" if predicted_risk == "Low Risk" else ("#F59E0B" if predicted_risk == "Moderate Risk" else "#EF4444")
        
        with rcol1:
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid #3B82F6;">
                <div class="kpi-title">Predicted Academic Score</div>
                <div class="kpi-value" style="color: #60A5FA;">{predicted_score:.1f} / 100</div>
                <div class="kpi-subtitle">Estimated final composite score</div>
            </div>
            """, unsafe_allow_html=True)

        with rcol2:
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {risk_color};">
                <div class="kpi-title">Predicted Risk Classification</div>
                <div class="kpi-value" style="color: {risk_color}; font-size: 1.55rem;">{predicted_risk}</div>
                <div class="kpi-subtitle">Early warning categorization</div>
            </div>
            """, unsafe_allow_html=True)

        with rcol3:
            pass_status = "Likely On-Track" if predicted_score >= 60 else "Requires Remediation"
            status_color = "#10B981" if predicted_score >= 60 else "#EF4444"
            st.markdown(f"""
            <div class="kpi-card" style="border-left: 4px solid {status_color};">
                <div class="kpi-title">Curriculum Progression Status</div>
                <div class="kpi-value" style="color: {status_color}; font-size: 1.45rem;">{pass_status}</div>
                <div class="kpi-subtitle">Pass threshold benchmark: 60.0%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # Feature Contribution Waterfall / Breakdown Chart
        c_chart1, c_chart2 = st.columns([1.2, 0.8])
        
        with c_chart1:
            st.markdown("#### 🔬 Feature Impact Breakdown")
            df_contrib = pd.DataFrame(feature_contribs[:7])
            
            fig_bar = go.Figure(go.Bar(
                x=df_contrib["impact_score"],
                y=df_contrib["feature"],
                orientation='h',
                marker=dict(
                    color=df_contrib["impact_score"].apply(lambda x: "#10B981" if x >= 0 else "#EF4444")
                ),
                text=df_contrib["impact_score"].apply(lambda x: f"{x:+.1f} pts"),
                textposition="outside"
            ))
            fig_bar.update_layout(get_plotly_layout_defaults())
            fig_bar.update_layout(
                title="Relative Score Contribution (vs Cohort Benchmark)",
                xaxis_title="Score Impact (Points)",
                yaxis=dict(autorange="reversed"),
                height=350
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with c_chart2:
            st.markdown("#### 🎲 Model Risk Probabilities")
            if probs:
                prob_df = pd.DataFrame(list(probs.items()), columns=["Risk Level", "Probability (%)"])
                fig_prob = go.Figure(go.Pie(
                    labels=prob_df["Risk Level"],
                    values=prob_df["Probability (%)"],
                    hole=0.6,
                    marker=dict(colors=["#EF4444", "#10B981", "#F59E0B"])
                ))
                fig_prob.update_layout(get_plotly_layout_defaults())
                fig_prob.update_layout(
                    title="Softmax Risk Distribution",
                    height=350,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                st.plotly_chart(fig_prob, use_container_width=True)

        # Action Recommendations
        rec_data = generate_academic_recommendations(student_input, predicted_score, predicted_risk)
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 💡 Tailored Academic Intervention Recommendations")
        
        for item in rec_data["recommendations"]:
            st.markdown(f"""
            <div class="modern-card" style="border-left: 4px solid {item['badge_color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div style="font-size: 1.05rem; font-weight: 700; color: #FFFFFF;">
                        {item['icon']} {item['title']}
                    </div>
                    <span style="background: {item['badge_color']}25; color: {item['badge_color']}; padding: 3px 10px; border-radius: 999px; font-size: 0.75rem; font-weight: 600;">
                        {item['priority']}
                    </span>
                </div>
                <div style="color: #94A3B8; font-size: 0.88rem; margin-bottom: 10px;">
                    {item['observation']}
                </div>
                <div style="color: #E2E8F0; font-size: 0.85rem;">
                    <strong>Action Items:</strong>
                    <ul style="margin-top: 4px; margin-bottom: 6px;">
                        {''.join(f'<li>{act}</li>' for act in item['action_items'])}
                    </ul>
                </div>
                <div style="color: #38BDF8; font-size: 0.8rem; font-weight: 600; margin-top: 6px;">
                    📈 Expected Academic Impact: {item['estimated_impact']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Responsible AI Disclaimer Box
        st.markdown("""
        <div style="background: rgba(30, 41, 59, 0.5); border: 1px dashed #64748B; border-radius: 10px; padding: 14px 18px; margin-top: 20px;">
            <div style="color: #94A3B8; font-size: 0.82rem; line-height: 1.5;">
                <strong style="color: #F8FAFC;">⚠️ Responsible AI & Model Limitations Advisory:</strong>
                Predictions generated by this system are statistical approximations derived from historical academic patterns.
                They are intended strictly as early-support decision aids for faculty and counselors, <em>never</em> as automated punitive measures, 
                admissions decisions, or definitive assessments of a student's intrinsic capability. Always exercise human judgment and contextual awareness.
            </div>
        </div>
        """, unsafe_allow_html=True)

