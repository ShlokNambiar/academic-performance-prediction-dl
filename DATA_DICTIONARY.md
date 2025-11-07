# Academic Performance Dataset - Data Dictionary

## Overview
This synthetic dataset contains **100,000 student records** with **48 features** designed for predictive analytics on academic performance and intervention strategy development.

## Dataset Statistics
- **Total Students**: 100,000
- **Total Features**: 48
- **Risk Distribution**:
  - Low Risk: 31,806 (31.8%)
  - Medium Risk: 53,699 (53.7%)
  - High Risk: 14,495 (14.5%)
- **Pass Rate**: 93.3% (93,257 pass, 6,743 fail)
- **Average Final Grade**: 82.18/100
- **Average GPA**: 3.16/4.0
- **Average Attendance**: 82.15%

---

## Feature Categories

### 1. Student Identification
| Feature | Type | Description | Values/Range |
|---------|------|-------------|--------------|
| `student_id` | String | Unique student identifier | STU00001 - STU05000 |

### 2. Demographics (8 features)
| Feature | Type | Description | Values/Range | Impact on Performance |
|---------|------|-------------|--------------|----------------------|
| `age` | Integer | Student age | 16-25 years | Minimal direct impact |
| `gender` | Categorical | Gender identity | Male, Female, Non-binary | No systematic bias |
| `socioeconomic_status` | Categorical | Family economic status | Low, Medium, High | **High impact**: +0.4 GPA for High, -0.3 for Low |
| `parent_education` | Categorical | Highest parent education | None, High School, Associate, Bachelor, Master, PhD | **High impact**: +0.4 GPA for PhD, -0.4 for None |
| `commute_distance` | Categorical | Distance from home to campus | <5km, 5-10km, 10-20km, >20km | **Medium impact**: Affects attendance (-12% for >20km) |
| `has_internet_at_home` | Binary | Internet access at home | 0 (No), 1 (Yes) | **Medium impact**: +0.2 GPA |
| `has_study_space` | Binary | Dedicated study space | 0 (No), 1 (Yes) | **Medium impact**: +0.15 GPA |
| `family_support` | Categorical | Level of family support | Low, Medium, High | **Medium impact**: Correlates with motivation |

### 3. Academic History (5 features)
| Feature | Type | Description | Values/Range | Predictive Power |
|---------|------|-------------|--------------|------------------|
| `previous_semester_gpa` | Float | GPA from last semester | 0.0 - 4.0 | **Very High**: Strong predictor of current performance |
| `previous_year_gpa` | Float | GPA from previous year | 0.0 - 4.0 | **Very High**: Indicates long-term trends |
| `cumulative_gpa` | Float | Overall GPA to date | 0.0 - 4.0 | **Very High**: Best single predictor |
| `courses_failed_previous` | Integer | Number of previously failed courses | 0-3 | **High**: Indicates academic struggles |

### 4. Current Semester Enrollment (5 features)
| Feature | Type | Description | Values/Range | Notes |
|---------|------|-------------|--------------|-------|
| `courses_enrolled` | Integer | Number of courses | 3-6 courses | Full-time typically 4-6 |
| `credit_hours` | Integer | Total credit hours | 9-24 hours | Affects workload and stress |
| `avg_course_difficulty` | Integer | Average difficulty rating | 1-5 (1=Easy, 5=Hard) | Impacts performance expectations |
| `major` | Categorical | Field of study | STEM, Business, Arts, Social Sciences, Health Sciences | Different performance patterns |
| `year_of_study` | Integer | Academic year | 1-4 (Freshman-Senior) | Experience level |

### 5. Attendance Metrics (4 features)
| Feature | Type | Description | Values/Range | Predictive Power |
|---------|------|-------------|--------------|------------------|
| `attendance_rate` | Float | Percentage of classes attended | 0-100% | **Very High**: Strong correlation with grades |
| `late_arrivals` | Integer | Number of late arrivals | 0-50 | **Medium**: Indicates engagement issues |
| `total_absences` | Integer | Total classes missed | 0-60 | **High**: Direct impact on learning |
| `has_health_issues` | Binary | Chronic health problems | 0 (No), 1 (Yes) | Explains some absences |

