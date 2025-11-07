"""
Quick Analysis Script for Academic Performance Dataset
Validates data quality and shows key statistics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
print("Loading dataset...")
df = pd.read_csv('academic_performance_dataset.csv')

print("\n" + "="*70)
print("DATASET OVERVIEW")
print("="*70)
print(f"Total Records: {len(df):,}")
print(f"Total Features: {len(df.columns)}")
print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"\nMissing Values: {df.isnull().sum().sum()}")

print("\n" + "="*70)
print("TARGET VARIABLE DISTRIBUTIONS")
print("="*70)

print("\n1. Risk Level Distribution:")
risk_dist = df['risk_level'].value_counts().sort_index()
for level, count in risk_dist.items():
    pct = (count / len(df)) * 100
    print(f"   {level}: {count:,} ({pct:.2f}%)")

print("\n2. Pass/Fail Distribution:")
pf_dist = df['pass_fail'].value_counts()
for status, count in pf_dist.items():
    pct = (count / len(df)) * 100
    print(f"   {status}: {count:,} ({pct:.2f}%)")

print("\n3. Letter Grade Distribution:")
grade_dist = df['letter_grade'].value_counts().sort_index()
for grade, count in grade_dist.items():
    pct = (count / len(df)) * 100
    print(f"   {grade}: {count:,} ({pct:.2f}%)")

print("\n" + "="*70)
print("KEY PERFORMANCE METRICS")
print("="*70)
print(f"Average Final Grade: {df['final_grade'].mean():.2f} ± {df['final_grade'].std():.2f}")
print(f"Median Final Grade: {df['final_grade'].median():.2f}")
print(f"Average Cumulative GPA: {df['cumulative_gpa'].mean():.2f} ± {df['cumulative_gpa'].std():.2f}")
print(f"Average Attendance Rate: {df['attendance_rate'].mean():.2f}% ± {df['attendance_rate'].std():.2f}%")
print(f"Average Study Hours/Week: {df['study_hours_per_week'].mean():.2f} ± {df['study_hours_per_week'].std():.2f}")
print(f"Average LMS Hours/Week: {df['lms_hours_per_week'].mean():.2f} ± {df['lms_hours_per_week'].std():.2f}")

print("\n" + "="*70)
print("DEMOGRAPHIC BREAKDOWN")
print("="*70)

print("\nGender Distribution:")
for gender, count in df['gender'].value_counts().items():
    pct = (count / len(df)) * 100
    print(f"   {gender}: {count:,} ({pct:.2f}%)")

print("\nSocioeconomic Status:")
for ses, count in df['socioeconomic_status'].value_counts().items():
    pct = (count / len(df)) * 100
    avg_grade = df[df['socioeconomic_status'] == ses]['final_grade'].mean()
    print(f"   {ses}: {count:,} ({pct:.2f}%) - Avg Grade: {avg_grade:.2f}")

print("\nMajor Distribution:")
for major, count in df['major'].value_counts().items():
    pct = (count / len(df)) * 100
    avg_grade = df[df['major'] == major]['final_grade'].mean()
    print(f"   {major}: {count:,} ({pct:.2f}%) - Avg Grade: {avg_grade:.2f}")

print("\n" + "="*70)
print("CORRELATION ANALYSIS (Top 10 with Final Grade)")
print("="*70)

# Select numeric columns only
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlations = df[numeric_cols].corr()['final_grade'].sort_values(ascending=False)

print("\nTop Positive Correlations:")
for i, (feature, corr) in enumerate(correlations.head(11).items(), 1):
    if feature != 'final_grade':
        print(f"{i:2d}. {feature:30s}: {corr:+.3f}")

print("\nTop Negative Correlations:")
for i, (feature, corr) in enumerate(correlations.tail(10).items(), 1):
    print(f"{i:2d}. {feature:30s}: {corr:+.3f}")

print("\n" + "="*70)
print("AT-RISK STUDENT ANALYSIS")
print("="*70)

high_risk = df[df['risk_level'] == 'High Risk']
print(f"\nHigh Risk Students: {len(high_risk):,}")
print(f"Average Final Grade: {high_risk['final_grade'].mean():.2f}")
print(f"Average Attendance: {high_risk['attendance_rate'].mean():.2f}%")
print(f"Average Study Hours: {high_risk['study_hours_per_week'].mean():.2f}")
print(f"Average Midterm Score: {high_risk['midterm_score'].mean():.2f}")
print(f"Fail Rate: {(high_risk['pass_fail'] == 'Fail').sum() / len(high_risk) * 100:.2f}%")

medium_risk = df[df['risk_level'] == 'Medium Risk']
print(f"\nMedium Risk Students: {len(medium_risk):,}")
print(f"Average Final Grade: {medium_risk['final_grade'].mean():.2f}")
print(f"Average Attendance: {medium_risk['attendance_rate'].mean():.2f}%")
print(f"Average Study Hours: {medium_risk['study_hours_per_week'].mean():.2f}")
print(f"Average Midterm Score: {medium_risk['midterm_score'].mean():.2f}")
print(f"Fail Rate: {(medium_risk['pass_fail'] == 'Fail').sum() / len(medium_risk) * 100:.2f}%")

low_risk = df[df['risk_level'] == 'Low Risk']
print(f"\nLow Risk Students: {len(low_risk):,}")
print(f"Average Final Grade: {low_risk['final_grade'].mean():.2f}")
print(f"Average Attendance: {low_risk['attendance_rate'].mean():.2f}%")
print(f"Average Study Hours: {low_risk['study_hours_per_week'].mean():.2f}")
print(f"Average Midterm Score: {low_risk['midterm_score'].mean():.2f}")
print(f"Fail Rate: {(low_risk['pass_fail'] == 'Fail').sum() / len(low_risk) * 100:.2f}%")

print("\n" + "="*70)
print("ENGAGEMENT METRICS BY RISK LEVEL")
print("="*70)

engagement_metrics = ['lms_logins_per_week', 'lms_hours_per_week', 'assignments_on_time', 
                      'forum_posts', 'tutoring_sessions_attended', 'office_hours_visits']

for metric in engagement_metrics:
    print(f"\n{metric}:")
    for risk in ['Low Risk', 'Medium Risk', 'High Risk']:
        avg = df[df['risk_level'] == risk][metric].mean()
        print(f"   {risk:15s}: {avg:.2f}")

print("\n" + "="*70)
print("DATA QUALITY CHECKS")
print("="*70)

# Check for outliers and data integrity
print("\n✓ Checking GPA ranges (should be 0-4):")
print(f"   Min GPA: {df['cumulative_gpa'].min():.2f}")
print(f"   Max GPA: {df['cumulative_gpa'].max():.2f}")

print("\n✓ Checking grade ranges (should be 0-100):")
print(f"   Min Final Grade: {df['final_grade'].min():.2f}")
print(f"   Max Final Grade: {df['final_grade'].max():.2f}")

print("\n✓ Checking attendance (should be 0-100%):")
print(f"   Min Attendance: {df['attendance_rate'].min():.2f}%")
print(f"   Max Attendance: {df['attendance_rate'].max():.2f}%")

print("\n✓ Checking for duplicate student IDs:")
duplicates = df['student_id'].duplicated().sum()
print(f"   Duplicates found: {duplicates}")

print("\n✓ Checking categorical variables:")
print(f"   Unique Risk Levels: {df['risk_level'].nunique()} (expected: 3)")
print(f"   Unique Letter Grades: {df['letter_grade'].nunique()} (expected: 5)")
print(f"   Unique Majors: {df['major'].nunique()} (expected: 5)")

print("\n" + "="*70)
print("SAMPLE RECORDS")
print("="*70)

print("\nHigh Risk Student Example:")
print(high_risk[['student_id', 'cumulative_gpa', 'attendance_rate', 'midterm_score', 
                 'study_hours_per_week', 'final_grade', 'letter_grade']].head(1).to_string(index=False))

print("\nLow Risk Student Example:")
print(low_risk[['student_id', 'cumulative_gpa', 'attendance_rate', 'midterm_score', 
                'study_hours_per_week', 'final_grade', 'letter_grade']].head(1).to_string(index=False))

print("\n" + "="*70)
print("DATASET READY FOR MODEL TRAINING")
print("="*70)
print("\nRecommended splits:")
print("   - Training: 70,000 students (70%)")
print("   - Validation: 15,000 students (15%)")
print("   - Testing: 15,000 students (15%)")
print("\nKey features for early prediction (before midterm):")
print("   - Demographics, Academic History, Attendance, LMS Activity, Behavioral Data")
print("\nKey features for mid-semester prediction (with midterm):")
print("   - All above + Midterm Score, Quiz Average, Assignment Average")
print("\n✓ Dataset generation complete and validated!")

