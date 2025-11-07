"""
Production Model Training Pipeline for Academic Performance Prediction
Includes: Preprocessing, DNN Training, Evaluation, SHAP Interpretability
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pickle
import json
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report, confusion_matrix,
    accuracy_score, precision_recall_fscore_support,
    roc_auc_score, roc_curve, auc
)

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks
from tensorflow.keras.utils import to_categorical

# Interpretability
import shap

# Configure GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Enable memory growth to prevent TensorFlow from allocating all GPU memory
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        # Set GPU as visible device
        tf.config.set_visible_devices(gpus, 'GPU')

        print(f"✓ Found {len(gpus)} GPU(s)")
        for i, gpu in enumerate(gpus):
            print(f"  GPU {i}: {gpu.name}")
    except RuntimeError as e:
        print(f"GPU configuration error: {e}")
else:
    print("WARNING: No GPU found - training will use CPU (slower)")

# Enable mixed precision for faster GPU training
if gpus:
    try:
        from tensorflow.keras import mixed_precision
        policy = mixed_precision.Policy('mixed_float16')
        mixed_precision.set_global_policy(policy)
        print("✓ Mixed precision training enabled (float16) for faster GPU performance")
    except Exception as e:
        print(f"⚠ Could not enable mixed precision: {e}")

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("\n" + "="*80)
print("ACADEMIC PERFORMANCE PREDICTION - PRODUCTION MODEL TRAINING")
print("="*80)
print(f"Training started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"TensorFlow version: {tf.__version__}")
print(f"GPU Available: {len(gpus) > 0 if gpus else False}")
print(f"GPU Count: {len(gpus) if gpus else 0}")
print(f"Compute Device: {'GPU (CUDA)' if gpus else 'CPU'}")

# ============================================================================
# 1. LOAD AND EXPLORE DATA
# ============================================================================
print("\n" + "="*80)
print("STEP 1: LOADING DATA")
print("="*80)

df = pd.read_csv('academic_performance_dataset.csv')
print(f"✓ Loaded {len(df):,} student records with {len(df.columns)} features")
print(f"✓ Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
print(f"✓ Missing values: {df.isnull().sum().sum()}")

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================
print("\n" + "="*80)
print("STEP 2: FEATURE ENGINEERING")
print("="*80)

# Create interaction features
df['study_attendance_interaction'] = df['study_hours_per_week'] * (df['attendance_rate'] / 100)
df['gpa_difficulty_ratio'] = df['cumulative_gpa'] / (df['avg_course_difficulty'] + 0.1)
df['engagement_score'] = (
    df['lms_hours_per_week'] * 0.4 +
    (df['assignments_on_time'] / 20) * 100 * 0.3 +
    df['attendance_rate'] * 0.3
)
df['workload_pressure'] = df['study_hours_per_week'] + df['work_hours_per_week'] + df['extracurricular_hours']
df['resource_access_score'] = df['has_internet_at_home'] + df['has_study_space']
df['academic_momentum'] = (df['cumulative_gpa'] - df['previous_semester_gpa']) * 10
df['assignment_completion_rate'] = df['assignments_on_time'] / (df['assignments_submitted'] + 0.1)
df['lms_efficiency'] = df['lms_hours_per_week'] / (df['lms_logins_per_week'] + 0.1)

print(f"✓ Added 8 engineered features")
print(f"✓ Total features now: {len(df.columns)}")

# ============================================================================
# 3. PREPARE FEATURES AND TARGET
# ============================================================================
print("\n" + "="*80)
print("STEP 3: PREPARING FEATURES AND TARGET")
print("="*80)

# Define target variable
TARGET = 'risk_level'

# Exclude columns that won't be available at prediction time
exclude_cols = [
    'student_id',           # ID
    'final_grade',          # Target we're trying to predict
    'letter_grade',         # Derived from final_grade
    'risk_level',           # Our target
    'pass_fail',            # Derived from final_grade
    'final_exam_score'      # Not available until end of semester
]

# Separate features and target
X = df.drop(columns=exclude_cols)
y = df[TARGET]

print(f"✓ Features: {X.shape[1]}")
print(f"✓ Target: {TARGET}")
print(f"\nTarget Distribution:")
for level, count in y.value_counts().items():
    pct = (count / len(y)) * 100
    print(f"  {level:15s}: {count:6,} ({pct:5.2f}%)")

# ============================================================================
# 4. ENCODE CATEGORICAL VARIABLES
# ============================================================================
print("\n" + "="*80)
print("STEP 4: ENCODING CATEGORICAL VARIABLES")
print("="*80)

# Store original feature names
original_features = X.columns.tolist()

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
print(f"✓ Found {len(categorical_cols)} categorical columns")

# Label encode categorical features
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le
    print(f"  - Encoded: {col} ({len(le.classes_)} classes)")

# Encode target
le_target = LabelEncoder()
y_encoded = le_target.fit_transform(y)
n_classes = len(le_target.classes_)
class_names = le_target.classes_

print(f"\n✓ Target encoded: {n_classes} classes")
print(f"  Classes: {', '.join(class_names)}")

# ============================================================================
# 5. SPLIT DATA
# ============================================================================
print("\n" + "="*80)
print("STEP 5: SPLITTING DATA")
print("="*80)

# Split: 70% train, 15% validation, 15% test
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y_encoded, test_size=0.3, stratify=y_encoded, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)

print(f"✓ Training set:   {len(X_train):6,} samples ({len(X_train)/len(X)*100:.1f}%)")
print(f"✓ Validation set: {len(X_val):6,} samples ({len(X_val)/len(X)*100:.1f}%)")
print(f"✓ Test set:       {len(X_test):6,} samples ({len(X_test)/len(X)*100:.1f}%)")

# Verify stratification
print("\nClass distribution in splits:")
for i, class_name in enumerate(class_names):
    train_pct = (y_train == i).sum() / len(y_train) * 100
    val_pct = (y_val == i).sum() / len(y_val) * 100
    test_pct = (y_test == i).sum() / len(y_test) * 100
    print(f"  {class_name:15s}: Train={train_pct:5.2f}% | Val={val_pct:5.2f}% | Test={test_pct:5.2f}%")

# ============================================================================
# 6. SCALE FEATURES
# ============================================================================
print("\n" + "="*80)
print("STEP 6: SCALING FEATURES")
print("="*80)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print(f"✓ Features scaled using StandardScaler")
print(f"  Mean: {X_train_scaled.mean():.6f}")
print(f"  Std:  {X_train_scaled.std():.6f}")

# ============================================================================
# 7. BUILD DEEP NEURAL NETWORK
# ============================================================================
print("\n" + "="*80)
print("STEP 7: BUILDING DEEP NEURAL NETWORK")
print("="*80)

def build_model(input_dim, n_classes):
    """Build DNN architecture"""
    model = keras.Sequential([
        # Input layer
        layers.Input(shape=(input_dim,)),

        # First hidden layer
        layers.Dense(256, kernel_initializer='he_normal'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.4),

        # Second hidden layer
        layers.Dense(128, kernel_initializer='he_normal'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.3),

        # Third hidden layer
        layers.Dense(64, kernel_initializer='he_normal'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.3),

        # Fourth hidden layer
        layers.Dense(32, kernel_initializer='he_normal'),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.2),

        # Output layer
        layers.Dense(n_classes, activation='softmax')
    ])

    return model

model = build_model(X_train_scaled.shape[1], n_classes)

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("✓ Model architecture:")
model.summary()

# ============================================================================
# 8. SETUP CALLBACKS
# ============================================================================
print("\n" + "="*80)
print("STEP 8: SETTING UP TRAINING CALLBACKS")
print("="*80)

# Early stopping
early_stop = callbacks.EarlyStopping(
    monitor='val_loss',
    patience=15,
    restore_best_weights=True,
    verbose=1
)

# Reduce learning rate on plateau
reduce_lr = callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=7,
    min_lr=1e-7,
    verbose=1
)

# Model checkpoint
checkpoint = callbacks.ModelCheckpoint(
    'best_model.keras',
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

# TensorBoard
tensorboard = callbacks.TensorBoard(
    log_dir=f'./logs/{datetime.now().strftime("%Y%m%d-%H%M%S")}',
    histogram_freq=1
)

callback_list = [early_stop, reduce_lr, checkpoint, tensorboard]
print(f"✓ Configured {len(callback_list)} callbacks")

# ============================================================================
# 9. TRAIN MODEL
# ============================================================================
print("\n" + "="*80)
print("STEP 9: TRAINING MODEL")
print("="*80)

print("Starting training...")
print(f"Epochs: 100 (with early stopping)")
print(f"Batch size: 64")
print(f"Optimizer: Adam (lr=0.001)")
print("-" * 80)

history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=100,
    batch_size=64,
    callbacks=callback_list,
    verbose=1
)

print("\n✓ Training completed!")
print(f"  Total epochs: {len(history.history['loss'])}")
print(f"  Best val_accuracy: {max(history.history['val_accuracy']):.4f}")
print(f"  Best val_loss: {min(history.history['val_loss']):.4f}")

# Save training history
with open('training_history.pkl', 'wb') as f:
    pickle.dump(history.history, f)
print("✓ Training history saved")

# ============================================================================
# 10. EVALUATE MODEL
# ============================================================================
print("\n" + "="*80)
print("STEP 10: EVALUATING MODEL")
print("="*80)

# Load best model
model = keras.models.load_model('best_model.keras')
print("✓ Loaded best model from checkpoint")

# Predictions
y_pred_proba = model.predict(X_test_scaled, verbose=0)
y_pred = np.argmax(y_pred_proba, axis=1)

# Calculate metrics
test_accuracy = accuracy_score(y_test, y_pred)
precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average='weighted')

print("\n" + "="*80)
print("TEST SET PERFORMANCE")
print("="*80)
print(f"Accuracy:  {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")

# Detailed classification report
print("\n" + "-"*80)
print("DETAILED CLASSIFICATION REPORT")
print("-"*80)
print(classification_report(y_test, y_pred, target_names=class_names, digits=4))

# Per-class metrics
print("\n" + "-"*80)
print("PER-CLASS PERFORMANCE")
print("-"*80)
for i, class_name in enumerate(class_names):
    mask = y_test == i
    if mask.sum() > 0:
        class_acc = (y_pred[mask] == i).sum() / mask.sum()
        # Get per-class metrics from the overall classification report
        class_precision = precision_recall_fscore_support(y_test, y_pred, average=None, zero_division=0)[0][i]
        class_recall = precision_recall_fscore_support(y_test, y_pred, average=None, zero_division=0)[1][i]
        class_f1 = precision_recall_fscore_support(y_test, y_pred, average=None, zero_division=0)[2][i]
        print(f"{class_name:15s}: Accuracy={class_acc:.4f} | Precision={class_precision:.4f} | "
              f"Recall={class_recall:.4f} | F1={class_f1:.4f} | Samples={mask.sum():,}")

# Save evaluation results
evaluation_results = {
    'test_accuracy': float(test_accuracy),
    'precision': float(precision),
    'recall': float(recall),
    'f1_score': float(f1),
    'classification_report': classification_report(y_test, y_pred, target_names=class_names, output_dict=True),
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

with open('evaluation_results.json', 'w') as f:
    json.dump(evaluation_results, f, indent=2)
print("\n✓ Evaluation results saved to 'evaluation_results.json'")

print("\n" + "="*80)
print("STEP 10 COMPLETED: Model Evaluation")
print("="*80)

# ============================================================================
# 11. ROC-AUC ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("STEP 11: ROC-AUC ANALYSIS")
print("="*80)

# Calculate ROC-AUC for multi-class
from sklearn.preprocessing import label_binarize

y_test_bin = label_binarize(y_test, classes=range(n_classes))
roc_auc_weighted = roc_auc_score(y_test_bin, y_pred_proba, average='weighted', multi_class='ovr')
roc_auc_macro = roc_auc_score(y_test_bin, y_pred_proba, average='macro', multi_class='ovr')

print(f"✓ ROC-AUC (Weighted): {roc_auc_weighted:.4f}")
print(f"✓ ROC-AUC (Macro):    {roc_auc_macro:.4f}")

# Per-class ROC-AUC
print("\nPer-Class ROC-AUC:")
for i, class_name in enumerate(class_names):
    class_roc_auc = roc_auc_score(y_test_bin[:, i], y_pred_proba[:, i])
    print(f"  {class_name:15s}: {class_roc_auc:.4f}")

# Save ROC-AUC results
evaluation_results['roc_auc_weighted'] = float(roc_auc_weighted)
evaluation_results['roc_auc_macro'] = float(roc_auc_macro)

# ============================================================================
# 12. VISUALIZATIONS
# ============================================================================
print("\n" + "="*80)
print("STEP 12: GENERATING VISUALIZATIONS")
print("="*80)

# Create output directory for plots
import os
os.makedirs('outputs', exist_ok=True)

# 1. Confusion Matrix
plt.figure(figsize=(10, 8))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names,
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix - Test Set', fontsize=16, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig('outputs/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Confusion matrix saved")

# 2. Training History
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Loss
axes[0].plot(history.history['loss'], label='Training Loss', linewidth=2)
axes[0].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[0].set_title('Model Loss Over Epochs', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Epoch', fontsize=12)
axes[0].set_ylabel('Loss', fontsize=12)
axes[0].legend(fontsize=10)
axes[0].grid(True, alpha=0.3)

# Accuracy
axes[1].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
axes[1].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
axes[1].set_title('Model Accuracy Over Epochs', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Epoch', fontsize=12)
axes[1].set_ylabel('Accuracy', fontsize=12)
axes[1].legend(fontsize=10)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/training_history.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Training history plot saved")

# 3. ROC Curves (One-vs-Rest)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (class_name, ax) in enumerate(zip(class_names, axes)):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_pred_proba[:, i])
    roc_auc = auc(fpr, tpr)

    ax.plot(fpr, tpr, linewidth=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random Classifier')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate', fontsize=11)
    ax.set_ylabel('True Positive Rate', fontsize=11)
    ax.set_title(f'ROC Curve - {class_name}', fontsize=12, fontweight='bold')
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('outputs/roc_curves.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ ROC curves saved")

# 4. Class Distribution Comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# True vs Predicted
class_counts_true = pd.Series(y_test).map({i: name for i, name in enumerate(class_names)}).value_counts()
class_counts_pred = pd.Series(y_pred).map({i: name for i, name in enumerate(class_names)}).value_counts()

x = np.arange(len(class_names))
width = 0.35

axes[0].bar(x - width/2, [class_counts_true.get(name, 0) for name in class_names],
            width, label='True', alpha=0.8)
axes[0].bar(x + width/2, [class_counts_pred.get(name, 0) for name in class_names],
            width, label='Predicted', alpha=0.8)
axes[0].set_xlabel('Risk Level', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].set_title('True vs Predicted Distribution', fontsize=14, fontweight='bold')
axes[0].set_xticks(x)
axes[0].set_xticklabels(class_names, rotation=15)
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# Prediction confidence
confidence_scores = np.max(y_pred_proba, axis=1)
axes[1].hist(confidence_scores, bins=50, alpha=0.7, edgecolor='black')
axes[1].axvline(confidence_scores.mean(), color='red', linestyle='--',
                linewidth=2, label=f'Mean: {confidence_scores.mean():.3f}')
axes[1].set_xlabel('Prediction Confidence', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].set_title('Prediction Confidence Distribution', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('outputs/class_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Class distribution plots saved")

print("\n✓ All visualizations saved to 'outputs/' directory")

# ============================================================================
# 13. SHAP INTERPRETABILITY ANALYSIS
# ============================================================================
print("\n" + "="*80)
print("STEP 13: SHAP INTERPRETABILITY ANALYSIS")
print("="*80)

print("Initializing SHAP explainer (this may take a few minutes)...")

# Use a sample for SHAP to speed up computation
sample_size = 1000
X_train_sample = X_train_scaled[np.random.choice(X_train_scaled.shape[0], sample_size, replace=False)]
X_test_sample = X_test_scaled[np.random.choice(X_test_scaled.shape[0], min(500, X_test_scaled.shape[0]), replace=False)]

# Create SHAP explainer
explainer = shap.DeepExplainer(model, X_train_sample)
shap_values = explainer.shap_values(X_test_sample)

print("✓ SHAP values calculated")

# Get feature names
feature_names = X.columns.tolist()

# Save SHAP values
shap_data = {
    'shap_values': [sv.tolist() for sv in shap_values],
    'feature_names': feature_names,
    'class_names': class_names.tolist()
}

with open('outputs/shap_values.pkl', 'wb') as f:
    pickle.dump(shap_data, f)
print("✓ SHAP values saved")

# Generate SHAP visualizations
print("\nGenerating SHAP visualizations...")

# Convert X_test_sample to DataFrame with feature names for SHAP
X_test_sample_df = pd.DataFrame(X_test_sample, columns=feature_names)

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
    print(f"  ✓ SHAP summary plot for {class_name}")

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
print("  ✓ Global feature importance plot")

# Save feature importance
feature_importance_df.to_csv('outputs/feature_importance.csv', index=False)
print("  ✓ Feature importance saved to CSV")

print("\n✓ SHAP analysis completed")

print("\n" + "="*80)
print("STEP 13 COMPLETED: SHAP Interpretability")
print("="*80)

# ============================================================================
# 14. SAVE ALL ARTIFACTS
# ============================================================================
print("\n" + "="*80)
print("STEP 14: SAVING MODEL ARTIFACTS")
print("="*80)

# Save final model
model.save('outputs/final_model.keras')
print("✓ Final model saved to 'outputs/final_model.keras'")

# Save preprocessing objects
preprocessing_artifacts = {
    'scaler': scaler,
    'label_encoders': label_encoders,
    'target_encoder': le_target,
    'feature_names': feature_names,
    'class_names': class_names.tolist(),
    'n_classes': n_classes,
    'original_features': original_features
}

with open('outputs/preprocessing_artifacts.pkl', 'wb') as f:
    pickle.dump(preprocessing_artifacts, f)
print("✓ Preprocessing artifacts saved")

# Update and save final evaluation results
evaluation_results.update({
    'model_architecture': 'Deep Neural Network (4 hidden layers)',
    'input_features': len(feature_names),
    'training_samples': len(X_train),
    'validation_samples': len(X_val),
    'test_samples': len(X_test),
    'epochs_trained': len(history.history['loss']),
    'best_val_accuracy': float(max(history.history['val_accuracy'])),
    'best_val_loss': float(min(history.history['val_loss']))
})

with open('outputs/evaluation_results.json', 'w') as f:
    json.dump(evaluation_results, f, indent=2)
print("✓ Final evaluation results saved")

print("\n" + "="*80)
print("STEP 14 COMPLETED: Model Artifacts Saved")
print("="*80)

# ============================================================================
# 15. GENERATE SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("STEP 15: GENERATING SUMMARY REPORT")
print("="*80)

summary_report = f"""
{'='*80}
ACADEMIC PERFORMANCE PREDICTION MODEL - TRAINING SUMMARY
{'='*80}

