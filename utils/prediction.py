import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/model.pkl")


def predict_score(student_data):
    """
    Predict exam score for a single student.
    student_data -> dictionary
    """

    df = pd.DataFrame([student_data])

    prediction = model.predict(df)[0]

    return round(prediction, 2)


def calculate_grade(score):
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def get_suggestions(score):
    suggestions = []

    if score >= 85:
        suggestions.append("🌟 Excellent performance! Keep it up.")
    elif score >= 70:
        suggestions.append("👍 Good performance. Focus on consistency.")
    elif score >= 60:
        suggestions.append("📚 Increase study hours and revise regularly.")
    else:
        suggestions.append("⚠️ Attend tutoring sessions and improve attendance.")

    return suggestions



def performance_analysis(score):

    if score >= 85:
        return """
Excellent academic performance.

The student demonstrates strong learning ability, consistent study habits, and a high probability of achieving excellent results.
"""

    elif score >= 70:
        return """
Good academic performance.

The student is performing well but can improve further by increasing study hours and maintaining attendance.
"""

    elif score >= 60:
        return """
Average performance.

The student should focus on regular revision, completing assignments, and improving classroom participation.
"""

    else:
        return """
Performance needs improvement.

The student should increase study hours, attend tutoring sessions, and maintain better attendance.
"""