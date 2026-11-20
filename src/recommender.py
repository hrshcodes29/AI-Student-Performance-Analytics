"""
AI Recommendation Engine for Student Academic Support
Generates personalized, data-backed academic action plans based on actual student metrics.
"""

from typing import Dict, List, Any

def generate_academic_recommendations(student: Dict[str, Any], predicted_score: float = None, predicted_risk: str = None) -> Dict[str, Any]:
    """
    Analyzes student metrics and generates a prioritized, multi-tiered action plan.
    """
    attendance = float(student.get("attendance_rate", 75.0))
    study_hours = float(student.get("study_hours_per_day", 4.0))
    prev_exam = float(student.get("previous_exam_score", 65.0))
    assignment_rate = float(student.get("assignment_completion_rate", 75.0))
    sleep = float(student.get("sleep_hours", 7.0))
    
    math = float(student.get("math_score", 65.0))
    sci = float(student.get("science_score", 65.0))
    eng = float(student.get("english_score", 65.0))
    cs = float(student.get("computer_science_score", 65.0))
    
    recommendations = []
    potential_score_gain = 0.0
    
    # 1. Attendance Intervention
    if attendance < 65.0:
        recommendations.append({
            "category": "Attendance & Engagement",
            "priority": "High Priority",
            "badge_color": "#EF4444",
            "icon": "🚨",
            "title": "Critical Attendance Recovery Program",
            "observation": f"Current attendance is at a critical level ({attendance}%). Missing lectures directly impacts conceptual continuity.",
            "action_items": [
                "Schedule a 1-on-1 academic counseling session with the faculty mentor within 48 hours.",
                "Target 100% attendance across the next 3 weeks to lift overall attendance above the 75% institutional requirement.",
                "Utilize recorded lectures and obtain lecture notes for all missed topics."
            ],
            "estimated_impact": "+6 to +10 Score Improvement"
        })
        potential_score_gain += 8.0
    elif attendance < 78.0:
        recommendations.append({
            "category": "Attendance & Engagement",
            "priority": "Medium Priority",
            "badge_color": "#F59E0B",
            "icon": "⚠️",
            "title": "Attendance Reinforcement",
            "observation": f"Attendance is currently {attendance}%, borderline below the recommended 80% benchmark.",
            "action_items": [
                "Commit to maintaining consistent attendance in morning and lab sessions.",
                "Track weekly attendance through the student portal to prevent dropping into the at-risk zone."
            ],
            "estimated_impact": "+3 to +5 Score Improvement"
        })
        potential_score_gain += 4.0

    # 2. Study Routine & Time Management
    if study_hours < 3.0:
        recommendations.append({
            "category": "Study Routine",
            "priority": "High Priority",
            "badge_color": "#EF4444",
            "icon": "⏱️",
            "title": "Daily Focused Study Expansion",
            "observation": f"Current self-study ({study_hours} hrs/day) is insufficient for complex curriculum mastery.",
            "action_items": [
                f"Gradually increase focused study time from {study_hours}h to at least 4.5h daily.",
                "Adopt the Pomodoro Technique: 50 minutes of deep study followed by 10-minute active recall breaks.",
                "Eliminate digital distractions and establish a fixed, quiet study block each evening."
            ],
            "estimated_impact": "+5 to +8 Score Improvement"
        })
        potential_score_gain += 6.5
    elif study_hours < 4.5:
        recommendations.append({
            "category": "Study Routine",
            "priority": "Medium Priority",
            "badge_color": "#F59E0B",
            "icon": "📚",
            "title": "Study Optimization & Retention",
            "observation": f"Study hours are moderate ({study_hours} hrs/day) but can be optimized with active recall techniques.",
            "action_items": [
                "Incorporate spaced repetition flashcards for core formulas and definitions.",
                "Dedicate 1 hour every Sunday for weekly synthesis and concept mapping."
            ],
            "estimated_impact": "+2 to +4 Score Improvement"
        })
        potential_score_gain += 3.0

    # 3. Subject-Specific Remediation
    weak_subjects = []
    if math < 60.0:
        weak_subjects.append(f"Mathematics ({math}/100)")
    if sci < 60.0:
        weak_subjects.append(f"Science ({sci}/100)")
    if cs < 60.0:
        weak_subjects.append(f"Computer Science ({cs}/100)")
    if eng < 60.0:
        weak_subjects.append(f"English Language ({eng}/100)")
        
    if weak_subjects:
        recommendations.append({
            "category": "Subject Remediation",
            "priority": "High Priority",
            "badge_color": "#EF4444",
            "icon": "🎯",
            "title": f"Targeted Remediation for Weaker Subjects",
            "observation": f"Identified below-threshold performance in: {', '.join(weak_subjects)}.",
            "action_items": [
                f"Enroll in peer tutoring or department office hours for: {', '.join(weak_subjects)}.",
                "Solve 5 practice problems or past exam questions every alternate day for each weak subject.",
                "Complete a self-diagnostic mock quiz at the end of each topic module."
            ],
            "estimated_impact": "+5 to +9 Score Improvement"
        })
        potential_score_gain += 7.0

    # 4. Assignment Completion
    if assignment_rate < 70.0:
        recommendations.append({
            "category": "Continuous Assessment",
            "priority": "High Priority",
            "badge_color": "#EF4444",
            "icon": "📝",
            "title": "Assignment Catch-Up & Submission Discipline",
            "observation": f"Assignment submission rate is low at {assignment_rate}%. Continuous internal marks depend heavily on this.",
            "action_items": [
                "Audit all pending assignments with respective subject instructors immediately.",
                "Submit draft submissions 48 hours before deadlines to allow revision and feedback.",
                "Set calendar alerts 3 days in advance of all continuous evaluation deliverables."
            ],
            "estimated_impact": "+4 to +7 Score Improvement"
        })
        potential_score_gain += 5.5
    elif assignment_rate < 85.0:
        recommendations.append({
            "category": "Continuous Assessment",
            "priority": "Medium Priority",
            "badge_color": "#F59E0B",
            "icon": "📋",
            "title": "Assignment Quality & Timeliness",
            "observation": f"Assignment rate is {assignment_rate}%. Target 95%+ to guarantee full continuous evaluation credits.",
            "action_items": [
                "Review rubric requirements before submitting coursework.",
                "Form a 2-person accountability study partnership for project milestones."
            ],
            "estimated_impact": "+2 to +3 Score Improvement"
        })
        potential_score_gain += 2.5

    # 5. Wellness & Cognitive Balance
    if sleep < 6.0:
        recommendations.append({
            "category": "Wellness & Cognitive Readiness",
            "priority": "Low Priority",
            "badge_color": "#3B82F6",
            "icon": "💤",
            "title": "Sleep Hygiene & Cognitive Restoration",
            "observation": f"Student averages only {sleep} hours of sleep. Chronic sleep deprivation reduces exam memory retention by ~20%.",
            "action_items": [
                "Target a minimum of 7 to 8 hours of sleep, particularly during examination weeks.",
                "Avoid late-night screen time 45 minutes prior to sleep."
            ],
            "estimated_impact": "+2 to +4 Score Improvement"
        })
        potential_score_gain += 2.0

    # If student is already performing exceptionally well
    if not recommendations:
        recommendations.append({
            "category": "Advanced Enrichment",
            "priority": "Maintenance",
            "badge_color": "#10B981",
            "icon": "🌟",
            "title": "Honors Track & Peer Mentorship",
            "observation": "Student maintains exemplary attendance, study hours, and academic scores across all metrics.",
            "action_items": [
                "Explore undergraduate research projects or competitive hackathons.",
                "Participate as an academic peer mentor in the student learning center.",
                "Engage in advanced certification electives (e.g., Cloud & AI Fundamentals)."
            ],
            "estimated_impact": "Maintains 90%+ Distinction Range"
        })
        potential_score_gain = 2.0

    bounded_gain = min(round(potential_score_gain, 1), 22.0)
    current_or_pred = predicted_score if predicted_score is not None else prev_exam
    target_potential_score = min(round(current_or_pred + bounded_gain, 1), 99.0)

    return {
        "student_id": student.get("student_id", "Custom Profile"),
        "student_name": student.get("name", "Student"),
        "current_score": current_or_pred,
        "predicted_risk": predicted_risk or student.get("risk_level", "Moderate Risk"),
        "estimated_gain": bounded_gain,
        "target_potential_score": target_potential_score,
        "total_recommendations": len(recommendations),
        "recommendations": recommendations
    }

