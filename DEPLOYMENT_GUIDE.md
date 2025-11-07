# Academic Performance Prediction System - Deployment Guide

## 🎯 Complete End-to-End System

This system provides AI-powered student risk assessment with personalized intervention recommendations through a modern web interface.

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + TypeScript)             │
│  - Single Student Prediction Dashboard                      │
│  - Batch Prediction Interface                               │
│  - Model Statistics & Visualizations                        │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────────────────┐
│                    BACKEND (Flask API)                       │
│  - /predict - Single student prediction                     │
│  - /predict/batch - Batch predictions                       │
│  - /stats - Model statistics                                │
│  - /features - Feature information                          │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              MACHINE LEARNING PIPELINE                       │
│  - Deep Neural Network (TensorFlow/Keras)                   │
│  - SHAP Interpretability Analysis                           │
│  - Recommendation Engine                                    │
│  - Report Generator                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Start the Backend API

```bash
# Navigate to project directory
cd "c:\Users\shlok\Downloads\DL final"

# Start the Flask API server
python api_server.py
```

The API will start on `http://localhost:5000`

### Step 2: Start the Frontend

```bash
# Open a new terminal
cd "c:\Users\shlok\Downloads\DL final\frontend"

# Start the React development server
npm start
```

The dashboard will open automatically at `http://localhost:3000`

### Step 3: Use the System

1. **Single Student Prediction**:
   - Click "Load Sample" to populate with sample data
   - Modify values as needed
   - Click "Predict Risk Level"
   - View risk assessment and intervention recommendations

2. **Batch Predictions**:
   - Prepare a JSON file with student data
   - Upload via the Batch Predictions tab
   - Download results as CSV

3. **View Model Statistics**:
   - Check the Model Statistics tab
   - See feature importance rankings
   - View model performance metrics

---

## 📦 System Components

### 1. **Trained Model**
- **File**: `best_model.keras`
- **Type**: Deep Neural Network (4 layers: 256→128→64→32)
- **Performance**: 92.92% test accuracy, 98.86% ROC-AUC
- **Features**: 50 input features (42 original + 8 engineered)

### 2. **Backend API** (`api_server.py`)
- **Framework**: Flask with CORS enabled
- **Endpoints**:
  - `GET /health` - Health check
  - `POST /predict` - Single prediction
  - `POST /predict/batch` - Batch predictions
  - `GET /stats` - Model statistics
  - `GET /features` - Feature list
  - `GET /sample` - Sample data

### 3. **Recommendation Engine** (`recommendation_engine.py`)
- Generates personalized interventions based on:
  - Risk level (High/Medium/Low)
  - Top contributing factors from SHAP analysis
  - Student profile characteristics
- Provides:
  - Priority interventions
  - Supporting interventions
  - Structured action plans
  - Follow-up timelines

### 4. **Report Generator** (`report_generator.py`)
- Creates HTML reports for individual students
- Generates batch summary reports
- Includes:
  - Risk assessment details
  - Intervention recommendations
  - Action plans
  - Follow-up schedules

### 5. **Frontend Dashboard** (`frontend/`)
- **Framework**: React 18 + TypeScript
- **UI Library**: Material-UI (MUI)
- **Charts**: Recharts
- **Features**:
  - Responsive design
  - Real-time predictions
  - Interactive visualizations
  - Batch processing
  - CSV export

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Install Python dependencies
pip install tensorflow pandas numpy scikit-learn matplotlib seaborn shap flask flask-cors

