"""
Page 8: Dataset Management & Ingestion Center
Dataset preview, schema validation, CSV upload, missing value imputation, and model retraining.
"""

import os
import streamlit as st
import pandas as pd
from src.ui_components import render_banner, render_kpi
from src.data_loader import validate_uploaded_csv, TEMPLATE_DATA_PATH, DEFAULT_DATA_PATH
from src.ml_pipeline import train_and_evaluate

def render(df: pd.DataFrame):
    render_banner(
        title="Dataset Management & Ingestion Center",
        subtitle="Inspect active student data, validate custom CSV uploads, handle missing records, and trigger dynamic model retraining.",
        tag="DATASET & ETL INGESTION"
    )

    # Top KPI Metrics on Active Dataset
    total_records = len(df)
    total_cols = len(df.columns)
    missing_cells = df.isnull().sum().sum()
    memory_kb = df.memory_usage(deep=True).sum() / 1024

    k1, k2, k3, k4 = st.columns(4)
    render_kpi(k1, "Active Records", f"{total_records:,}", "Loaded in memory", "#3B82F6")
    render_kpi(k2, "Feature Columns", f"{total_cols}", "Academic indicators", "#10B981")
    render_kpi(k3, "Missing Values", f"{missing_cells}", "Zero imputation needed", "#06B6D4")
    render_kpi(k4, "Memory Usage", f"{memory_kb:.1f} KB", "Optimized DataFrame", "#8B5CF6")

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Tabs for Data Operations
    tab1, tab2, tab3 = st.tabs(["📊 Active Dataset Preview", "📤 Upload Custom CSV", "📥 Download Data & Templates"])

    with tab1:
        st.markdown("#### 📋 Active Cohort Records")
        
        # Search & Column filter
        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            search_txt = st.text_input("Filter records by keyword:", "", key="data_search")
        with col_s2:
            show_cols = st.multiselect(
                "Select visible columns:",
                list(df.columns),
                default=[
                    "student_id", "name", "grade_level", "study_hours_per_day",
                    "attendance_rate", "previous_exam_score", "assignment_completion_rate",
                    "final_score", "risk_level"
                ]
            )

        preview_df = df.copy()
        if search_txt.strip():
            s = search_txt.strip().lower()
            mask = preview_df.astype(str).apply(lambda row: row.str.lower().str.contains(s).any(), axis=1)
            preview_df = preview_df[mask]

        if show_cols:
            st.dataframe(preview_df[show_cols], use_container_width=True, height=360)
        else:
            st.dataframe(preview_df, use_container_width=True, height=360)

        st.caption(f"Showing {len(preview_df)} of {len(df)} total students.")

    with tab2:
        st.markdown("#### 📤 Upload Custom Student Dataset")
        st.markdown("""
        Upload your institution's CSV file to dynamically analyze student cohorts or retrain the predictive machine learning models.
        The system automatically validates required columns and safely imputes missing values.
        """)

        uploaded_file = st.file_uploader("Select a CSV file to upload", type=["csv"])

        if uploaded_file is not None:
            is_valid, message, parsed_df = validate_uploaded_csv(uploaded_file)
            
            if is_valid:
                st.success(f"✅ {message}")
                st.markdown("##### Uploaded Data Preview (First 5 Rows):")
                st.dataframe(parsed_df.head(5), use_container_width=True)

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🚀 Apply as Active Dataset (Whole App)", use_container_width=True):
                        st.session_state["active_df"] = parsed_df
                        st.success("🎉 Uploaded dataset is now active across all dashboard pages!")
                        st.rerun()

                with col_btn2:
                    if st.button("🧠 Retrain AI Models on This Dataset", use_container_width=True):
                        temp_save_path = os.path.join(os.path.dirname(DEFAULT_DATA_PATH), "custom_uploaded_data.csv")
                        parsed_df.to_csv(temp_save_path, index=False)
                        with st.spinner("Retraining Regression & Classification models on new data..."):
                            try:
                                new_metrics = train_and_evaluate(temp_save_path)
                                st.session_state["active_df"] = parsed_df
                                st.success(f"🎉 Model retrained! New Regressor R²: {new_metrics['best_regressor_metrics']['R2']}, Classifier Acc: {new_metrics['best_classifier_metrics']['Accuracy']}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Retraining failed: {str(e)}")
            else:
                st.error(f"❌ Validation Error: {message}")

    with tab3:
        st.markdown("#### 📥 Export Data & Standardized Templates")
        
        down_col1, down_col2 = st.columns(2)
        
        with down_col1:
            st.markdown("""
            <div class="modern-card">
                <h5 style="margin-top:0; color: #38BDF8;">📄 Download Active Processed Dataset</h5>
                <p style="color: #94A3B8; font-size: 0.85rem;">
                    Export the complete 1,000 student dataset with all calculated features, risk levels, and predicted academic statuses.
                </p>
            </div>
            """, unsafe_allow_html=True)
            active_csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Full Processed CSV",
                data=active_csv,
                file_name="processed_student_performance_data.csv",
                mime="text/csv",
                use_container_width=True
            )

        with down_col2:
            st.markdown("""
            <div class="modern-card">
                <h5 style="margin-top:0; color: #10B981;">📋 Download Standardized CSV Template</h5>
                <p style="color: #94A3B8; font-size: 0.85rem;">
                    Download an empty/sample formatted CSV template with required column headers for bulk cohort upload.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if os.path.exists(TEMPLATE_DATA_PATH):
                with open(TEMPLATE_DATA_PATH, "rb") as f:
                    template_bytes = f.read()
                st.download_button(
                    label="📥 Download Sample Template CSV",
                    data=template_bytes,
                    file_name="student_data_upload_template.csv",
                    mime="text/csv",
                    use_container_width=True
                )