Training Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
TensorFlow Version: {tf.__version__}
GPU Used: {len(tf.config.list_physical_devices('GPU')) > 0}

{'='*80}
DATASET INFORMATION
{'='*80}
Total Samples: {len(df):,}
Training Samples: {len(X_train):,} (70%)
Validation Samples: {len(X_val):,} (15%)
Test Samples: {len(X_test):,} (15%)

Input Features: {len(feature_names)}
  - Original Features: {len(original_features)}
  - Engineered Features: {len(feature_names) - len(original_features)}

Target Variable: {TARGET}
Number of Classes: {n_classes}
Classes: {', '.join(class_names)}

Class Distribution (Test Set):
"""

for i, class_name in enumerate(class_names):
    count = (y_test == i).sum()
    pct = count / len(y_test) * 100
    summary_report += f"  {class_name:15s}: {count:5,} ({pct:5.2f}%)\n"

summary_report += f"""
{'='*80}
MODEL ARCHITECTURE
{'='*80}
Type: Deep Neural Network (DNN)
Layers:
  - Input: {len(feature_names)} features
  - Hidden Layer 1: 256 units (ReLU + BatchNorm + Dropout 0.4)
  - Hidden Layer 2: 128 units (ReLU + BatchNorm + Dropout 0.3)
  - Hidden Layer 3: 64 units (ReLU + BatchNorm + Dropout 0.3)
  - Hidden Layer 4: 32 units (ReLU + BatchNorm + Dropout 0.2)
  - Output: {n_classes} units (Softmax)