# Verify model and artifacts exist
ls best_model.keras
ls outputs/preprocessing_artifacts.pkl
ls outputs/feature_importance.csv
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Dependencies installed:
# - react, react-dom
# - @mui/material, @mui/icons-material
# - axios
# - recharts
# - typescript
```

---

## 📊 Model Performance

### Training Results
- **Dataset**: 100,000 student records
- **Train/Val/Test Split**: 70% / 15% / 15%
- **Training Time**: ~12 minutes (CPU)
- **Best Epoch**: 93/100

### Performance Metrics
| Metric | Value |
|--------|-------|
| Test Accuracy | 92.92% |
| Precision | 93.00% |
| Recall | 92.92% |
| F1-Score | 92.90% |
| ROC-AUC (Weighted) | 98.86% |
| ROC-AUC (Macro) | 99.08% |

### Per-Class Performance
| Risk Level | Precision | Recall | F1-Score | Support |
|------------|-----------|--------|----------|---------|
| High Risk | 92.33% | 87.49% | 89.84% | 2,174 |
| Low Risk | 95.76% | 90.78% | 93.20% | 4,771 |
| Medium Risk | 91.54% | 95.65% | 93.55% | 8,055 |

### Top 10 Most Important Features
1. midterm_score (0.1228)
2. lms_hours_per_week (0.0969)
3. total_absences (0.0699)
4. stress_level (0.0658)
5. engagement_score (0.0638)
6. avg_sleep_hours (0.0584)
7. assignments_on_time (0.0556)
8. attendance_rate (0.0534)
9. lms_efficiency (0.0433)
10. assignments_submitted (0.0392)

---

## 📁 Project Structure

```
DL final/
├── academic_performance_dataset.csv    # Training dataset (100K records)
├── best_model.keras                    # Trained model
├── train_model.py                      # Model training pipeline
├── complete_shap_analysis_v2.py        # SHAP analysis script
├── api_server.py                       # Flask API server
├── recommendation_engine.py            # Intervention recommendation system
├── report_generator.py                 # HTML/PDF report generator
├── outputs/                            # Model outputs
│   ├── preprocessing_artifacts.pkl     # Scaler, encoders, feature names
│   ├── feature_importance.csv          # SHAP feature rankings
│   ├── confusion_matrix.png            # Confusion matrix visualization
│   ├── training_history.png            # Training curves
│   ├── roc_curves.png                  # ROC curves
│   ├── class_distribution.png          # Class distribution
│   ├── shap_summary_High_Risk.png      # SHAP for High Risk
│   ├── shap_summary_Medium_Risk.png    # SHAP for Medium Risk
│   ├── shap_summary_Low_Risk.png       # SHAP for Low Risk
│   └── shap_global_importance.png      # Global feature importance
├── frontend/                           # React frontend
│   ├── src/
│   │   ├── App.tsx                     # Main app component
│   │   ├── components/
│   │   │   ├── PredictionDashboard.tsx # Single prediction UI
│   │   │   ├── BatchPrediction.tsx     # Batch prediction UI
│   │   │   └── ModelStats.tsx          # Statistics dashboard
│   │   └── ...
│   ├── package.json
│   └── ...
└── reports/                            # Generated reports (auto-created)
```

---

## 🎓 Usage Examples

### Example 1: Single Student Prediction

```python
import requests

student_data = {
    'student_id': 'STU001',
    'age': 20,
    'cumulative_gpa': 2.8,
    'midterm_score': 65,
    'attendance_rate': 75,
    'study_hours_per_week': 10,
    'stress_level': 8,
    # ... other features
}

response = requests.post('http://localhost:5000/predict', json=student_data)
result = response.json()

print(f"Risk Level: {result['prediction']['risk_level']}")
print(f"Confidence: {result['prediction']['confidence']:.2%}")
```

### Example 2: Batch Prediction

```python
import requests
import json

# Load student data
with open('students.json', 'r') as f:
    students = json.load(f)

response = requests.post('http://localhost:5000/predict/batch', json=students)
results = response.json()

print(f"Processed {results['total_students']} students")
for student in results['results']:
    print(f"{student['student_id']}: {student['risk_level']}")
```

### Example 3: Generate Report

```python
from report_generator import ReportGenerator

generator = ReportGenerator()

# Get prediction result
response = requests.post('http://localhost:5000/predict', json=student_data)
result = response.json()

# Generate HTML report
filename = generator.save_html_report(result)
print(f"Report saved to: {filename}")
```

---

## 🔒 Security Considerations

1. **API Security**: Currently no authentication - add JWT tokens for production
2. **CORS**: Enabled for development - restrict origins in production
3. **Input Validation**: Add comprehensive validation for all inputs
4. **Rate Limiting**: Implement rate limiting to prevent abuse
5. **HTTPS**: Use HTTPS in production deployment

---

## 🚢 Production Deployment

### Option 1: Docker Deployment

```dockerfile
# Dockerfile for backend
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "api_server.py"]
```

### Option 2: Cloud Deployment

**Backend (Heroku/AWS/Azure)**:
- Deploy Flask API as a web service
- Use gunicorn for production server
- Set environment variables for configuration

**Frontend (Vercel/Netlify)**:
- Build React app: `npm run build`
- Deploy build folder
- Configure API endpoint

---

## 📞 Support & Troubleshooting

### Common Issues

1. **API not starting**: Check if port 5000 is available
2. **Frontend can't connect**: Verify API is running on localhost:5000
3. **Model loading error**: Ensure `best_model.keras` and `outputs/` exist
4. **SHAP errors**: Reinstall shap: `pip install shap --upgrade`

---

## 📄 License

This project is for educational purposes as part of a Deep Learning course project.

---

## 👥 Contributors

Deep Learning Final Project - Academic Performance Prediction System

**Date**: November 2025

