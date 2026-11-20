"""
Page 9: Responsible AI & Microsoft AI-901 Alignment View
Ethical governance, bias mitigation, human-in-the-loop principles, and transparent oversight.
"""

import streamlit as st
import pandas as pd
from src.ui_components import render_banner

def render(df: pd.DataFrame):
    render_banner(
        title="Responsible AI, Ethics & Microsoft AI-901 Principles",
        subtitle="Operationalizing ethical machine learning, algorithmic accountability, bias detection, and human-in-the-loop safeguards.",
        tag="RESPONSIBLE AI GOVERNANCE"
    )

    st.markdown("""
    <div class="modern-card" style="border-left: 4px solid #38BDF8;">
        <h4 style="margin-top:0; color: #38BDF8;">🏛️ Alignment with Microsoft AI-901 AI Fundamentals</h4>
        <p style="color: #CBD5E1; font-size: 0.92rem; line-height: 1.6; margin-bottom: 0;">
            The Microsoft AI-901 certification mandates that modern artificial intelligence systems must not only achieve 
            high predictive accuracy, but must also adhere to strict ethical governance frameworks. In educational environments, 
            algorithmic decisions directly impact student development and institutional equity. This system is architected around 
            the <strong>Six Core Microsoft Responsible AI Principles</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # The 6 Principles in a 2x3 Grid
    st.markdown("#### ⚖️ The Six Microsoft Principles of Responsible AI")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #10B981; height: 100%;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #10B981; margin-bottom: 6px;">
                1. Fairness (Algorithmic Equity)
            </div>
            <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                <strong>Requirement:</strong> AI systems must treat all individuals fairly without discriminating based on gender, race, socio-economic status, or background.<br>
                <strong>System Implementation:</strong> Demographic features (e.g., gender, parent education) are insulated from primary scoring weights, ensuring that predicted academic outcomes reflect demonstrated academic behaviors (study hours, attendance, assignments) rather than protected characteristics.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #3B82F6; height: 100%;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #3B82F6; margin-bottom: 6px;">
                2. Reliability & Safety
            </div>
            <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                <strong>Requirement:</strong> AI systems must operate consistently, reliably, and safely under normal as well as unexpected operational conditions.<br>
                <strong>System Implementation:</strong> Input parameters undergo strict schema bounds checking (e.g., attendance clipped to 0-100%, study hours bounded), missing values are safely imputed using medians, and model residuals are empirically bounded (MAE ±2.7 pts).
            </p>
        </div>
        """, unsafe_allow_html=True)

    p3, p4 = st.columns(2)
    with p3:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #8B5CF6; height: 100%;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #8B5CF6; margin-bottom: 6px;">
                3. Privacy & Security
            </div>
            <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                <strong>Requirement:</strong> Respect student privacy and safeguard personal data against unauthorized disclosure or manipulation.<br>
                <strong>System Implementation:</strong> Synthetic pseudo-identifiers (e.g., <code>STU-1001</code>) are used for analytics. No personally identifiable student contacts, residential addresses, or financial records are processed or retained.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with p4:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #F59E0B; height: 100%;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #F59E0B; margin-bottom: 6px;">
                4. Inclusiveness
            </div>
            <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                <strong>Requirement:</strong> AI should empower everyone and engage people with diverse needs, abilities, and academic backgrounds.<br>
                <strong>System Implementation:</strong> Prescriptive action plans provide tailored interventions for differing student learning velocities, from foundational remedial drills to honors enrichment trajectories.
            </p>
        </div>
        """, unsafe_allow_html=True)

    p5, p6 = st.columns(2)
    with p5:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #06B6D4; height: 100%;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #06B6D4; margin-bottom: 6px;">
                5. Transparency & Explainability
            </div>
            <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                <strong>Requirement:</strong> AI decisions must be understandable, interpretable, and verifiable by human educators and students.<br>
                <strong>System Implementation:</strong> Every prediction is accompanied by a feature impact decomposition chart explaining <em>why</em> the score was predicted, alongside global feature importances and confusion matrices in the AI Lab.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with p6:
        st.markdown("""
        <div class="modern-card" style="border-left: 4px solid #EF4444; height: 100%;">
            <div style="font-size: 1.15rem; font-weight: 700; color: #EF4444; margin-bottom: 6px;">
                6. Accountability
            </div>
            <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
                <strong>Requirement:</strong> Human operators and institutions remain ultimately accountable for the behavior and impact of AI solutions.<br>
                <strong>System Implementation:</strong> The system enforces a strict <strong>Human-in-the-Loop</strong> governance model. AI predictions serve exclusively as consultative alerts to educators, not as automated graders or disciplinary agents.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Bias in Academic Datasets
    st.markdown("#### 🔍 Understanding Bias in Academic Datasets")
    bcol1, bcol2 = st.columns(2)
    
    with bcol1:
        st.markdown("""
        <div class="modern-card">
            <h5 style="color: #F8FAFC; margin-top: 0;">⚠️ Sources of Educational Data Bias</h5>
            <ul style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6; margin-bottom: 0;">
                <li><strong>Historical Evaluation Bias:</strong> Past grading disparities can be mirrored and codified into model weights if historical marks reflect subjective instructor variance.</li>
                <li><strong>Proxy Correlation Traps:</strong> Features such as home computer access or private coaching can act as proxies for family income, creating unfair systemic penalties.</li>
                <li><strong>Self-Fulfilling Labeling Loops:</strong> Labeling a student as "High Risk" without empathetic guidance can demoralize learners and precipitate the exact negative outcome predicted.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with bcol2:
        st.markdown("""
        <div class="modern-card">
            <h5 style="color: #F8FAFC; margin-top: 0;">🛡️ Active Bias Mitigation Techniques</h5>
            <ul style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6; margin-bottom: 0;">
                <li><strong>Stratified Validation Splits:</strong> Ensures equitable representation across all performance brackets and cohorts during model evaluation.</li>
                <li><strong>Continuous Audit Cycles:</strong> Regular analysis of false positive and false negative rates across gender and cohort sub-groups.</li>
                <li><strong>Empowerment-Focused Framing:</strong> System language deliberately frames predictions around "Support Opportunities" and "Target Growth" rather than fixed student deficits.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Why Predictions Never Replace Educators
    st.markdown("""
    <div class="modern-card" style="border-left: 4px solid #EC4899; margin-top: 15px;">
        <h4 style="margin-top:0; color: #F472B6;">👩‍🏫 Why AI Predictions Must Never Replace Teachers</h4>
        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6; margin-bottom: 0;">
            Machine learning models recognize correlation patterns across tabular data, but they lack human empathy, contextual intuition, 
            and knowledge of extenuating personal circumstances (such as illness, family emergencies, or sudden personal motivation). 
            A student with a low statistical projection may achieve an extraordinary breakthrough through inspired mentorship. 
            <strong>Artificial Intelligence is a diagnostic flashlight, not an automated judge.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Formal Disclaimer
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; border-radius: 10px; padding: 16px 20px; margin-top: 20px;">
        <div style="color: #F8FAFC; font-weight: 700; font-size: 0.92rem; margin-bottom: 6px;">
            📜 Official Academic Use & Ethical Compliance Disclaimer
        </div>
        <div style="color: #94A3B8; font-size: 0.82rem; line-height: 1.55;">
            This software is developed strictly for educational, academic research, and decision-support purposes as part of an industrial internship curriculum.
            The predictions, risk classifications, and recommendations generated by this software do not constitute legally binding academic evaluations,
            admissions decisions, or disciplinary sanctions. Educational institutions deploying this platform must maintain human faculty oversight for all student welfare interventions.
        </div>
    </div>
    """, unsafe_allow_html=True)

