"""
Starter Script for Academic Performance Prediction Model
Demonstrates basic model training pipeline
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("ACADEMIC PERFORMANCE PREDICTION - MODEL TRAINING")
print("="*70)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================
print("\n[1/7] Loading dataset...")
df = pd.read_csv('academic_performance_dataset.csv')
print(f"   Loaded {len(df):,} records with {len(df.columns)} features")

# ============================================================================
# 2. FEATURE ENGINEERING
# ============================================================================
print("\n[2/7] Engineering features...")

# Create interaction features
df['study_attendance_score'] = df['study_hours_per_week'] * (df['attendance_rate'] / 100)
df['engagement_score'] = (
    df['lms_hours_per_week'] * 0.4 +
    (df['assignments_on_time'] / 20) * 100 * 0.3 +
    (df['attendance_rate']) * 0.3
)
df['workload_pressure'] = df['study_hours_per_week'] + df['work_hours_per_week'] + df['extracurricular_hours']
df['resource_access_score'] = df['has_internet_at_home'] + df['has_study_space']

print(f"   Added 4 engineered features")

# ============================================================================
# 3. PREPARE FEATURES AND TARGET
# ============================================================================
print("\n[3/7] Preparing features and target...")

# Define target variable (choose one)
TARGET = 'risk_level'  # Options: 'risk_level', 'letter_grade', 'pass_fail', 'final_grade'

# Columns to exclude
exclude_cols = ['student_id', 'final_grade', 'letter_grade', 'risk_level', 'pass_fail', 
                'final_exam_score']  # Exclude final_exam as it's not available early

# Separate features and target
X = df.drop(columns=exclude_cols)
y = df[TARGET]

print(f"   Features: {X.shape[1]}")
print(f"   Target: {TARGET}")
print(f"   Target distribution:\n{y.value_counts()}")

# ============================================================================
# 4. ENCODE CATEGORICAL VARIABLES
# ============================================================================
print("\n[4/7] Encoding categorical variables...")

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
print(f"   Categorical columns: {len(categorical_cols)}")

# Label encode categorical features
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# Encode target if categorical
if y.dtype == 'object':
    le_target = LabelEncoder()
    y_encoded = le_target.fit_transform(y)
    n_classes = len(le_target.classes_)
    print(f"   Target classes: {le_target.classes_}")
else:
    y_encoded = y.values
    n_classes = 1  # Regression

# ============================================================================
# 5. SPLIT AND SCALE DATA
# ============================================================================
print("\n[5/7] Splitting and scaling data...")

# Split data (stratified for classification)
if n_classes > 1:
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y_encoded, test_size=0.3, stratify=y_encoded, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )
else:
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y_encoded, test_size=0.3, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )

print(f"   Training set: {len(X_train):,} samples")
print(f"   Validation set: {len(X_val):,} samples")
print(f"   Test set: {len(X_test):,} samples")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print(f"   Features scaled using StandardScaler")

# ============================================================================
# 6. BUILD AND TRAIN MODEL
# ============================================================================
print("\n[6/7] Building and training model...")

# Build neural network
model = keras.Sequential([
    layers.Dense(256, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    
    layers.Dense(128, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    layers.Dense(64, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.3),
    
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.2),
])

# Add output layer based on task
if n_classes > 1:
    # Classification
    model.add(layers.Dense(n_classes, activation='softmax'))
    loss = 'sparse_categorical_crossentropy'
    metrics = ['accuracy']
else:
    # Regression
    model.add(layers.Dense(1))
    loss = 'mse'
    metrics = ['mae']

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=loss,
    metrics=metrics
)

print("\nModel Architecture:")
model.summary()

# Callbacks
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-6
)

# Train model
print("\nTraining model...")
history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_val_scaled, y_val),
    epochs=100,
    batch_size=64,
    callbacks=[early_stopping, reduce_lr],
    verbose=1
)

# ============================================================================
# 7. EVALUATE MODEL
# ============================================================================
print("\n[7/7] Evaluating model...")

# Predictions
y_pred_proba = model.predict(X_test_scaled)

if n_classes > 1:
    # Classification metrics
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    print("\nTest Set Performance:")
    print("="*70)
    print(classification_report(y_test, y_pred, target_names=le_target.classes_))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=le_target.classes_, 
                yticklabels=le_target.classes_)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("\n✓ Confusion matrix saved to 'confusion_matrix.png'")
    
    # ROC-AUC for multi-class
    if n_classes == 2:
        roc_auc = roc_auc_score(y_test, y_pred_proba[:, 1])
        print(f"\nROC-AUC Score: {roc_auc:.4f}")
    else:
        from sklearn.preprocessing import label_binarize
        y_test_bin = label_binarize(y_test, classes=range(n_classes))
        roc_auc = roc_auc_score(y_test_bin, y_pred_proba, average='weighted', multi_class='ovr')
        print(f"\nWeighted ROC-AUC Score: {roc_auc:.4f}")
    
    # Class-wise performance
    print("\nPer-Class Performance:")
    print("="*70)
    for i, class_name in enumerate(le_target.classes_):
        mask = y_test == i
        if mask.sum() > 0:
            acc = (y_pred[mask] == i).sum() / mask.sum()
            print(f"{class_name:15s}: {acc:.2%} accuracy ({mask.sum():,} samples)")
    
else:
    # Regression metrics
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    y_pred = y_pred_proba.flatten()
    
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print("\nTest Set Performance:")
    print("="*70)
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")

# Plot training history
plt.figure(figsize=(14, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
metric_name = 'accuracy' if n_classes > 1 else 'mae'
plt.plot(history.history[metric_name], label=f'Training {metric_name.upper()}')
plt.plot(history.history[f'val_{metric_name}'], label=f'Validation {metric_name.upper()}')
plt.title(f'Model {metric_name.upper()}')
plt.xlabel('Epoch')
plt.ylabel(metric_name.upper())
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
print("✓ Training history saved to 'training_history.png'")

# ============================================================================
# FEATURE IMPORTANCE (using permutation importance)
# ============================================================================
print("\n" + "="*70)
print("FEATURE IMPORTANCE ANALYSIS")
print("="*70)

from sklearn.inspection import permutation_importance

# Calculate permutation importance
perm_importance = permutation_importance(
    model, X_test_scaled, y_test, n_repeats=10, random_state=42
)

# Get feature names
feature_names = X.columns.tolist()

# Sort by importance
indices = np.argsort(perm_importance.importances_mean)[::-1]

print("\nTop 15 Most Important Features:")
for i, idx in enumerate(indices[:15], 1):
    print(f"{i:2d}. {feature_names[idx]:30s}: {perm_importance.importances_mean[idx]:.4f} ± {perm_importance.importances_std[idx]:.4f}")

# Plot feature importance
plt.figure(figsize=(12, 8))
top_n = 20
top_indices = indices[:top_n]
plt.barh(range(top_n), perm_importance.importances_mean[top_indices])
plt.yticks(range(top_n), [feature_names[i] for i in top_indices])
plt.xlabel('Permutation Importance')
plt.title(f'Top {top_n} Most Important Features')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
print("\n✓ Feature importance plot saved to 'feature_importance.png'")

# ============================================================================
# SAVE MODEL
# ============================================================================
print("\n" + "="*70)
print("SAVING MODEL")
print("="*70)

model.save('academic_performance_model.h5')
print("✓ Model saved to 'academic_performance_model.h5'")

# Save scaler and encoders
import pickle

with open('preprocessing_objects.pkl', 'wb') as f:
    pickle.dump({
        'scaler': scaler,
        'label_encoders': label_encoders,
        'target_encoder': le_target if n_classes > 1 else None,
        'feature_names': feature_names
    }, f)
print("✓ Preprocessing objects saved to 'preprocessing_objects.pkl'")

print("\n" + "="*70)
print("MODEL TRAINING COMPLETE!")
print("="*70)
print("\nGenerated files:")
print("  1. academic_performance_model.h5 - Trained model")
print("  2. preprocessing_objects.pkl - Scaler and encoders")
print("  3. confusion_matrix.png - Confusion matrix visualization")
print("  4. training_history.png - Training curves")
print("  5. feature_importance.png - Feature importance plot")
print("\nNext steps:")
print("  - Fine-tune hyperparameters")
print("  - Try different architectures (LSTM, ensemble methods)")
print("  - Implement SHAP for better interpretability")
print("  - Deploy model for real-time predictions")
print("="*70)

