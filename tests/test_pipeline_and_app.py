"""
Comprehensive Test Suite for AI Student Performance Analytics
Tests dataset integrity, ML pipeline, inference, recommendations, and view modules.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from data.generate_dataset import generate_student_dataset
from src.data_loader import load_default_data, validate_uploaded_csv
from src.ml_pipeline import (
    train_and_evaluate,
    predict_single_student,
    ALL_FEATURE_COLUMNS,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES
)
from src.recommender import generate_academic_recommendations
from src.views import (
    page_executive_dashboard,
    page_prediction,
    page_student_explorer,
    page_at_risk,
    page_academic_insights,
    page_recommendations,
    page_model_lab,
    page_dataset_mgmt,
    page_responsible_ai
)

def test_dataset_generation():
    df = generate_student_dataset(n_samples=200, random_state=42)
    assert len(df) == 200
    assert "student_id" in df.columns
    assert "final_score" in df.columns
    assert "risk_level" in df.columns
    assert set(df["risk_level"].unique()).issubset({"Low Risk", "Moderate Risk", "High Risk"})
    assert (df["final_score"] >= 0).all() and (df["final_score"] <= 100).all()
    assert (df["attendance_rate"] >= 0).all() and (df["attendance_rate"] <= 100).all()

def test_data_loader():
    df = load_default_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 1000
    for col in ALL_FEATURE_COLUMNS:
        assert col in df.columns, f"Missing feature column: {col}"

def test_ml_pipeline_and_metrics():
    # Verify trained artifacts
    models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    assert os.path.exists(os.path.join(models_dir, "best_score_regressor.joblib"))
    assert os.path.exists(os.path.join(models_dir, "best_risk_classifier.joblib"))
    assert os.path.exists(os.path.join(models_dir, "preprocessor.joblib"))
    assert os.path.exists(os.path.join(models_dir, "model_metrics.json"))

def test_live_inference():
    sample_student = {
        "study_hours_per_day": 5.0,
        "attendance_rate": 85.0,
        "previous_exam_score": 75.0,
        "assignment_completion_rate": 80.0,
        "sleep_hours": 7.0,
        "math_score": 78.0,
        "science_score": 74.0,
        "english_score": 82.0,
        "computer_science_score": 80.0,
        "subjects_needing_improvement": 0,
        "gender": "Female",
        "grade_level": "Grade 11",
        "parent_education_level": "Bachelor's",
        "internet_access": "Yes",
        "extracurricular_activities": "Yes"
    }
    result = predict_single_student(sample_student)
    assert "predicted_score" in result
    assert 0.0 <= result["predicted_score"] <= 100.0
    assert result["predicted_risk"] in ["Low Risk", "Moderate Risk", "High Risk"]
    assert len(result["feature_contributions"]) > 0

def test_recommender():
    sample_student = {
        "student_id": "TEST-101",
        "name": "Test Student",
        "study_hours_per_day": 2.0,
        "attendance_rate": 60.0,
        "previous_exam_score": 50.0,
        "assignment_completion_rate": 55.0,
        "sleep_hours": 5.0,
        "math_score": 45.0,
        "science_score": 52.0,
        "english_score": 60.0,
        "computer_science_score": 50.0,
        "risk_level": "High Risk"
    }
    recs = generate_academic_recommendations(sample_student, predicted_score=52.0, predicted_risk="High Risk")
    assert recs["total_recommendations"] >= 3
    assert recs["estimated_gain"] > 0
    priorities = [r["priority"] for r in recs["recommendations"]]
    assert "High Priority" in priorities

def test_view_modules_imported():
    views = [
        page_executive_dashboard,
        page_prediction,
        page_student_explorer,
        page_at_risk,
        page_academic_insights,
        page_recommendations,
        page_model_lab,
        page_dataset_mgmt,
        page_responsible_ai
    ]
    for v in views:
        assert hasattr(v, "render"), f"View {v.__name__} must define a render() function"

if __name__ == "__main__":
    print("Running tests manually...")
    test_dataset_generation()
    print("✅ test_dataset_generation passed")
    test_data_loader()
    print("✅ test_data_loader passed")
    test_ml_pipeline_and_metrics()
    print("✅ test_ml_pipeline_and_metrics passed")
    test_live_inference()
    print("✅ test_live_inference passed")
    test_recommender()
    print("✅ test_recommender passed")
    test_view_modules_imported()
    print("✅ test_view_modules_imported passed")
    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY!")

