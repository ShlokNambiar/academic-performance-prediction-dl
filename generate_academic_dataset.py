"""
Synthetic Dataset Generator for Academic Performance Prediction
Creates a comprehensive dataset with realistic correlations and patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_student_demographics(n_students):
    """Generate student demographic information"""

    genders = ['Male', 'Female', 'Non-binary']
    age_groups = list(range(16, 26))

    # Socioeconomic status affects performance
    socioeconomic_status = ['Low', 'Medium', 'High']

    # Parent education level influences student performance
    parent_education = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD', 'None']

    # Distance from home affects attendance
    commute_distance = ['<5km', '5-10km', '10-20km', '>20km']

    demographics = {
        'student_id': [f'STU{str(i).zfill(5)}' for i in range(1, n_students + 1)],
        'age': np.random.choice(age_groups, n_students),
        'gender': np.random.choice(genders, n_students, p=[0.48, 0.48, 0.04]),
        'socioeconomic_status': np.random.choice(socioeconomic_status, n_students, p=[0.25, 0.50, 0.25]),
        'parent_education': np.random.choice(parent_education, n_students, p=[0.20, 0.15, 0.30, 0.20, 0.10, 0.05]),
        'commute_distance': np.random.choice(commute_distance, n_students, p=[0.40, 0.30, 0.20, 0.10]),
        'has_internet_at_home': np.random.choice([0, 1], n_students, p=[0.15, 0.85]),
        'has_study_space': np.random.choice([0, 1], n_students, p=[0.20, 0.80]),
        'family_support': np.random.choice(['Low', 'Medium', 'High'], n_students, p=[0.20, 0.50, 0.30])
    }

    return pd.DataFrame(demographics)

def generate_academic_history(df):
    """Generate previous academic performance data"""

    n_students = len(df)

    # Previous semester grades (correlated with socioeconomic status and parent education)
    base_gpa = np.random.normal(2.8, 0.6, n_students)

    # Adjust based on socioeconomic status
    ses_adjustment = df['socioeconomic_status'].map({'Low': -0.3, 'Medium': 0, 'High': 0.4})

    # Adjust based on parent education
    parent_edu_adjustment = df['parent_education'].map({
        'None': -0.4, 'High School': -0.2, 'Associate': 0,
        'Bachelor': 0.2, 'Master': 0.3, 'PhD': 0.4
    })

    # Adjust based on resources
    resource_adjustment = (df['has_internet_at_home'] * 0.2 + df['has_study_space'] * 0.15)

    previous_gpa = base_gpa + ses_adjustment + parent_edu_adjustment + resource_adjustment
    previous_gpa = np.clip(previous_gpa, 0.0, 4.0)

    df['previous_semester_gpa'] = np.round(previous_gpa, 2)
    df['previous_year_gpa'] = np.round(np.clip(previous_gpa + np.random.normal(0, 0.2, n_students), 0.0, 4.0), 2)
    df['cumulative_gpa'] = np.round((df['previous_semester_gpa'] + df['previous_year_gpa']) / 2, 2)

    # Number of courses failed in previous semesters
    fail_probability = 1 - (df['cumulative_gpa'] / 4.0)
    df['courses_failed_previous'] = np.random.binomial(3, fail_probability)

    return df

def generate_current_semester_data(df):
    """Generate current semester enrollment and course data"""

    n_students = len(df)

    # Number of courses enrolled (full-time vs part-time)
    df['courses_enrolled'] = np.random.choice([3, 4, 5, 6], n_students, p=[0.10, 0.30, 0.40, 0.20])

    # Credit hours
    df['credit_hours'] = df['courses_enrolled'] * np.random.choice([3, 4], n_students, p=[0.7, 0.3])

    # Course difficulty (average)
    df['avg_course_difficulty'] = np.random.choice([1, 2, 3, 4, 5], n_students, p=[0.05, 0.20, 0.50, 0.20, 0.05])

    # Major field
    majors = ['STEM', 'Business', 'Arts', 'Social Sciences', 'Health Sciences']
    df['major'] = np.random.choice(majors, n_students, p=[0.30, 0.25, 0.15, 0.15, 0.15])

    # Year of study
    df['year_of_study'] = np.random.choice([1, 2, 3, 4], n_students, p=[0.30, 0.30, 0.25, 0.15])

    return df

def generate_attendance_data(df):
    """Generate attendance patterns"""

    n_students = len(df)

    # Base attendance rate
    base_attendance = np.random.beta(8, 2, n_students) * 100

    # Adjust based on commute distance
    commute_penalty = df['commute_distance'].map({'<5km': 0, '5-10km': -3, '10-20km': -7, '>20km': -12})

    # Adjust based on previous performance (better students attend more)
    performance_bonus = (df['cumulative_gpa'] / 4.0) * 10

    # Health issues affect attendance
    df['has_health_issues'] = np.random.choice([0, 1], n_students, p=[0.80, 0.20])
    health_penalty = df['has_health_issues'] * np.random.uniform(-15, -5, n_students)

    attendance_rate = base_attendance + commute_penalty + performance_bonus + health_penalty
    df['attendance_rate'] = np.clip(attendance_rate, 0, 100).round(1)

    # Late arrivals
    df['late_arrivals'] = np.random.poisson(lam=5 * (1 - df['attendance_rate']/100), size=n_students)

    # Absences
    total_classes = 60  # Assume 60 classes per semester
    df['total_absences'] = ((100 - df['attendance_rate']) / 100 * total_classes).astype(int)

    return df

def generate_lms_activity(df):
    """Generate Learning Management System activity data"""

    n_students = len(df)

    # LMS logins per week (correlated with performance)
    base_logins = np.random.poisson(lam=15, size=n_students)
    performance_factor = (df['cumulative_gpa'] / 4.0) * 10
    df['lms_logins_per_week'] = np.clip(base_logins + performance_factor, 0, 50).astype(int)

    # Time spent on LMS (hours per week)
    df['lms_hours_per_week'] = np.random.gamma(shape=2, scale=3, size=n_students) * (df['lms_logins_per_week'] / 15)
    df['lms_hours_per_week'] = np.clip(df['lms_hours_per_week'], 0, 40).round(1)

    # Assignment submissions
    total_assignments = 20
    submission_rate = df['cumulative_gpa'] / 4.0 + np.random.normal(0, 0.1, n_students)
    df['assignments_submitted'] = (submission_rate * total_assignments).clip(0, total_assignments).astype(int)
    df['assignments_on_time'] = (df['assignments_submitted'] * np.random.uniform(0.6, 1.0, n_students)).astype(int)
    df['assignments_late'] = df['assignments_submitted'] - df['assignments_on_time']

    # Forum participation
    df['forum_posts'] = np.random.poisson(lam=8, size=n_students) * (df['lms_hours_per_week'] / 10)
    df['forum_posts'] = df['forum_posts'].astype(int)

    # Resource downloads
    df['resources_downloaded'] = np.random.poisson(lam=25, size=n_students) * (df['lms_logins_per_week'] / 15)
    df['resources_downloaded'] = df['resources_downloaded'].astype(int)

    # Video lecture views
    total_videos = 40
    df['videos_watched'] = (np.random.beta(5, 2, n_students) * total_videos * (df['lms_hours_per_week'] / 20)).astype(int)
    df['videos_watched'] = np.clip(df['videos_watched'], 0, total_videos)

    return df

def generate_behavioral_data(df):
    """Generate behavioral and engagement indicators"""

    n_students = len(df)

    # Study hours per week
    base_study = np.random.gamma(shape=3, scale=4, size=n_students)
    df['study_hours_per_week'] = np.clip(base_study + (df['cumulative_gpa'] / 4.0) * 10, 0, 60).round(1)

    # Part-time work hours
    df['work_hours_per_week'] = np.random.choice([0, 10, 20, 30, 40], n_students, p=[0.30, 0.25, 0.25, 0.15, 0.05])

    # Extracurricular activities
    df['extracurricular_hours'] = np.random.choice([0, 2, 5, 10], n_students, p=[0.40, 0.30, 0.20, 0.10])

    # Library visits per week
    df['library_visits_per_week'] = np.random.poisson(lam=3, size=n_students) * (df['study_hours_per_week'] / 15)
    df['library_visits_per_week'] = df['library_visits_per_week'].astype(int)

    # Tutoring sessions attended
    df['tutoring_sessions_attended'] = np.random.poisson(lam=2, size=n_students)

    # Office hours attendance
    df['office_hours_visits'] = np.random.poisson(lam=3, size=n_students)

    # Peer study groups
    df['study_group_participation'] = np.random.choice([0, 1], n_students, p=[0.40, 0.60])

    # Mental health indicators
    stress_base = np.random.choice([1, 2, 3, 4, 5], n_students, p=[0.10, 0.20, 0.40, 0.20, 0.10])
    workload_stress = (df['credit_hours'] / 18) * 2
    df['stress_level'] = np.clip(stress_base + workload_stress, 1, 5).astype(int)

    # Motivation level
    df['motivation_level'] = np.random.choice([1, 2, 3, 4, 5], n_students, p=[0.10, 0.15, 0.40, 0.25, 0.10])

    # Sleep hours per night
    df['avg_sleep_hours'] = np.clip(np.random.normal(7, 1.5, n_students), 3, 10).round(1)

    return df

def generate_assessment_scores(df):
    """Generate midterm and quiz scores"""

    n_students = len(df)

    # Base performance from cumulative GPA
    base_score = (df['cumulative_gpa'] / 4.0) * 100

    # Adjust based on current semester factors
    attendance_factor = (df['attendance_rate'] - 70) / 30 * 10
    lms_factor = (df['lms_hours_per_week'] / 20) * 5
    study_factor = (df['study_hours_per_week'] / 30) * 10
    stress_penalty = (df['stress_level'] - 3) * -3
    sleep_factor = (df['avg_sleep_hours'] - 7) * 2

    # Midterm scores
    midterm_score = base_score + attendance_factor + lms_factor + study_factor + stress_penalty + sleep_factor
    midterm_score = midterm_score + np.random.normal(0, 8, n_students)
    df['midterm_score'] = np.clip(midterm_score, 0, 100).round(1)

    # Quiz average
    quiz_score = base_score + lms_factor + study_factor + np.random.normal(0, 10, n_students)
    df['quiz_average'] = np.clip(quiz_score, 0, 100).round(1)

    # Assignment average
    assignment_completion = (df['assignments_on_time'] / 20) * 100
    df['assignment_average'] = np.clip(assignment_completion * 0.7 + base_score * 0.3 + np.random.normal(0, 5, n_students), 0, 100).round(1)

    return df

def generate_target_variables(df):
    """Generate target variables for prediction"""

    n_students = len(df)

    # Calculate final grade based on all factors
    weights = {
        'midterm': 0.25,
        'quiz': 0.15,
        'assignment': 0.20,
        'attendance': 0.10,
        'final_exam': 0.30
    }

    # Simulate final exam (correlated with midterm and preparation)
    final_exam_base = df['midterm_score'] + (df['study_hours_per_week'] / 30) * 15
    final_exam = final_exam_base + np.random.normal(0, 10, n_students)
    df['final_exam_score'] = np.clip(final_exam, 0, 100).round(1)

    # Calculate final grade
    final_grade = (
        df['midterm_score'] * weights['midterm'] +
        df['quiz_average'] * weights['quiz'] +
        df['assignment_average'] * weights['assignment'] +
        df['attendance_rate'] * weights['attendance'] +
        df['final_exam_score'] * weights['final_exam']
    )

    df['final_grade'] = np.clip(final_grade, 0, 100).round(1)

    # Convert to letter grade
    def get_letter_grade(score):
        if score >= 90: return 'A'
        elif score >= 80: return 'B'
        elif score >= 70: return 'C'
        elif score >= 60: return 'D'
        else: return 'F'

    df['letter_grade'] = df['final_grade'].apply(get_letter_grade)

    # Risk level (target for intervention)
    def get_risk_level(row):
        risk_score = 0

        # Academic factors
        if row['midterm_score'] < 60: risk_score += 3
        elif row['midterm_score'] < 70: risk_score += 2
        elif row['midterm_score'] < 80: risk_score += 1

        if row['attendance_rate'] < 70: risk_score += 3
        elif row['attendance_rate'] < 80: risk_score += 2
        elif row['attendance_rate'] < 90: risk_score += 1

        if row['assignments_on_time'] < 12: risk_score += 2
        elif row['assignments_on_time'] < 16: risk_score += 1

        # Behavioral factors
        if row['lms_hours_per_week'] < 5: risk_score += 2
        if row['study_hours_per_week'] < 10: risk_score += 2
        if row['stress_level'] >= 4: risk_score += 1
        if row['avg_sleep_hours'] < 6: risk_score += 1

        # Classify risk
        if risk_score >= 8: return 'High Risk'
        elif risk_score >= 4: return 'Medium Risk'
        else: return 'Low Risk'

    df['risk_level'] = df.apply(get_risk_level, axis=1)

    # Pass/Fail
    df['pass_fail'] = df['final_grade'].apply(lambda x: 'Pass' if x >= 60 else 'Fail')

    return df

def main():
    """Main function to generate complete dataset"""

    print("Generating Synthetic Academic Performance Dataset...")
    print("=" * 60)

    # Number of students
    n_students = 100000

    # Generate dataset step by step
    print(f"\n1. Generating demographics for {n_students} students...")
    df = generate_student_demographics(n_students)

    print("2. Generating academic history...")
    df = generate_academic_history(df)

    print("3. Generating current semester data...")
    df = generate_current_semester_data(df)

    print("4. Generating attendance data...")
    df = generate_attendance_data(df)

    print("5. Generating LMS activity data...")
    df = generate_lms_activity(df)

    print("6. Generating behavioral data...")
    df = generate_behavioral_data(df)

    print("7. Generating assessment scores...")
    df = generate_assessment_scores(df)

    print("8. Generating target variables...")
    df = generate_target_variables(df)

    # Save dataset
    output_file = 'academic_performance_dataset.csv'
    df.to_csv(output_file, index=False)
    print(f"\n✓ Dataset saved to '{output_file}'")

    # Generate summary statistics
    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    print(f"Total Students: {len(df)}")
    print(f"Total Features: {len(df.columns)}")
    print(f"\nRisk Level Distribution:")
    print(df['risk_level'].value_counts())
    print(f"\nPass/Fail Distribution:")
    print(df['pass_fail'].value_counts())
    print(f"\nLetter Grade Distribution:")
    print(df['letter_grade'].value_counts().sort_index())
    print(f"\nAverage Final Grade: {df['final_grade'].mean():.2f}")
    print(f"Average GPA: {df['cumulative_gpa'].mean():.2f}")
    print(f"Average Attendance: {df['attendance_rate'].mean():.2f}%")

    return df

if __name__ == "__main__":
    df = main()
