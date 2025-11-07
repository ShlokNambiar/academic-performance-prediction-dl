import React, { useState } from 'react';
import axios from 'axios';
import {
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Chip,
  Divider,
  MenuItem,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText
} from '@mui/material';
import PredictIcon from '@mui/icons-material/Psychology';

const API_URL = 'http://localhost:5000';

interface PredictionResult {
  student_id: string;
  prediction: {
    risk_level: string;
    confidence: number;
    probabilities: { [key: string]: number };
  };
  recommendations: {
    risk_level: string;
    priority_interventions: Array<{
      title: string;
      priority: string;
      interventions: string[];
    }>;
  };
  timestamp: string;
}

const ComprehensivePrediction: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [formData, setFormData] = useState({
    student_id: 'STU001',
    age: '20',
    gender: 'Male',
    socioeconomic_status: 'Middle',
    parent_education: 'Bachelor',
    commute_distance: 'Medium',
    has_internet_at_home: '1',
    has_study_space: '1',
    family_support: 'High',
    previous_semester_gpa: '3.2',
    cumulative_gpa: '3.3',
    year_of_study: '2',
    major: 'Engineering',
    attendance_rate: '85',
    study_hours_per_week: '15',
    work_hours_per_week: '10',
    lms_hours_per_week: '5',
    assignments_on_time: '8',
    stress_level: '5',
    avg_sleep_hours: '7',
    midterm_score: '75'
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLoadSample = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_URL}/sample`);

      // Map sample data to form fields
      const sample = response.data;
      setFormData({
        student_id: sample.student_id || 'STU001',
        age: String(sample.age || 20),
        gender: sample.gender || 'Male',
        socioeconomic_status: sample.socioeconomic_status || 'Middle',
        parent_education: sample.parent_education || 'Bachelor',
        commute_distance: sample.commute_distance || 'Medium',
        has_internet_at_home: String(sample.has_internet_at_home || 1),
        has_study_space: String(sample.has_study_space || 1),
        family_support: sample.family_support || 'High',
        previous_semester_gpa: String(sample.previous_semester_gpa || 3.2),
        cumulative_gpa: String(sample.cumulative_gpa || 3.3),
        year_of_study: String(sample.year_of_study || 2),
        major: sample.major || 'Engineering',
        attendance_rate: String(sample.attendance_rate || 85),
        study_hours_per_week: String(sample.study_hours_per_week || 15),
        work_hours_per_week: String(sample.work_hours_per_week || 10),
        lms_hours_per_week: String(sample.lms_hours_per_week || 5),
        assignments_on_time: String(sample.assignments_on_time || 8),
        stress_level: String(sample.stress_level || 5),
        avg_sleep_hours: String(sample.avg_sleep_hours || 7),
        midterm_score: String(sample.midterm_score || 75)
      });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load sample data');
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async () => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);

      // First get sample data to fill in missing fields
      const sampleResponse = await axios.get(`${API_URL}/sample`);
      const sampleData = sampleResponse.data;

      // Override with user inputs
      const predictionData = {
        ...sampleData,
        student_id: formData.student_id,
        age: parseFloat(formData.age),
        gender: formData.gender,
        socioeconomic_status: formData.socioeconomic_status,
        parent_education: formData.parent_education,
        commute_distance: formData.commute_distance,
        has_internet_at_home: parseInt(formData.has_internet_at_home),
        has_study_space: parseInt(formData.has_study_space),
        family_support: formData.family_support,
        previous_semester_gpa: parseFloat(formData.previous_semester_gpa),
        cumulative_gpa: parseFloat(formData.cumulative_gpa),
        year_of_study: parseInt(formData.year_of_study),
        major: formData.major,
        attendance_rate: parseFloat(formData.attendance_rate),
        study_hours_per_week: parseFloat(formData.study_hours_per_week),
        work_hours_per_week: parseFloat(formData.work_hours_per_week),
        lms_hours_per_week: parseFloat(formData.lms_hours_per_week),
        assignments_on_time: parseInt(formData.assignments_on_time),
        stress_level: parseInt(formData.stress_level),
        avg_sleep_hours: parseFloat(formData.avg_sleep_hours),
        midterm_score: parseFloat(formData.midterm_score)
      };

      const response = await axios.post(`${API_URL}/predict`, predictionData);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string): 'error' | 'warning' | 'success' => {
    if (risk === 'High Risk') return 'error';
    if (risk === 'Medium Risk') return 'warning';
    return 'success';
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5">Student Risk Assessment</Typography>
          <Button variant="outlined" onClick={handleLoadSample} disabled={loading}>
            Load Sample Data
          </Button>
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 2 }}>
          {/* Demographics */}
          <TextField
            fullWidth
            label="Student ID"
            name="student_id"
            value={formData.student_id}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Age"
            name="age"
            type="number"
            value={formData.age}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            select
            label="Gender"
            name="gender"
            value={formData.gender}
            onChange={handleInputChange}
          >
            <MenuItem value="Male">Male</MenuItem>
            <MenuItem value="Female">Female</MenuItem>
            <MenuItem value="Other">Other</MenuItem>
          </TextField>

          {/* Socioeconomic */}
          <TextField
            fullWidth
            select
            label="Socioeconomic Status"
            name="socioeconomic_status"
            value={formData.socioeconomic_status}
            onChange={handleInputChange}
          >
            <MenuItem value="Low">Low</MenuItem>
            <MenuItem value="Middle">Middle</MenuItem>
            <MenuItem value="High">High</MenuItem>
          </TextField>
          <TextField
            fullWidth
            select
            label="Parent Education"
            name="parent_education"
            value={formData.parent_education}
            onChange={handleInputChange}
          >
            <MenuItem value="High School">High School</MenuItem>
            <MenuItem value="Associate">Associate</MenuItem>
            <MenuItem value="Bachelor">Bachelor</MenuItem>
            <MenuItem value="Master">Master</MenuItem>
            <MenuItem value="PhD">PhD</MenuItem>
            <MenuItem value="None">None</MenuItem>
          </TextField>
          <TextField
            fullWidth
            select
            label="Commute Distance"
            name="commute_distance"
            value={formData.commute_distance}
            onChange={handleInputChange}
          >
            <MenuItem value="Short">Short</MenuItem>
            <MenuItem value="Medium">Medium</MenuItem>
            <MenuItem value="Long">Long</MenuItem>
            <MenuItem value="Very Long">Very Long</MenuItem>
          </TextField>

          {/* Resources */}
          <TextField
            fullWidth
            select
            label="Internet at Home"
            name="has_internet_at_home"
            value={formData.has_internet_at_home}
            onChange={handleInputChange}
          >
            <MenuItem value="1">Yes</MenuItem>
            <MenuItem value="0">No</MenuItem>
          </TextField>
          <TextField
            fullWidth
            select
            label="Study Space"
            name="has_study_space"
            value={formData.has_study_space}
            onChange={handleInputChange}
          >
            <MenuItem value="1">Yes</MenuItem>
            <MenuItem value="0">No</MenuItem>
          </TextField>
          <TextField
            fullWidth
            select
            label="Family Support"
            name="family_support"
            value={formData.family_support}
            onChange={handleInputChange}
          >
            <MenuItem value="Low">Low</MenuItem>
            <MenuItem value="Medium">Medium</MenuItem>
            <MenuItem value="High">High</MenuItem>
          </TextField>

          {/* Academic Performance */}
          <TextField
            fullWidth
            label="Previous Semester GPA"
            name="previous_semester_gpa"
            type="number"
            inputProps={{ step: 0.1, min: 0, max: 4 }}
            value={formData.previous_semester_gpa}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Cumulative GPA"
            name="cumulative_gpa"
            type="number"
            inputProps={{ step: 0.1, min: 0, max: 4 }}
            value={formData.cumulative_gpa}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Year of Study"
            name="year_of_study"
            type="number"
            inputProps={{ min: 1, max: 6 }}
            value={formData.year_of_study}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            select
            label="Major"
            name="major"
            value={formData.major}
            onChange={handleInputChange}
          >
            <MenuItem value="Engineering">Engineering</MenuItem>
            <MenuItem value="Business">Business</MenuItem>
            <MenuItem value="Science">Science</MenuItem>
            <MenuItem value="Arts">Arts</MenuItem>
            <MenuItem value="Other">Other</MenuItem>
          </TextField>

          {/* Attendance & Engagement */}
          <TextField
            fullWidth
            label="Attendance Rate (%)"
            name="attendance_rate"
            type="number"
            inputProps={{ min: 0, max: 100 }}
            value={formData.attendance_rate}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Study Hours/Week"
            name="study_hours_per_week"
            type="number"
            inputProps={{ min: 0 }}
            value={formData.study_hours_per_week}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Work Hours/Week"
            name="work_hours_per_week"
            type="number"
            inputProps={{ min: 0 }}
            value={formData.work_hours_per_week}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="LMS Hours/Week"
            name="lms_hours_per_week"
            type="number"
            inputProps={{ min: 0 }}
            value={formData.lms_hours_per_week}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Assignments On Time"
            name="assignments_on_time"
            type="number"
            inputProps={{ min: 0 }}
            value={formData.assignments_on_time}
            onChange={handleInputChange}
          />

          {/* Wellbeing */}
          <TextField
            fullWidth
            label="Stress Level (1-10)"
            name="stress_level"
            type="number"
            inputProps={{ min: 1, max: 10 }}
            value={formData.stress_level}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Sleep Hours/Day"
            name="avg_sleep_hours"
            type="number"
            inputProps={{ step: 0.5, min: 0, max: 24 }}
            value={formData.avg_sleep_hours}
            onChange={handleInputChange}
          />
          <TextField
            fullWidth
            label="Midterm Score"
            name="midterm_score"
            type="number"
            inputProps={{ min: 0, max: 100 }}
            value={formData.midterm_score}
            onChange={handleInputChange}
          />
        </Box>

        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<PredictIcon />}
            onClick={handlePredict}
            disabled={loading}
            fullWidth
          >
            {loading ? <CircularProgress size={24} /> : 'Predict Risk Level'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {result && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Prediction Results
          </Typography>

          <Box sx={{ mb: 3 }}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Risk Level
            </Typography>
            <Chip
              label={result.prediction.risk_level}
              color={getRiskColor(result.prediction.risk_level)}
              sx={{ fontSize: '1.2rem', padding: '20px 10px' }}
            />
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Confidence: {(result.prediction.confidence * 100).toFixed(1)}%
            </Typography>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Typography variant="h6" gutterBottom>
            Recommended Interventions
          </Typography>

          {result.recommendations && result.recommendations.priority_interventions && result.recommendations.priority_interventions.length > 0 ? (
            result.recommendations.priority_interventions.map((rec, index) => (
              <Card key={index} sx={{ mb: 2 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="subtitle1" fontWeight="bold">
                      {rec.title}
                    </Typography>
                    <Chip
                      label={rec.priority}
                      size="small"
                      color={
                        rec.priority === 'CRITICAL' ? 'error' :
                        rec.priority === 'HIGH' ? 'warning' : 'info'
                      }
                    />
                  </Box>
                  <List dense>
                    {rec.interventions.map((action, idx) => (
                      <ListItem key={idx}>
                        <ListItemText primary={`• ${action}`} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            ))
          ) : (
            <Alert severity="success">
              No interventions needed - student is performing well!
            </Alert>
          )}
        </Paper>
      )}
    </Box>
  );
};

export default ComprehensivePrediction;
