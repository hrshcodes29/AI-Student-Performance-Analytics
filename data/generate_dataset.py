"""
Dataset Generator for AI Student Performance Analytics
Generates a realistic, statistically coherent student performance dataset (1,000 records).
Fully reproducible using fixed NumPy/Random seeds.
"""

import numpy as np
import pandas as pd
import os

def generate_student_dataset(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    np.random.seed(random_state)
    
    first_names_male = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna",
        "Ishaan", "Shaurya", "Atharv", "Harsh", "Rohan", "Kabir", "Aryan", "Dev", "Dhruv",
        "Alexander", "Marcus", "Lucas", "Noah", "Liam", "Ethan", "Oliver", "Leo", "Sebastian"
    ]
    first_names_female = [
        "Aanya", "Diya", "Saanvi", "Ananya", "Aadhya", "Pari", "Chiara", "Rhea", "Isha",
        "Avani", "Meera", "Myra", "Sneha", "Pooja", "Tanya", "Priya", "Nisha", "Kavya",
        "Emma", "Sophia", "Olivia", "Ava", "Mia", "Isabella", "Amelia", "Harper", "Evelyn"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Singh", "Chandel", "Gupta", "Malhotra", "Kapoor", "Joshi",
        "Rao", "Nair", "Iyer", "Reddy", "Mehta", "Bhatia", "Saxena", "Choudhury", "Das",
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Taylor"
    ]

    student_ids = [f"STU-{1000 + i}" for i in range(1, n_samples + 1)]
    genders = np.random.choice(["Male", "Female"], size=n_samples, p=[0.50, 0.50])
    
    names = []
    for g in genders:
        if g == "Male":
            fname = np.random.choice(first_names_male)
        else:
            fname = np.random.choice(first_names_female)
        lname = np.random.choice(last_names)
        names.append(f"{fname} {lname}")

    grades = np.random.choice(
        ["Grade 10", "Grade 11", "Grade 12", "Undergrad Year 1", "Undergrad Year 2"],
        size=n_samples,
        p=[0.20, 0.22, 0.22, 0.18, 0.18]
    )

    parent_edu = np.random.choice(
        ["High School", "Associate", "Bachelor's", "Master's", "Doctorate"],
        size=n_samples,
        p=[0.22, 0.18, 0.38, 0.16, 0.06]
    )
    edu_weights = {
        "High School": -2.0,
        "Associate": 0.0,
        "Bachelor's": 2.5,
        "Master's": 4.0,
        "Doctorate": 5.5
    }

    internet = np.random.choice(["Yes", "No"], size=n_samples, p=[0.88, 0.12])
    extracurricular = np.random.choice(["Yes", "No"], size=n_samples, p=[0.58, 0.42])
    
    # Study hours: normal dist centered at 4.2 hours, clipped to 1.0 - 9.5
    study_hours = np.clip(np.random.normal(loc=4.5, scale=1.8, size=n_samples), 1.0, 9.5).round(1)
    
    # Attendance: beta distribution skewed towards 80-95%
    attendance_raw = np.random.beta(a=7, b=2, size=n_samples) * 100
    attendance = np.clip(attendance_raw, 45.0, 99.5).round(1)
    
    # Sleep hours: centered at 7.0
    sleep_hours = np.clip(np.random.normal(loc=7.0, scale=1.1, size=n_samples), 4.5, 9.5).round(1)
    
    # Assignment completion rate correlated with study hours and attendance
    assignment_rate = np.clip(
        0.35 * attendance + 5.0 * study_hours + np.random.normal(30, 8, size=n_samples),
        35.0,
        100.0
    ).round(1)
    
    # Previous exam score correlated with study hours & attendance
    prev_exam = np.clip(
        0.45 * attendance + 3.8 * study_hours + np.random.normal(25, 9, size=n_samples),
        35.0,
        98.0
    ).round(1)

    # Subject scores
    math_score = np.clip(
        0.35 * prev_exam + 3.0 * study_hours + 0.2 * assignment_rate + np.random.normal(5, 8, size=n_samples),
        30.0, 100.0
    ).round(1)
    
    science_score = np.clip(
        0.36 * prev_exam + 2.8 * study_hours + 0.2 * assignment_rate + np.random.normal(6, 8, size=n_samples),
        30.0, 100.0
    ).round(1)

    english_score = np.clip(
        0.30 * prev_exam + 2.2 * study_hours + 0.25 * assignment_rate + np.random.normal(12, 7, size=n_samples),
        32.0, 100.0
    ).round(1)

    cs_score = np.clip(
        0.34 * prev_exam + 3.2 * study_hours + 0.2 * assignment_rate + np.random.normal(7, 8, size=n_samples),
        30.0, 100.0
    ).round(1)

    # Count subjects with score < 60
    subjects_matrix = np.column_stack([math_score, science_score, english_score, cs_score])
    subjects_needing_improvement = (subjects_matrix < 60.0).sum(axis=1)

    # Calculate final score based on a realistic weighted composite + noise
    parent_boost = np.array([edu_weights[e] for e in parent_edu])
    internet_boost = np.where(internet == "Yes", 2.0, -3.0)
    
    final_score = (
        0.30 * prev_exam +
        0.25 * attendance +
        0.18 * assignment_rate +
        2.2 * study_hours +
        0.05 * (math_score + science_score + english_score + cs_score) / 4 +
        parent_boost * 0.4 +
        internet_boost * 0.3 +
        np.random.normal(0, 3.2, size=n_samples)
    )
    final_score = np.clip(final_score, 32.0, 99.2).round(1)

    # Risk level classification logic
    risk_level = []
    academic_status = []
    for score, att, weak_sub in zip(final_score, attendance, subjects_needing_improvement):
        if score < 58.0 or att < 65.0 or weak_sub >= 3:
            risk_level.append("High Risk")
        elif score < 72.0 or att < 75.0 or weak_sub >= 2:
            risk_level.append("Moderate Risk")
        else:
            risk_level.append("Low Risk")
            
        if score >= 85.0:
            academic_status.append("Distinction")
        elif score >= 70.0:
            academic_status.append("First Class")
        elif score >= 55.0:
            academic_status.append("Second Class")
        else:
            academic_status.append("Needs Academic Support")

    df = pd.DataFrame({
        "student_id": student_ids,
        "name": names,
        "gender": genders,
        "grade_level": grades,
        "study_hours_per_day": study_hours,
        "attendance_rate": attendance,
        "previous_exam_score": prev_exam,
        "assignment_completion_rate": assignment_rate,
        "parent_education_level": parent_edu,
        "internet_access": internet,
        "extracurricular_activities": extracurricular,
        "sleep_hours": sleep_hours,
        "math_score": math_score,
        "science_score": science_score,
        "english_score": english_score,
        "computer_science_score": cs_score,
        "subjects_needing_improvement": subjects_needing_improvement,
        "final_score": final_score,
        "risk_level": risk_level,
        "academic_status": academic_status
    })

    return df

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "student_performance_data.csv")
    df = generate_student_dataset(n_samples=1000, random_state=42)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} student records at: {output_path}")
    print("\nDataset Overview:")
    print(df.info())
    print("\nRisk Level Distribution:")
    print(df["risk_level"].value_counts(normalize=True))
    print("\nSample Rows:")
    print(df.head(3))