Total Parameters: {model.count_params():,}
Optimizer: Adam (initial lr=0.001)
Loss Function: Sparse Categorical Crossentropy

{'='*80}
TRAINING CONFIGURATION
{'='*80}
Epochs: 100 (with early stopping)
Batch Size: 64
Callbacks:
  - Early Stopping (patience=15, monitor=val_loss)
  - Reduce LR on Plateau (patience=7, factor=0.5)
  - Model Checkpoint (save best model)
  - TensorBoard Logging

Actual Epochs Trained: {len(history.history['loss'])}
Best Validation Accuracy: {max(history.history['val_accuracy']):.4f}
Best Validation Loss: {min(history.history['val_loss']):.4f}

{'='*80}
TEST SET PERFORMANCE
{'='*80}
Overall Metrics:
  Accuracy:  {test_accuracy:.4f}
  Precision: {precision:.4f}
  Recall:    {recall:.4f}
  F1-Score:  {f1:.4f}

ROC-AUC Scores:
  Weighted: {roc_auc_weighted:.4f}
  Macro:    {roc_auc_macro:.4f}

Per-Class Performance:
"""

for i, class_name in enumerate(class_names):
    mask = y_test == i
    if mask.sum() > 0:
        class_acc = (y_pred[mask] == i).sum() / mask.sum()
        class_roc_auc = roc_auc_score(y_test_bin[:, i], y_pred_proba[:, i])
        summary_report += f"  {class_name:15s}: Accuracy={class_acc:.4f} | ROC-AUC={class_roc_auc:.4f} | Samples={mask.sum():,}\n"

summary_report += f"""
{'='*80}
TOP 10 MOST IMPORTANT FEATURES (SHAP)
{'='*80}
"""

for idx, row in feature_importance_df.head(10).iterrows():
    summary_report += f"  {row['feature']:40s}: {row['importance']:.6f}\n"

summary_report += f"""
{'='*80}
OUTPUT FILES GENERATED
{'='*80}
Models:
  ✓ outputs/final_model.keras - Trained model
  ✓ best_model.keras - Best checkpoint during training

