"""
Generate SHAP Visualizations from saved SHAP values
This script loads pre-computed SHAP values and creates all visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

print("="*80)
print("GENERATING SHAP VISUALIZATIONS")
print("="*80)

# Load saved SHAP values
print("\n[1/3] Loading saved SHAP values...")
with open('outputs/shap_values.pkl', 'rb') as f:
    shap_data = pickle.load(f)

shap_values = shap_data['shap_values']
X_test_sample = shap_data['X_test_sample']
feature_names = shap_data['feature_names']
class_names = shap_data['class_names']

print(f"Loaded SHAP values for {len(class_names)} classes")
print(f"Sample size: {X_test_sample.shape[0]} students")
print(f"Features: {len(feature_names)}")

# Convert X_test_sample to DataFrame
X_test_sample_df = pd.DataFrame(X_test_sample, columns=feature_names)

# Import shap after loading data
import shap

print("\n[2/3] Generating per-class SHAP summary plots...")
# Create summary plot for each class
for i, class_name in enumerate(class_names):
    print(f"  Creating plot for {class_name}...")
    plt.figure(figsize=(12, 8))
    shap.summary_plot(shap_values[i], X_test_sample_df,
                     show=False, max_display=20)
    plt.title(f'SHAP Feature Importance - {class_name}', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f'outputs/shap_summary_{class_name.replace(" ", "_")}.png',
                dpi=300, bbox_inches='tight')
    plt.close()
    print(f"    [OK] Saved shap_summary_{class_name.replace(' ', '_')}.png")

print("\n[3/3] Generating global feature importance plot...")
# Calculate mean absolute SHAP values
mean_abs_shap = np.abs(shap_values).mean(axis=1).mean(axis=0)
feature_importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': mean_abs_shap
}).sort_values('importance', ascending=False)

# Create bar plot
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
print("  [OK] Saved shap_global_importance.png")

# Save feature importance to CSV
feature_importance_df.to_csv('outputs/feature_importance.csv', index=False)
print("  [OK] Saved feature_importance.csv")

print("\n" + "="*80)
print("SHAP VISUALIZATIONS COMPLETED!")
print("="*80)
print("\nGenerated files:")
print("  - outputs/shap_summary_High_Risk.png")
print("  - outputs/shap_summary_Low_Risk.png")
print("  - outputs/shap_summary_Medium_Risk.png")
print("  - outputs/shap_global_importance.png")
print("  - outputs/feature_importance.csv")

print("\nTop 10 Most Important Features:")
print(feature_importance_df.head(10).to_string(index=False))

