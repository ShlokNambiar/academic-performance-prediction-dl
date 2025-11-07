"""
Complete SHAP Analysis for the trained model
This script loads the trained model and generates SHAP visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import shap
from tensorflow import keras
from sklearn.preprocessing import StandardScaler, LabelEncoder

print("="*80)
print("COMPLETING SHAP INTERPRETABILITY ANALYSIS")
print("="*80)

# Load the dataset
print("\n[1/6] Loading dataset...")
df = pd.read_csv('academic_performance_dataset.csv')
print(f"Loaded {len(df):,} records")

# Feature engineering (same as in training)
print("\n[2/6] Feature engineering...")
df['study_attendance_interaction'] = df['study_hours_per_week'] * (df['attendance_rate'] / 100)
df['gpa_difficulty_ratio'] = df['cumulative_gpa'] / (df['avg_course_difficulty'] + 0.1)
df['engagement_score'] = (df['lms_hours_per_week'] * 0.4 + (df['assignments_on_time'] / 20) * 100 * 0.3 + df['attendance_rate'] * 0.3)
df['workload_pressure'] = df['study_hours_per_week'] + df['work_hours_per_week'] + df['extracurricular_hours']
df['resource_access_score'] = df['has_internet_at_home'] + df['has_study_space']
df['academic_momentum'] = (df['cumulative_gpa'] - df['previous_semester_gpa']) * 10
df['assignment_completion_rate'] = df['assignments_on_time'] / (df['assignments_submitted'] + 0.1)
df['lms_efficiency'] = df['lms_hours_per_week'] / (df['lms_logins_per_week'] + 0.1)

# Prepare features
TARGET = 'risk_level'
X = df.drop(columns=[TARGET])
y = df[TARGET]

# Encode categorical variables
print("\n[3/6] Encoding categorical variables...")
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
class_names = le_target.classes_

# Split data (same split as training)
from sklearn.model_selection import train_test_split
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y_encoded, test_size=0.15, random_state=42, stratify=y_encoded
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.176, random_state=42, stratify=y_temp
)

# Scale features
print("\n[4/6] Scaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Load the trained model
print("\n[5/6] Loading trained model...")
model = keras.models.load_model('best_model.keras')
print("Model loaded successfully")

# SHAP Analysis
print("\n[6/6] Running SHAP analysis...")
print("This may take several minutes...")

# Use a sample for SHAP
sample_size = 1000
X_train_sample = X_train_scaled[np.random.choice(X_train_scaled.shape[0], sample_size, replace=False)]
X_test_sample = X_test_scaled[np.random.choice(X_test_scaled.shape[0], min(500, X_test_scaled.shape[0]), replace=False)]

# Create SHAP explainer
explainer = shap.DeepExplainer(model, X_train_sample)
shap_values = explainer.shap_values(X_test_sample)

print("SHAP values calculated")

# Get feature names
feature_names = X.columns.tolist()

# Convert X_test_sample to DataFrame for SHAP
X_test_sample_df = pd.DataFrame(X_test_sample, columns=feature_names)

# Generate SHAP visualizations
print("\nGenerating SHAP visualizations...")

# 1. Summary plot for each class
for i, class_name in enumerate(class_names):
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values[i], X_test_sample_df,
                     show=False, max_display=20)
    plt.title(f'SHAP Feature Importance - {class_name}', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'outputs/shap_summary_{class_name.replace(" ", "_")}.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] SHAP summary plot for {class_name}")

# 2. Mean absolute SHAP values (global feature importance)
mean_abs_shap = np.abs(shap_values).mean(axis=1).mean(axis=0)
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': mean_abs_shap
}).sort_values('importance', ascending=False)

plt.figure(figsize=(12, 10))
top_n = 25
top_features = feature_importance_df.head(top_n)
plt.barh(range(top_n), top_features['importance'].values)
plt.yticks(range(top_n), top_features['feature'].values)
plt.xlabel('Mean |SHAP value|', fontsize=12)
plt.title(f'Top {top_n} Most Important Features (Global)', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('outputs/shap_global_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("  [OK] Global feature importance plot")

# Save feature importance
feature_importance_df.to_csv('outputs/feature_importance.csv', index=False)
print("  [OK] Feature importance saved to CSV")

print("\n" + "="*80)
print("SHAP ANALYSIS COMPLETED SUCCESSFULLY!")
print("="*80)
print("\nGenerated files:")
print("  - outputs/shap_summary_High_Risk.png")
print("  - outputs/shap_summary_Low_Risk.png")
print("  - outputs/shap_summary_Medium_Risk.png")
print("  - outputs/shap_global_importance.png")
print("  - outputs/feature_importance.csv")
print("\nTop 10 Most Important Features:")
print(feature_importance_df.head(10).to_string(index=False))

