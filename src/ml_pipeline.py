"""
Machine Learning Pipeline for AI Student Performance Analytics
Trains, evaluates, and persists regression & classification models.
Supports live prediction, feature importance calculation, and model explanation.
"""

import os
import json
import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Feature definitions
NUMERICAL_FEATURES = [
    "study_hours_per_day",
    "attendance_rate",
    "previous_exam_score",
    "assignment_completion_rate",
    "sleep_hours",
    "subjects_needing_improvement",
    "math_score",
    "science_score",
    "english_score",
    "computer_science_score"
]

CATEGORICAL_FEATURES = [
    "gender",
    "grade_level",
    "parent_education_level",
    "internet_access",
    "extracurricular_activities"
]

ALL_FEATURE_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
REGRESSION_TARGET = "final_score"
CLASSIFICATION_TARGET = "risk_level"

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "student_performance_data.csv")

def get_preprocessor():
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer([
        ("num", num_pipeline, NUMERICAL_FEATURES),
        ("cat", cat_pipeline, CATEGORICAL_FEATURES)
    ])
    return preprocessor

def train_and_evaluate(data_path: str = DATA_PATH, output_dir: str = MODELS_DIR) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(data_path)
    
    X = df[ALL_FEATURE_COLUMNS].copy()
    y_reg = df[REGRESSION_TARGET].copy()
    y_clf = df[CLASSIFICATION_TARGET].copy()
    
    # 80/20 train-test split (stratified on risk_level for balanced representation)
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X, y_reg, y_clf, test_size=0.20, random_state=42, stratify=y_clf
    )
    
    # Fit preprocessor
    preprocessor = get_preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    # Get feature names from preprocessor
    cat_names = preprocessor.named_transformers_["cat"].named_steps["encoder"].get_feature_names_out(CATEGORICAL_FEATURES)
    all_proc_feature_names = NUMERICAL_FEATURES + list(cat_names)
    
    # ----------------------------------------------------
    # 1. Regression Models (Final Score Prediction)
    # ----------------------------------------------------
    reg_candidates = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Decision Tree Regressor": DecisionTreeRegressor(max_depth=6, random_state=42),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    }
    
    reg_metrics = {}
    best_reg_name = None
    best_reg_r2 = -float("inf")
    trained_reg_models = {}
    
    for name, model in reg_candidates.items():
        model.fit(X_train_proc, y_reg_train)
        preds = model.predict(X_test_proc)
        
        mae = float(mean_absolute_error(y_reg_test, preds))
        mse = float(mean_squared_error(y_reg_test, preds))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_reg_test, preds))
        
        reg_metrics[name] = {
            "MAE": round(mae, 3),
            "MSE": round(mse, 3),
            "RMSE": round(rmse, 3),
            "R2": round(r2, 4)
        }
        trained_reg_models[name] = model
        
        if r2 > best_reg_r2:
            best_reg_r2 = r2
            best_reg_name = name
            
    best_regressor = trained_reg_models[best_reg_name]

    # ----------------------------------------------------
    # 2. Classification Models (Risk Level Prediction)
    # ----------------------------------------------------
    clf_candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree Classifier": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, max_depth=7, random_state=42)
    }
    
    clf_metrics = {}
    best_clf_name = None
    best_clf_f1 = -float("inf")
    trained_clf_models = {}
    
    class_labels = ["Low Risk", "Moderate Risk", "High Risk"]
    
    for name, model in clf_candidates.items():
        model.fit(X_train_proc, y_clf_train)
        preds = model.predict(X_test_proc)
        
        acc = float(accuracy_score(y_clf_test, preds))
        prec = float(precision_score(y_clf_test, preds, average="weighted", zero_division=0))
        rec = float(recall_score(y_clf_test, preds, average="weighted", zero_division=0))
        f1 = float(f1_score(y_clf_test, preds, average="weighted", zero_division=0))
        
        clf_metrics[name] = {
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4)
        }
        trained_clf_models[name] = model
        
        if f1 > best_clf_f1:
            best_clf_f1 = f1
            best_clf_name = name
            
    best_classifier = trained_clf_models[best_clf_name]
    
    # Compute test confusion matrix for best classifier
    best_clf_preds = best_classifier.predict(X_test_proc)
    cm = confusion_matrix(y_clf_test, best_clf_preds, labels=class_labels)
    cm_list = cm.tolist()
    
    # Feature Importance from Random Forest Regressor & Classifier
    rf_reg = trained_reg_models["Random Forest Regressor"]
    rf_reg_importances = rf_reg.feature_importances_
    
    # Aggregate importance back to original features
    feature_importance_dict = {}
    for idx, feature in enumerate(NUMERICAL_FEATURES):
        feature_importance_dict[feature] = float(rf_reg_importances[idx])
        
    # Group one-hot encoded categories
    cat_offset = len(NUMERICAL_FEATURES)
    cat_transformed_names = list(cat_names)
    for cat_feat in CATEGORICAL_FEATURES:
        cat_indices = [
            cat_offset + i for i, col in enumerate(cat_transformed_names)
            if col.startswith(cat_feat)
        ]
        feature_importance_dict[cat_feat] = float(sum(rf_reg_importances[i] for i in cat_indices))
        
    # Normalize importances so sum = 100%
    total_imp = sum(feature_importance_dict.values())
    if total_imp > 0:
        feature_importance_dict = {
            k: round((v / total_imp) * 100, 2)
            for k, v in sorted(feature_importance_dict.items(), key=lambda item: item[1], reverse=True)
        }
        
    # Test predictions sample for scatter plot in model lab
    sample_size = min(150, len(y_reg_test))
    test_sample_actual = [float(x) for x in y_reg_test.iloc[:sample_size].values]
    test_sample_predicted = [float(round(x, 2)) for x in best_regressor.predict(X_test_proc[:sample_size])]
    test_sample_risk_actual = [str(x) for x in y_clf_test.iloc[:sample_size].values]
    test_sample_risk_pred = [str(x) for x in best_classifier.predict(X_test_proc[:sample_size])]
    
    # Save artifacts
    joblib.dump(preprocessor, os.path.join(output_dir, "preprocessor.joblib"))
    joblib.dump(best_regressor, os.path.join(output_dir, "best_score_regressor.joblib"))
    joblib.dump(best_classifier, os.path.join(output_dir, "best_risk_classifier.joblib"))
    
    metadata = {
        "dataset_records": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "features_count": len(ALL_FEATURE_COLUMNS),
        "numerical_features": NUMERICAL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "best_regressor_name": best_reg_name,
        "best_regressor_metrics": reg_metrics[best_reg_name],
        "regression_comparison": reg_metrics,
        "best_classifier_name": best_clf_name,
        "best_classifier_metrics": clf_metrics[best_clf_name],
        "classification_comparison": clf_metrics,
        "class_labels": class_labels,
        "confusion_matrix": cm_list,
        "feature_importance": feature_importance_dict,
        "test_sample_predictions": {
            "actual_scores": test_sample_actual,
            "predicted_scores": test_sample_predicted,
            "actual_risks": test_sample_risk_actual,
            "predicted_risks": test_sample_risk_pred
        }
    }
    
    with open(os.path.join(output_dir, "model_metrics.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Model training and evaluation successfully completed!")
    print(f"Best Regressor: {best_reg_name} (R2={reg_metrics[best_reg_name]['R2']}, MAE={reg_metrics[best_reg_name]['MAE']})")
    print(f"Best Classifier: {best_clf_name} (Accuracy={clf_metrics[best_clf_name]['Accuracy']}, F1={clf_metrics[best_clf_name]['F1-Score']})")
    
    return metadata

def load_artifacts(models_dir: str = MODELS_DIR):
    preprocessor = joblib.load(os.path.join(models_dir, "preprocessor.joblib"))
    regressor = joblib.load(os.path.join(models_dir, "best_score_regressor.joblib"))
    classifier = joblib.load(os.path.join(models_dir, "best_risk_classifier.joblib"))
    with open(os.path.join(models_dir, "model_metrics.json"), "r") as f:
        metrics = json.load(f)
    return preprocessor, regressor, classifier, metrics

def predict_single_student(student_dict: dict, models_dir: str = MODELS_DIR):
    preprocessor, regressor, classifier, metrics = load_artifacts(models_dir)
    df_input = pd.DataFrame([student_dict])
    
    # Fill missing columns if any
    for col in ALL_FEATURE_COLUMNS:
        if col not in df_input.columns:
            if col in NUMERICAL_FEATURES:
                df_input[col] = 50.0
            else:
                df_input[col] = "None"
                
    X_proc = preprocessor.transform(df_input[ALL_FEATURE_COLUMNS])
    
    pred_score = float(np.clip(regressor.predict(X_proc)[0], 0.0, 100.0).round(1))
    pred_risk = str(classifier.predict(X_proc)[0])
    
    # Class probabilities if available
    risk_probs = {}
    if hasattr(classifier, "predict_proba"):
        probs = classifier.predict_proba(X_proc)[0]
        classes = classifier.classes_
        for cls_name, p in zip(classes, probs):
            risk_probs[cls_name] = round(float(p) * 100, 1)
            
    # Calculate feature influence for this student relative to dataset average
    # Baseline comparison
    feature_contributions = []
    mean_benchmarks = {
        "attendance_rate": 80.0,
        "study_hours_per_day": 4.5,
        "previous_exam_score": 65.0,
        "assignment_completion_rate": 75.0,
        "subjects_needing_improvement": 1.0,
        "math_score": 65.0,
        "science_score": 65.0,
        "english_score": 65.0,
        "computer_science_score": 65.0
    }
    
    weights = {
        "previous_exam_score": 0.30,
        "attendance_rate": 0.25,
        "study_hours_per_day": 2.2,
        "assignment_completion_rate": 0.18,
        "subjects_needing_improvement": -3.5,
        "math_score": 0.05,
        "science_score": 0.05,
        "english_score": 0.05,
        "computer_science_score": 0.05
    }
    
    for feat, mean_val in mean_benchmarks.items():
        if feat in student_dict:
            val = float(student_dict[feat])
            diff = val - mean_val
            impact = diff * weights.get(feat, 0.1)
            feature_contributions.append({
                "feature": feat.replace("_", " ").title(),
                "student_value": val,
                "benchmark": mean_val,
                "impact_score": round(impact, 2),
                "direction": "Positive Impact" if impact >= 0 else "Needs Improvement"
            })
            
    # Sort by absolute impact
    feature_contributions.sort(key=lambda x: abs(x["impact_score"]), reverse=True)
    
    return {
        "predicted_score": pred_score,
        "predicted_risk": pred_risk,
        "risk_probabilities": risk_probs,
        "feature_contributions": feature_contributions
    }

if __name__ == "__main__":
    metrics = train_and_evaluate()

