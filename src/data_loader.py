"""
Data Loader & Validator for AI Student Performance Analytics
Handles loading, caching, uploading, validation, and preprocessing of student datasets.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st

DEFAULT_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "student_performance_data.csv")
TEMPLATE_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "template_upload.csv")

REQUIRED_NUMERICAL_COLS = [
    "study_hours_per_day",
    "attendance_rate",
    "previous_exam_score",
    "assignment_completion_rate",
    "sleep_hours",
    "math_score",
    "science_score",
    "english_score",
    "computer_science_score"
]

OPTIONAL_COLS = [
    "student_id",
    "name",
    "gender",
    "grade_level",
    "parent_education_level",
    "internet_access",
    "extracurricular_activities",
    "subjects_needing_improvement",
    "final_score",
    "risk_level",
    "academic_status"
]

@st.cache_data(show_spinner=False)
def load_default_data() -> pd.DataFrame:
    if os.path.exists(DEFAULT_DATA_PATH):
        df = pd.read_csv(DEFAULT_DATA_PATH)
        return df
    else:
        # Fallback dataset generation if not present
        from data.generate_dataset import generate_student_dataset
        df = generate_student_dataset(n_samples=1000, random_state=42)
        df.to_csv(DEFAULT_DATA_PATH, index=False)
        return df

def validate_uploaded_csv(uploaded_file) -> tuple[bool, str, pd.DataFrame]:
    """
    Validates user-uploaded CSV against schema requirements.
    Returns (is_valid, message, dataframe).
    """
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return False, f"Could not parse CSV file. Error: {str(e)}", pd.DataFrame()

    if df.empty:
        return False, "The uploaded CSV file is empty.", df

    # Check for missing required columns
    missing_cols = [col for col in REQUIRED_NUMERICAL_COLS if col not in df.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}. Please check the template format.", df

    # Sanitize and impute missing values
    df_clean = df.copy()
    
    # Fill student_id and name if absent
    if "student_id" not in df_clean.columns:
        df_clean["student_id"] = [f"NEW-{1000 + i}" for i in range(len(df_clean))]
    if "name" not in df_clean.columns:
        df_clean["name"] = [f"Student {i+1}" for i in range(len(df_clean))]
    if "gender" not in df_clean.columns:
        df_clean["gender"] = "Unspecified"
    if "grade_level" not in df_clean.columns:
        df_clean["grade_level"] = "General"
    if "parent_education_level" not in df_clean.columns:
        df_clean["parent_education_level"] = "Bachelor's"
    if "internet_access" not in df_clean.columns:
        df_clean["internet_access"] = "Yes"
    if "extracurricular_activities" not in df_clean.columns:
        df_clean["extracurricular_activities"] = "No"

    # Clean numerical columns
    for col in REQUIRED_NUMERICAL_COLS:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
        median_val = df_clean[col].median()
        if pd.isna(median_val):
            median_val = 50.0
        df_clean[col] = df_clean[col].fillna(median_val)

    # Compute subjects needing improvement if absent
    if "subjects_needing_improvement" not in df_clean.columns:
        subject_cols = ["math_score", "science_score", "english_score", "computer_science_score"]
        weak_count = (df_clean[subject_cols] < 60.0).sum(axis=1)
        df_clean["subjects_needing_improvement"] = weak_count

    return True, f"Successfully validated and processed {len(df_clean)} records.", df_clean

def create_template_csv():
    """Generates a downloadable template CSV for users."""
    if not os.path.exists(TEMPLATE_DATA_PATH):
        sample_rows = pd.DataFrame({
            "student_id": ["STU-9001", "STU-9002", "STU-9003"],
            "name": ["Aarav Patel", "Maya Lin", "Jordan Smith"],
            "gender": ["Male", "Female", "Male"],
            "grade_level": ["Grade 11", "Grade 12", "Undergrad Year 1"],
            "study_hours_per_day": [4.5, 6.2, 2.0],
            "attendance_rate": [88.5, 95.0, 62.0],
            "previous_exam_score": [72.0, 89.0, 51.0],
            "assignment_completion_rate": [80.0, 96.0, 48.0],
            "parent_education_level": ["Bachelor's", "Master's", "High School"],
            "internet_access": ["Yes", "Yes", "Yes"],
            "extracurricular_activities": ["Yes", "No", "No"],
            "sleep_hours": [7.0, 8.0, 5.5],
            "math_score": [74.0, 92.0, 48.0],
            "science_score": [70.0, 88.0, 54.0],
            "english_score": [78.0, 90.0, 58.0],
            "computer_science_score": [82.0, 95.0, 50.0],
            "subjects_needing_improvement": [0, 0, 4]
        })
        sample_rows.to_csv(TEMPLATE_DATA_PATH, index=False)
    return TEMPLATE_DATA_PATH

# Initialize template file on import
create_template_csv()

