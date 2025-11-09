"""
Flask API Server for Academic Performance Prediction System
Provides endpoints for predictions, recommendations, and batch processing
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle
from tensorflow import keras
from sklearn.preprocessing import StandardScaler, LabelEncoder
from recommendation_engine import InterventionRecommendationEngine
from report_generator import ReportGenerator
import json
from datetime import datetime
import os

from collections import deque, Counter

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Global variables for model and preprocessing artifacts
model = None
scaler = None
label_encoders = None
target_encoder = None
feature_names = None
recommendation_engine = None
# In-memory log of recent predictions for educator insights
PREDICTION_LOG = deque(maxlen=5000)


def _log_prediction(student_data: dict, risk_level: str, confidence: float, probabilities: dict):
    entry = {
        'student_id': student_data.get('student_id', 'Unknown'),
        'risk_level': risk_level,
        'confidence': float(confidence),
        'probabilities': {k: float(v) for k, v in probabilities.items()},
        'timestamp': datetime.now().isoformat(),
        # Key student signals for aggregate insights
        'attendance_rate': student_data.get('attendance_rate'),
        'study_hours_per_week': student_data.get('study_hours_per_week'),
        'lms_hours_per_week': student_data.get('lms_hours_per_week'),
        'avg_sleep_hours': student_data.get('avg_sleep_hours'),
        'stress_level': student_data.get('stress_level'),
        'midterm_score': student_data.get('midterm_score'),
    }
    PREDICTION_LOG.append(entry)

report_generator = None

def load_model_and_artifacts():
    """Load trained model and preprocessing artifacts"""
    global model, scaler, label_encoders, target_encoder, feature_names, recommendation_engine, report_generator

    print("Loading model and artifacts...")

    # Load model
    model = keras.models.load_model('best_model.keras')
    print("✓ Model loaded")

    # Load preprocessing artifacts
    with open('outputs/preprocessing_artifacts.pkl', 'rb') as f:
        artifacts = pickle.load(f)
        scaler = artifacts['scaler']
        label_encoders = artifacts['label_encoders']
        target_encoder = artifacts['target_encoder']
        feature_names = artifacts['feature_names']
    print("✓ Preprocessing artifacts loaded")

    # Initialize recommendation engine
    recommendation_engine = InterventionRecommendationEngine()
    print("✓ Recommendation engine initialized")

    # Initialize report generator
    report_generator = ReportGenerator()
    print("✓ Report generator initialized")

    print(f"✓ Ready to predict with {len(feature_names)} features")

def preprocess_student_data(student_data: dict) -> np.ndarray:
    """Preprocess student data for prediction"""

    # Create DataFrame with single row
    df = pd.DataFrame([student_data])

    # Feature engineering (same as training)
    df['study_attendance_interaction'] = df['study_hours_per_week'] * (df['attendance_rate'] / 100)
    df['gpa_difficulty_ratio'] = df['cumulative_gpa'] / (df['avg_course_difficulty'] + 0.1)
    df['engagement_score'] = (df['lms_hours_per_week'] * 0.4 +
                              (df['assignments_on_time'] / 20) * 100 * 0.3 +
                              df['attendance_rate'] * 0.3)
    df['workload_pressure'] = df['study_hours_per_week'] + df['work_hours_per_week'] + df['extracurricular_hours']
    df['resource_access_score'] = df['has_internet_at_home'] + df['has_study_space']
    df['academic_momentum'] = (df['cumulative_gpa'] - df['previous_semester_gpa']) * 10
    df['assignment_completion_rate'] = df['assignments_on_time'] / (df['assignments_submitted'] + 0.1)
    df['lms_efficiency'] = df['lms_hours_per_week'] / (df['lms_logins_per_week'] + 0.1)

    # Encode categorical variables
    for col in label_encoders.keys():
        if col in df.columns:
            # Handle unseen categories
            try:
                df[col] = label_encoders[col].transform(df[col].astype(str))
            except ValueError:
                # Use most common class for unseen categories
                df[col] = 0

    # Ensure all features are present in correct order
    X = df[feature_names]

    # Scale features
    X_scaled = scaler.transform(X)

    return X_scaled

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict risk level for a single student

    Request body: JSON with student features
    Returns: Risk prediction, probabilities, and recommendations
    """
    try:
        # Get student data from request
        student_data = request.json

        if not student_data:
            return jsonify({'error': 'No data provided'}), 400

        # Preprocess data
        X_scaled = preprocess_student_data(student_data)

        # Make prediction
        probabilities = model.predict(X_scaled, verbose=0)[0]
        predicted_class = np.argmax(probabilities)
        risk_level = target_encoder.classes_[predicted_class]

        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            student_data,
            risk_level,
            probabilities
        )

        # Prepare response
        response = {
            'student_id': student_data.get('student_id', 'Unknown'),
            'prediction': {
                'risk_level': risk_level,
                'confidence': float(probabilities[predicted_class]),
                'probabilities': {
                    target_encoder.classes_[i]: float(probabilities[i])
                    for i in range(len(probabilities))
                }
            },
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }

        # Log for educator insights
        _log_prediction(
            student_data,
            risk_level,
            float(probabilities[predicted_class]),
            {target_encoder.classes_[i]: float(probabilities[i]) for i in range(len(probabilities))}
        )

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict risk levels for multiple students

    Request body: JSON array of student data
    Returns: Array of predictions and recommendations
    """
    try:
        # Get batch data from request
        students_data = request.json

        if not students_data or not isinstance(students_data, list):
            return jsonify({'error': 'Expected array of student data'}), 400

        results = []

        for student_data in students_data:
            # Preprocess data
            X_scaled = preprocess_student_data(student_data)

            # Make prediction
            probabilities = model.predict(X_scaled, verbose=0)[0]
            predicted_class = np.argmax(probabilities)
            risk_level = target_encoder.classes_[predicted_class]

            # Generate recommendations
            recommendations = recommendation_engine.generate_recommendations(
                student_data,
                risk_level,
                probabilities
            )

            result_entry = {
                'student_id': student_data.get('student_id', 'Unknown'),
                'risk_level': risk_level,
                'confidence': float(probabilities[predicted_class]),
                'probabilities': {
                    target_encoder.classes_[i]: float(probabilities[i])
                    for i in range(len(probabilities))
                },

                'recommendations': recommendations
            }
            results.append(result_entry)

            # Log each prediction
            _log_prediction(
                student_data,
                risk_level,
                float(probabilities[predicted_class]),
                {target_encoder.classes_[i]: float(probabilities[i]) for i in range(len(probabilities))}
            )

        return jsonify({
            'total_students': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get model statistics and feature importance"""
    try:
        # Load feature importance
        feature_importance = pd.read_csv('outputs/feature_importance.csv')

        return jsonify({
            'model_info': {
                'total_features': len(feature_names),
                'risk_levels': target_encoder.classes_.tolist(),
                'model_type': 'Deep Neural Network'
            },
            'top_features': feature_importance.head(10).to_dict('records'),
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/features', methods=['GET'])
def get_features():
    """Get list of required features for prediction"""
    try:
        # Get original features (before engineering)
        original_features = [f for f in feature_names if f not in [
            'study_attendance_interaction',
            'gpa_difficulty_ratio',
            'engagement_score',
            'workload_pressure',
            'resource_access_score',
            'academic_momentum',
            'assignment_completion_rate',
            'lms_efficiency'
        ]]

        return jsonify({
            'required_features': original_features,
            'total_features': len(original_features),
            'engineered_features': [
                'study_attendance_interaction',
                'gpa_difficulty_ratio',
                'engagement_score',
                'workload_pressure',
                'resource_access_score',
                'academic_momentum',
                'assignment_completion_rate',
                'lms_efficiency'
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sample', methods=['GET'])
def get_sample_data():
    """Get sample student data for testing - returns only the 42 features needed for prediction
    (excludes: student_id, final_grade, letter_grade, risk_level, pass_fail, final_exam_score)
    """
    sample = {
        'student_id': 'SAMPLE_001',  # For display purposes only
        'age': 20,
        'gender': 'Female',
        'socioeconomic_status': 'Middle',
        'parent_education': 'Bachelor',
        'commute_distance': 'Medium',
        'has_internet_at_home': 1,
        'has_study_space': 1,
        'family_support': 'High',
        'previous_semester_gpa': 3.0,
        'previous_year_gpa': 3.1,
        'cumulative_gpa': 3.2,
        'courses_failed_previous': 0,
        'courses_enrolled': 5,
        'credit_hours': 15,
        'avg_course_difficulty': 3.5,
        'major': 'Engineering',
        'year_of_study': 2,
        'has_health_issues': 0,
        'attendance_rate': 85,
        'late_arrivals': 2,
        'total_absences': 3,
        'lms_logins_per_week': 12,
        'lms_hours_per_week': 8,
        'assignments_submitted': 18,
        'assignments_on_time': 15,
        'assignments_late': 3,
        'forum_posts': 5,
        'resources_downloaded': 20,
        'videos_watched': 10,
        'study_hours_per_week': 15,
        'work_hours_per_week': 10,
        'extracurricular_hours': 5,
        'library_visits_per_week': 3,
        'tutoring_sessions_attended': 2,
        'office_hours_visits': 1,
        'study_group_participation': 1,
        'stress_level': 6,
        'motivation_level': 7,
        'avg_sleep_hours': 6.5,
        'midterm_score': 75,
        'quiz_average': 78,
        'assignment_average': 80
        # Note: final_exam_score, final_grade, letter_grade, pass_fail are excluded
        # as they are not available at prediction time
    }

    return jsonify(sample)
@app.route('/predictions/recent', methods=['GET'])
def get_recent_predictions():
    """Return recent predictions from the in-memory log"""
    try:
        limit = int(request.args.get('limit', 25))
        items = list(PREDICTION_LOG)[-limit:][::-1]
        return jsonify({
            'count': len(items),
            'results': items,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/insights', methods=['GET'])
def get_insights():
    """Aggregate educator-facing insights from recent predictions"""
    try:
        logs = list(PREDICTION_LOG)
        total = len(logs)
        risk_counts = Counter([x['risk_level'] for x in logs]) if total else Counter()

        def _avg(key):
            vals = [x[key] for x in logs if isinstance(x.get(key), (int, float))]
            return float(np.mean(vals)) if vals else None

        insights = {
            'predictions_count': total,
            'risk_distribution': [
                {'label': k, 'count': v, 'percent': (v/total if total else 0)}
                for k, v in risk_counts.items()
            ],
            'high_risk_rate': (risk_counts.get('High Risk', 0) / total) if total else 0.0,
            'averages': {
                'attendance_rate': _avg('attendance_rate'),
                'study_hours_per_week': _avg('study_hours_per_week'),
                'lms_hours_per_week': _avg('lms_hours_per_week'),
                'avg_sleep_hours': _avg('avg_sleep_hours'),
                'stress_level': _avg('stress_level'),
                'midterm_score': _avg('midterm_score'),
            },
            'recent_predictions': logs[-10:][::-1],
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/report', methods=['POST'])
def generate_report():
    """Generate HTML report for a student prediction"""
    try:
        # Get prediction result from request
        prediction_result = request.json

        if not prediction_result:
            return jsonify({'error': 'No prediction data provided'}), 400

        # Generate HTML report
        html_content = report_generator.generate_html_report(prediction_result)

        # Save report to file
        student_id = prediction_result.get('student_id', 'unknown')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'reports/student_{student_id}_{timestamp}.html'

        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Report generated successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/report/download/<path:filename>', methods=['GET'])
def download_report(filename):
    """Download a generated report"""
    try:
        filepath = os.path.join('reports', filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'Report not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load model and artifacts on startup
    load_model_and_artifacts()

    # Run server
    print("\n" + "="*80)
    print("ACADEMIC PERFORMANCE PREDICTION API SERVER")
    print("="*80)
    print("\nEndpoints:")
    print("  GET  /health                    - Health check")
    print("  POST /predict                   - Single student prediction")
    print("  POST /predict/batch             - Batch predictions")
    print("  GET  /predictions/recent        - Recent predictions")
    print("  GET  /insights                  - Aggregated educator insights")
    print("  GET  /stats                     - Model statistics")
    print("  GET  /features                  - Required features list")
    print("  GET  /sample                    - Sample student data")
    print("  POST /report                    - Generate HTML report")
    print("  GET  /report/download/<file>    - Download report")
    print("\nStarting server on http://localhost:5000")
    print("="*80 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
