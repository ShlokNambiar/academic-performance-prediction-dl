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
  Stack
} from '@mui/material';
import PredictIcon from '@mui/icons-material/Psychology';

const API_URL = 'http://localhost:5000';

const SimplePrediction: React.FC = () => {
  const [studentId, setStudentId] = useState('STU001');
  const [gpa, setGpa] = useState('3.5');
  const [attendance, setAttendance] = useState('85');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handlePredict = async () => {
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.get(`${API_URL}/sample`);
      const sampleData = response.data;

      // Override with user inputs
      sampleData.student_id = studentId;
      sampleData.cumulative_gpa = parseFloat(gpa);
      sampleData.attendance_rate = parseFloat(attendance);

      const predResponse = await axios.post(`${API_URL}/predict`, sampleData);
      setResult(predResponse.data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to get prediction');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'High Risk': return 'error';
      case 'Medium Risk': return 'warning';
      case 'Low Risk': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Student Risk Prediction
      </Typography>

      <Stack spacing={3}>
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Student Information
          </Typography>

          <Stack spacing={2}>
            <TextField
              fullWidth
              label="Student ID"
              value={studentId}
              onChange={(e) => setStudentId(e.target.value)}
            />

            <TextField
              fullWidth
              label="Cumulative GPA"
              type="number"
              value={gpa}
              onChange={(e) => setGpa(e.target.value)}
              inputProps={{ min: 0, max: 4, step: 0.1 }}
            />

            <TextField
              fullWidth
              label="Attendance Rate (%)"
              type="number"
              value={attendance}
              onChange={(e) => setAttendance(e.target.value)}
              inputProps={{ min: 0, max: 100 }}
            />

            <Button
              variant="contained"
              size="large"
              startIcon={loading ? <CircularProgress size={20} /> : <PredictIcon />}
              onClick={handlePredict}
              disabled={loading}
            >
              {loading ? 'Predicting...' : 'Predict Risk Level'}
            </Button>
          </Stack>
        </Paper>

        {error && (
          <Alert severity="error">{error}</Alert>
        )}

        {result && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Prediction Results
            </Typography>

            <Stack spacing={2}>
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Risk Level
                </Typography>
                <Chip
                  label={result.prediction}
                  color={getRiskColor(result.prediction) as any}
                  sx={{ mt: 1, fontSize: '1.2rem', padding: '20px 10px' }}
                />
              </Box>

              <Box>
                <Typography variant="body2" color="text.secondary">
                  Confidence
                </Typography>
                <Typography variant="h6">
                  {(result.confidence * 100).toFixed(1)}%
                </Typography>
              </Box>

              {result.recommendations && result.recommendations.priority_interventions && (
                <Box>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Top Recommendations
                  </Typography>
                  {result.recommendations.priority_interventions.slice(0, 3).map((rec: any, idx: number) => (
                    <Alert key={idx} severity="info" sx={{ mt: 1 }}>
                      <Typography variant="body2">
                        <strong>{rec.category}:</strong> {rec.strategy}
                      </Typography>
                    </Alert>
                  ))}
                </Box>
              )}
            </Stack>
          </Paper>
        )}
      </Stack>
    </Box>
  );
};

export default SimplePrediction;