### 6. LMS (Learning Management System) Activity (9 features)
| Feature | Type | Description | Values/Range | Predictive Power |
|---------|------|-------------|--------------|------------------|
| `lms_logins_per_week` | Integer | Weekly LMS logins | 0-50 | **High**: Indicates engagement |
| `lms_hours_per_week` | Float | Hours spent on LMS weekly | 0-40 hours | **Very High**: Active learning indicator |
| `assignments_submitted` | Integer | Total assignments submitted | 0-20 | **Very High**: Completion is critical |
| `assignments_on_time` | Integer | On-time submissions | 0-20 | **Very High**: Time management indicator |
| `assignments_late` | Integer | Late submissions | 0-20 | **Medium**: Better late than never |
| `forum_posts` | Integer | Discussion forum posts | 0-100+ | **Medium**: Engagement and collaboration |
| `resources_downloaded` | Integer | Course materials downloaded | 0-100+ | **Medium**: Preparation indicator |
| `videos_watched` | Integer | Lecture videos viewed | 0-40 | **High**: Content consumption |

### 7. Behavioral & Engagement (11 features)
| Feature | Type | Description | Values/Range | Predictive Power |
|---------|------|-------------|--------------|------------------|
| `study_hours_per_week` | Float | Self-study hours weekly | 0-60 hours | **Very High**: Direct impact on mastery |
| `work_hours_per_week` | Integer | Part-time work hours | 0, 10, 20, 30, 40 | **Medium**: Competes with study time |
| `extracurricular_hours` | Integer | Extracurricular activities | 0, 2, 5, 10 hours | **Low**: Balanced involvement is positive |
| `library_visits_per_week` | Integer | Library visits weekly | 0-20 | **Medium**: Study environment quality |
| `tutoring_sessions_attended` | Integer | Tutoring sessions | 0-15 | **High**: Seeking help is positive |
| `office_hours_visits` | Integer | Professor office hours | 0-15 | **High**: Proactive engagement |
| `study_group_participation` | Binary | Participates in study groups | 0 (No), 1 (Yes) | **Medium**: Peer learning benefit |
| `stress_level` | Integer | Self-reported stress | 1-5 (1=Low, 5=High) | **Medium**: High stress hurts performance |
| `motivation_level` | Integer | Self-reported motivation | 1-5 (1=Low, 5=High) | **High**: Drives effort and persistence |
| `avg_sleep_hours` | Float | Average sleep per night | 3-10 hours | **Medium**: Cognitive function impact |

### 8. Assessment Scores (4 features)
| Feature | Type | Description | Values/Range | Predictive Power |
|---------|------|-------------|--------------|------------------|
| `midterm_score` | Float | Midterm exam score | 0-100% | **Very High**: Early performance indicator |
| `quiz_average` | Float | Average quiz score | 0-100% | **High**: Consistent assessment |
| `assignment_average` | Float | Average assignment score | 0-100% | **High**: Work quality indicator |
| `final_exam_score` | Float | Final exam score | 0-100% | **Target**: Part of final grade calculation |

### 9. Target Variables (4 features)
| Feature | Type | Description | Values/Range | Use Case |
|---------|------|-------------|--------------|----------|
| `final_grade` | Float | Overall course grade | 0-100% | **Primary Target**: Regression |
| `letter_grade` | Categorical | Letter grade | A, B, C, D, F | **Classification Target** |
| `risk_level` | Categorical | Intervention risk level | Low Risk, Medium Risk, High Risk | **Primary Target**: Intervention prediction |
| `pass_fail` | Categorical | Pass/fail status | Pass (≥60%), Fail (<60%) | **Binary Classification Target** |

---

## Target Variable Details

### Risk Level Calculation
The `risk_level` is calculated using a scoring system:

**Academic Risk Factors:**
- Midterm score < 60: +3 points
- Midterm score 60-70: +2 points
- Midterm score 70-80: +1 point
- Attendance < 70%: +3 points
- Attendance 70-80%: +2 points
- Attendance 80-90%: +1 point
- On-time assignments < 12: +2 points
- On-time assignments 12-16: +1 point

**Behavioral Risk Factors:**
- LMS hours < 5/week: +2 points
- Study hours < 10/week: +2 points
- Stress level ≥ 4: +1 point
- Sleep < 6 hours: +1 point

**Risk Classification:**
- **High Risk**: Score ≥ 8 (14.5% of students - 14,495 students)
- **Medium Risk**: Score 4-7 (53.7% of students - 53,699 students)
- **Low Risk**: Score < 4 (31.8% of students - 31,806 students)

### Final Grade Calculation
Weighted average of:
- Midterm: 25%
- Quizzes: 15%
- Assignments: 20%
- Attendance: 10%
- Final Exam: 30%

---

## Data Correlations & Patterns

### Strong Positive Correlations with Performance:
1. **Cumulative GPA** (r ≈ 0.85): Best historical predictor
2. **Study hours per week** (r ≈ 0.65): Direct effort impact
3. **Attendance rate** (r ≈ 0.70): Engagement and exposure
4. **LMS hours per week** (r ≈ 0.60): Active learning
5. **Assignments on time** (r ≈ 0.75): Discipline and understanding
6. **Midterm score** (r ≈ 0.80): Early performance indicator

