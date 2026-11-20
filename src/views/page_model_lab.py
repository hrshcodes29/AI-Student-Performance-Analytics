"""
Page 7: Model Insights & AI Lab View
Transparency, evaluation metrics, feature importance, confusion matrix, and ML architecture.
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.ui_components import render_banner, render_kpi, get_plotly_layout_defaults

METRICS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "model_metrics.json")

def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return None

def render(df: pd.DataFrame):
    render_banner(
        title="Model Insights, Evaluation & AI Architecture Lab",
        subtitle="Transparent machine learning engineering, empirical benchmarking, feature importance, and diagnostic metrics.",
        tag="MACHINE LEARNING LAB"
    )

    metrics = load_metrics()
    if not metrics:
        st.warning("⚠️ Model metrics have not been computed yet. Please run training in Dataset Management.")
        return

    # Top KPI Metrics on ML Pipeline
    best_reg = metrics.get("best_regressor_name", "Linear Regression")
    best_reg_metrics = metrics.get("best_regressor_metrics", {})
    best_clf = metrics.get("best_classifier_name", "Random Forest")
    best_clf_metrics = metrics.get("best_classifier_metrics", {})

    k1, k2, k3, k4 = st.columns(4)
    render_kpi(k1, "Best Regressor", best_reg, f"R² = {best_reg_metrics.get('R2', 0.90):.4f}", "#3B82F6")
    render_kpi(k2, "Regression MAE", f"±{best_reg_metrics.get('MAE', 2.7):.2f} pts", "Mean Absolute Error", "#10B981")
    render_kpi(k3, "Best Classifier", best_clf, f"F1 = {best_clf_metrics.get('F1-Score', 0.93):.4f}", "#8B5CF6")
    render_kpi(k4, "Classification Acc", f"{best_clf_metrics.get('Accuracy', 0.93)*100:.1f}%", "Out-of-sample test accuracy", "#06B6D4")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # ML Pipeline Architecture Diagram
    st.markdown("#### 🔄 End-to-End Machine Learning Pipeline Architecture")
    st.markdown("""
    <div class="modern-card" style="padding: 16px 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; text-align: center; gap: 10px;">
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; min-width: 140px; flex: 1;">
                <div style="font-size: 1.2rem;">📥</div>
                <div style="color: #F8FAFC; font-weight: 700; font-size: 0.88rem;">1. Data Ingestion</div>
                <div style="color: #94A3B8; font-size: 0.74rem;">1,000 Academic Records</div>
            </div>
            <div style="color: #38BDF8; font-size: 1.2rem;">➔</div>
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; min-width: 140px; flex: 1;">
                <div style="font-size: 1.2rem;">⚙️</div>
                <div style="color: #F8FAFC; font-weight: 700; font-size: 0.88rem;">2. Preprocessing</div>
                <div style="color: #94A3B8; font-size: 0.74rem;">Scaling + One-Hot Encode</div>
            </div>
            <div style="color: #38BDF8; font-size: 1.2rem;">➔</div>
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; min-width: 140px; flex: 1;">
                <div style="font-size: 1.2rem;">✂️</div>
                <div style="color: #F8FAFC; font-weight: 700; font-size: 0.88rem;">3. Train/Test Split</div>
                <div style="color: #94A3B8; font-size: 0.74rem;">80% Train / 20% Test</div>
            </div>
            <div style="color: #38BDF8; font-size: 1.2rem;">➔</div>
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; min-width: 140px; flex: 1;">
                <div style="font-size: 1.2rem;">🧠</div>
                <div style="color: #F8FAFC; font-weight: 700; font-size: 0.88rem;">4. Multi-Model Train</div>
                <div style="color: #94A3B8; font-size: 0.74rem;">Regression & Classification</div>
            </div>
            <div style="color: #38BDF8; font-size: 1.2rem;">➔</div>
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; min-width: 140px; flex: 1;">
                <div style="font-size: 1.2rem;">🎯</div>
                <div style="color: #F8FAFC; font-weight: 700; font-size: 0.88rem;">5. Live Inference</div>
                <div style="color: #94A3B8; font-size: 0.74rem;">Score + Risk + Insights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Multi-Model Comparative Benchmarks
    mcol1, mcol2 = st.columns(2)

    with mcol1:
        st.markdown("#### 📈 Regression Model Comparison (Score Prediction)")
        reg_comp = metrics.get("regression_comparison", {})
        df_reg = pd.DataFrame(reg_comp).T.reset_index().rename(columns={"index": "Algorithm"})
        st.dataframe(
            df_reg.style.highlight_max(subset=["R2"], color="#1E3A8A")
                        .highlight_min(subset=["MAE", "RMSE"], color="#14532D"),
            use_container_width=True,
            height=200
        )
        st.caption("ℹ️ Linear Regression and Ridge provide strong linear explanatory power, while Random Forest handles subtle feature interactions.")

    with mcol2:
        st.markdown("#### 🛡️ Classification Model Comparison (Risk Categorization)")
        clf_comp = metrics.get("classification_comparison", {})
        df_clf = pd.DataFrame(clf_comp).T.reset_index().rename(columns={"index": "Algorithm"})
        st.dataframe(
            df_clf.style.highlight_max(subset=["Accuracy", "F1-Score"], color="#14532D"),
            use_container_width=True,
            height=200
        )
        st.caption("ℹ️ Random Forest Classifier achieves superior out-of-sample F1-score across balanced risk classes.")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Feature Importance & Confusion Matrix
    chart_col1, chart_col2 = st.columns([1.1, 0.9])

    with chart_col1:
        st.markdown("#### 🌟 Global Feature Importance (Random Forest Gini)")
        feat_imp = metrics.get("feature_importance", {})
        df_imp = pd.DataFrame(list(feat_imp.items()), columns=["Feature", "Relative Importance (%)"]).head(9)
        df_imp["Feature"] = df_imp["Feature"].apply(lambda x: x.replace("_", " ").title())
        
        fig_imp = px.bar(
            df_imp,
            x="Relative Importance (%)",
            y="Feature",
            orientation="h",
            text="Relative Importance (%)",
            color="Relative Importance (%)",
            color_continuous_scale="Blues"
        )
        fig_imp.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_imp.update_layout(get_plotly_layout_defaults())
        fig_imp.update_layout(
            height=370,
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_imp, use_container_width=True)

    with chart_col2:
        st.markdown("#### 🔲 Test Set Confusion Matrix")
        cm = metrics.get("confusion_matrix", [])
        labels = metrics.get("class_labels", ["Low Risk", "Moderate Risk", "High Risk"])
        
        if cm:
            fig_cm = px.imshow(
                cm,
                x=[f"Pred: {l}" for l in labels],
                y=[f"Actual: {l}" for l in labels],
                color_continuous_scale="Purples",
                text_auto=True
            )
            fig_cm.update_layout(get_plotly_layout_defaults())
            fig_cm.update_layout(height=370)
            st.plotly_chart(fig_cm, use_container_width=True)

    # Regression Actual vs Predicted Scatter
    test_preds = metrics.get("test_sample_predictions", {})
    if test_preds:
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 🎯 Actual vs Predicted Final Score (Test Split Holdout)")
        
        scatter_df = pd.DataFrame({
            "Actual Score": test_preds.get("actual_scores", []),
            "Predicted Score": test_preds.get("predicted_scores", []),
            "Risk Tier": test_preds.get("actual_risks", [])
        })
        
        fig_scatter = px.scatter(
            scatter_df,
            x="Actual Score",
            y="Predicted Score",
            color="Risk Tier",
            color_discrete_map={"Low Risk": "#10B981", "Moderate Risk": "#F59E0B", "High Risk": "#EF4444"},
            hover_data=["Actual Score", "Predicted Score"],
            opacity=0.85
        )
        # Add 45 degree perfect prediction line
        min_v = min(scatter_df["Actual Score"].min(), scatter_df["Predicted Score"].min())
        max_v = max(scatter_df["Actual Score"].max(), scatter_df["Predicted Score"].max())
        fig_scatter.add_trace(go.Scatter(
            x=[min_v, max_v],
            y=[min_v, max_v],
            mode="lines",
            line=dict(color="#64748B", dash="dash"),
            name="Ideal 1:1 Fit"
        ))
        fig_scatter.update_layout(get_plotly_layout_defaults())
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Model Limitations & Assumptions
    st.markdown("""
    <div class="modern-card" style="margin-top: 15px; border-left: 4px solid #6366F1;">
        <h5 style="margin-top: 0; color: #818CF8;">🔬 Technical Assumptions & Boundary Conditions</h5>
        <div style="color: #94A3B8; font-size: 0.86rem; line-height: 1.6;">
            • <strong>Feature Independence & Linearity:</strong> Regression features are assumed to maintain monotonic relationships with academic outcomes.<br>
            • <strong>Out-of-Distribution Sensitivity:</strong> Students with unprecedented behavioral profiles (e.g., zero attendance with 99% test marks) may experience higher residual errors.<br>
            • <strong>Dynamic Drift:</strong> Models should undergo retraining at the conclusion of each academic semester to adapt to revised curriculum standards and grading rubrics.
        </div>
    </div>
    """, unsafe_allow_html=True)

