"""
Generate preprocessing_artifacts.pkl from the dataset
This script creates the missing preprocessing artifacts file needed by the API server
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder

print("Loading dataset...")
df = pd.read_csv('academic_performance_dataset.csv')

# Feature engineering (same as in train_model.py)
print("Engineering features...")
df['study_attendance_interaction'] = df['study_hours_per_week'] * df['attendance_rate']
df['gpa_difficulty_ratio'] = df['cumulative_gpa'] / (df['avg_course_difficulty'] + 1)
df['engagement_score'] = (df['lms_hours_per_week'] + df['library_visits_per_week']) / 2
df['workload_pressure'] = df['work_hours_per_week'] / (df['study_hours_per_week'] + 1)
df['resource_access_score'] = (df['library_visits_per_week'] + df['tutoring_sessions_attended']) / 2
df['academic_momentum'] = df['cumulative_gpa'] - df['previous_semester_gpa']
df['assignment_completion_rate'] = df['assignments_on_time'] / (df['assignments_submitted'] + 1)
df['lms_efficiency'] = df['lms_hours_per_week'] / (df['study_hours_per_week'] + 1)

# Prepare features and target
print("Preparing features...")
target_col = 'risk_level'
# Exclude columns that won't be available at prediction time (same as train_model.py)
exclude_cols = [
    'student_id',           # ID
    'final_grade',          # Target we're trying to predict
    'letter_grade',         # Derived from final_grade
    'risk_level',           # Our target
    'pass_fail',            # Derived from final_grade
    'final_exam_score'      # Not available until end of semester
]
feature_cols = [col for col in df.columns if col not in exclude_cols]

X = df[feature_cols].copy()
y = df[target_col].copy()

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
print(f"Found {len(categorical_cols)} categorical columns: {categorical_cols}")

# Encode categorical variables
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le
    print(f"  - Encoded: {col} ({len(le.classes_)} classes)")

# Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
class_names = le_target.classes_
n_classes = len(class_names)
print(f"\nTarget encoded: {n_classes} classes")
print(f"  Classes: {', '.join(class_names)}")

# Scale features
print("\nScaling features...")
scaler = StandardScaler()
scaler.fit(X)

# Get feature names
feature_names = X.columns.tolist()
original_features = [col for col in feature_cols if col not in [
    'study_attendance_interaction', 'gpa_difficulty_ratio', 'engagement_score',
    'workload_pressure', 'resource_access_score', 'academic_momentum',
    'assignment_completion_rate', 'lms_efficiency'
]]

# Create preprocessing artifacts dictionary
preprocessing_artifacts = {
    'scaler': scaler,
    'label_encoders': label_encoders,
    'target_encoder': le_target,
    'feature_names': feature_names,
    'class_names': class_names.tolist(),
    'n_classes': n_classes,
    'original_features': original_features
}

# Save to file
print("\nSaving preprocessing artifacts...")
with open('outputs/preprocessing_artifacts.pkl', 'wb') as f:
    pickle.dump(preprocessing_artifacts, f)

print("✓ Preprocessing artifacts saved to 'outputs/preprocessing_artifacts.pkl'")
print(f"\nArtifacts include:")
print(f"  - Scaler: StandardScaler")
print(f"  - Label encoders: {len(label_encoders)} encoders")
print(f"  - Target encoder: {n_classes} classes")
print(f"  - Feature names: {len(feature_names)} features")
print(f"  - Original features: {len(original_features)} features")