Preprocessing:
  ✓ outputs/preprocessing_artifacts.pkl - Scaler, encoders, feature names

Evaluation:
  ✓ outputs/evaluation_results.json - Complete metrics
  ✓ training_history.pkl - Training history

Visualizations:
  ✓ outputs/confusion_matrix.png - Confusion matrix
  ✓ outputs/training_history.png - Loss and accuracy curves
  ✓ outputs/roc_curves.png - ROC curves for each class
  ✓ outputs/class_distribution.png - Prediction analysis
  ✓ outputs/shap_summary_High_Risk.png - SHAP for High Risk
  ✓ outputs/shap_summary_Low_Risk.png - SHAP for Low Risk
  ✓ outputs/shap_summary_Medium_Risk.png - SHAP for Medium Risk
  ✓ outputs/shap_global_importance.png - Global feature importance

Data:
  ✓ outputs/feature_importance.csv - Feature importance rankings
  ✓ outputs/shap_values.pkl - SHAP values for interpretability

{'='*80}
MODEL READY FOR DEPLOYMENT
{'='*80}

Next Steps:
1. Review visualizations in 'outputs/' directory
2. Analyze SHAP plots to understand model decisions
3. Build intervention recommendation engine
4. Create prediction API or dashboard
5. Deploy for real-time student risk assessment

{'='*80}
TRAINING COMPLETED SUCCESSFULLY!
{'='*80}
"""

# Save summary report
with open('outputs/training_summary.txt', 'w') as f:
    f.write(summary_report)

print(summary_report)
print("\n✓ Summary report saved to 'outputs/training_summary.txt'")

print("\n" + "="*80)
print("STEP 15 COMPLETED: Summary Report Generated")
print("="*80)

# ============================================================================
# FINAL MESSAGE
# ============================================================================
print("\n" + "="*80)
print("🎉 MODEL TRAINING PIPELINE COMPLETED SUCCESSFULLY! 🎉")
print("="*80)
print(f"\nTotal execution time: {(datetime.now() - datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')).total_seconds():.0f} seconds")
print("\nAll outputs saved to 'outputs/' directory")
print("\nKey Achievements:")
print(f"  ✓ Trained DNN with {test_accuracy:.2%} test accuracy")
print(f"  ✓ ROC-AUC: {roc_auc_weighted:.4f}")
print(f"  ✓ SHAP interpretability implemented")
print(f"  ✓ {len(feature_names)} features analyzed")
print(f"  ✓ {len(df):,} students processed")
print("\nReady for intervention recommendation engine development!")
print("="*80)