### Negative Correlations with Performance:
1. **Stress level** (r ≈ -0.35): Cognitive interference
2. **Work hours** (r ≈ -0.25): Time competition
3. **Commute distance** (r ≈ -0.20): Indirect through attendance
4. **Courses failed previously** (r ≈ -0.55): Cumulative struggles

### Socioeconomic Factors:
- **Parent education**: +0.4 GPA difference (PhD vs None)
- **Socioeconomic status**: +0.7 GPA difference (High vs Low)
- **Internet access**: +0.2 GPA on average
- **Study space**: +0.15 GPA on average

---

## Recommended Interventions by Risk Level

### High Risk Students (Score ≥ 8)
**Characteristics:**
- Midterm score < 60%
- Attendance < 70%
- Minimal LMS engagement
- Poor assignment completion

**Recommended Interventions:**
1. **Mandatory academic counseling** (weekly)
2. **Tutoring program enrollment** (2-3 sessions/week)
3. **Study skills workshop** (time management, note-taking)
4. **Attendance monitoring** with follow-up
5. **Reduced course load** consideration
6. **Mental health screening** and support
7. **Peer mentoring** assignment
8. **Financial aid review** (if applicable)

### Medium Risk Students (Score 4-7)
**Characteristics:**
- Midterm score 60-75%
- Attendance 70-85%
- Moderate engagement
- Some late assignments

**Recommended Interventions:**
1. **Academic advisor check-in** (bi-weekly)
2. **Optional tutoring** availability
3. **Study group formation** encouragement
4. **Time management resources**
5. **Office hours** encouragement
6. **LMS engagement** monitoring
7. **Stress management** resources

### Low Risk Students (Score < 4)
**Characteristics:**
- Midterm score > 75%
- Attendance > 85%
- High engagement
- Consistent performance

**Recommended Support:**
1. **Enrichment opportunities** (research, advanced courses)
2. **Peer tutoring** opportunities (as tutors)
3. **Leadership roles** in study groups
4. **Maintain engagement** monitoring
5. **Career development** resources

---

## Usage Recommendations

### For Model Training:
1. **Train/Test Split**: 80/20 or 70/30
2. **Stratify by**: `risk_level` or `letter_grade` to maintain distribution
3. **Feature Engineering**: Consider interaction terms (e.g., study_hours × attendance_rate)
4. **Temporal Split**: Use midterm data to predict final outcomes

### For Intervention Prediction:
1. **Primary Target**: `risk_level` (3-class classification)
2. **Early Prediction**: Use features available by week 6-8 (before midterm)
3. **Mid-semester Prediction**: Include midterm scores for refinement
4. **Feature Importance**: Use SHAP/LIME for interpretability

### For Performance Prediction:
1. **Regression Target**: `final_grade` (continuous)
2. **Classification Target**: `letter_grade` or `pass_fail`
3. **Multi-task Learning**: Predict both grade and risk level simultaneously

### Evaluation Metrics:
- **Classification**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Regression**: MAE, RMSE, R²
- **Intervention Focus**: Prioritize **Recall for High Risk** (don't miss at-risk students)
- **Interpretability**: SHAP values, feature importance, decision rules

---

## Data Quality Notes

### Realistic Correlations:
- All features have realistic correlations based on educational research
- Socioeconomic factors appropriately influence outcomes
- Behavioral patterns reflect real student challenges
- No perfect predictors (noise included for realism)

### Diversity:
- Balanced gender distribution
- Varied socioeconomic backgrounds
- Multiple majors and difficulty levels
- Range of engagement patterns

### Limitations:
- Synthetic data may not capture all real-world complexities
- Correlations are modeled, not observed
- Some rare edge cases may be underrepresented
- Cultural and institutional factors are simplified

---

## File Information
- **Filename**: `academic_performance_dataset.csv`
- **Format**: CSV (Comma-Separated Values)
- **Encoding**: UTF-8
- **Size**: 100,000 rows × 48 columns (~25 MB)
- **Missing Values**: None (complete dataset)

---

## Citation
If using this dataset, please cite:
```
Synthetic Academic Performance Dataset for Predictive Analytics
Generated: 2025
Purpose: Educational intervention and performance prediction
Features: 48 variables across demographics, academics, behavior, and outcomes
Students: 100,000 synthetic records
```

---

## Contact & Support
For questions about feature definitions, data generation methodology, or usage recommendations, refer to the generation script: `generate_academic_dataset.py`
