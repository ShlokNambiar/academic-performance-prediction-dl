import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Stack,
  Divider
} from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import PsychologyIcon from '@mui/icons-material/Psychology';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

const API_URL = 'http://localhost:5000';

const COLORS = ['#ef4444', '#f59e0b', '#22c55e'];

interface InsightAverages {
  attendance_rate?: number | null;
  study_hours_per_week?: number | null;
  lms_hours_per_week?: number | null;
  avg_sleep_hours?: number | null;
  stress_level?: number | null;
  midterm_score?: number | null;
}

interface RiskSlice { label: string; count: number; percent: number }

interface RecentPredictionEntry {
  student_id: string;
  risk_level: string;
  confidence: number;
  timestamp: string;
  attendance_rate?: number;
  study_hours_per_week?: number;
  lms_hours_per_week?: number;
  avg_sleep_hours?: number;
  stress_level?: number;
}

interface InsightsResponse {
  predictions_count: number;
  risk_distribution: RiskSlice[];
  high_risk_rate: number;
  averages: InsightAverages;
  recent_predictions: RecentPredictionEntry[];
}

const StatCard: React.FC<{ label: string; value: string | number; sublabel?: string }> = ({ label, value, sublabel }) => (
  <Paper elevation={2} sx={{ p: 2.5, borderRadius: 2 }}>
    <Typography variant="overline" color="text.secondary">{label}</Typography>
    <Typography variant="h5" fontWeight={800}>{value}</Typography>
    {sublabel && <Typography variant="caption" color="text.secondary">{sublabel}</Typography>}
  </Paper>
);

const RiskChip: React.FC<{ level: string }> = ({ level }) => {
  const color = level.includes('High') ? 'error' : level.includes('Medium') ? 'warning' : 'success';
  return <Chip size="small" color={color as any} label={level} />;
};

const EducatorDashboard: React.FC<{ onNavigateToTab?: (tabIndex: number) => void }> = ({ onNavigateToTab }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<InsightsResponse | null>(null);

  const load = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_URL}/insights`);
      setData(res.data);
      setError(null);
    } catch (e: any) {
      setError(e.response?.data?.error || 'Failed to load insights');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const riskChartData = useMemo(() => (data?.risk_distribution || []).map((d) => ({ name: d.label, value: d.count })), [data]);

  if (loading) return <Box sx={{ display:'flex', justifyContent:'center', py: 8 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      {/* Header */}
      <Paper sx={{ p: 3, borderRadius: 3, mb: 3 }}>
        <Stack direction="row" alignItems="center" spacing={1}>
          <DashboardIcon color="primary" />
          <Typography variant="h5" fontWeight={800}>Educator Dashboard</Typography>
        </Stack>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          High-level view tailored for principals and teachers. See risk distribution, cohort health, and recent predictions.
        </Typography>
      </Paper>

      {/* KPI cards */}
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label="Predictions" value={data?.predictions_count ?? 0} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label="High-Risk Rate" value={`${((data?.high_risk_rate || 0) * 100).toFixed(0)}%`} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label="Avg Attendance" value={data?.averages.attendance_rate != null ? `${(data.averages.attendance_rate).toFixed(0)}%` : '—'} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard label="Avg Study Hours" value={data?.averages.study_hours_per_week != null ? `${(data.averages.study_hours_per_week).toFixed(1)} h/wk` : '—'} />
        </Grid>
      </Grid>

      <Grid container spacing={2} sx={{ mt: 1 }}>
        {/* Risk Distribution */}
        <Grid item xs={12} md={5}>
          <Paper sx={{ p: 2.5, borderRadius: 2, height: 360 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Risk Distribution
            </Typography>
            <Box sx={{ width: '100%', height: 280 }}>
              <ResponsiveContainer>
                <PieChart>
                  <Pie dataKey="value" data={riskChartData} cx="50%" cy="50%" outerRadius={100} label>
                    {riskChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        {/* Cohort signals */}
        <Grid item xs={12} md={7}>
          <Paper sx={{ p: 2.5, borderRadius: 2, height: 360 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Cohort Signals
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} md={3}><StatCard label="Avg LMS Hours" value={data?.averages.lms_hours_per_week != null ? `${data.averages.lms_hours_per_week.toFixed(1)} h/wk` : '—'} /></Grid>
              <Grid item xs={6} md={3}><StatCard label="Avg Sleep" value={data?.averages.avg_sleep_hours != null ? `${data.averages.avg_sleep_hours.toFixed(1)} hrs` : '—'} /></Grid>
              <Grid item xs={6} md={3}><StatCard label="Avg Stress" value={data?.averages.stress_level != null ? data.averages.stress_level.toFixed(1) : '—'} /></Grid>
              <Grid item xs={6} md={3}><StatCard label="Avg Midterm" value={data?.averages.midterm_score != null ? `${data.averages.midterm_score.toFixed(0)}%` : '—'} /></Grid>
            </Grid>
            <Divider sx={{ my: 2 }} />
            <Stack direction={{ xs: 'column', md: 'row' }} spacing={1}>
              <Button startIcon={<UploadFileIcon />} variant="contained" color="primary" onClick={() => onNavigateToTab?.(2)}>
                Analyze a Cohort (Batch)
              </Button>
              <Button startIcon={<PsychologyIcon />} variant="outlined" onClick={() => onNavigateToTab?.(1)}>
                Predict a Student
              </Button>
              <Button onClick={load}>Refresh</Button>
            </Stack>
          </Paper>
        </Grid>
      </Grid>

      {/* Recent predictions */}
      <Paper sx={{ p: 2.5, borderRadius: 2, mt: 2 }}>
        <Typography variant="subtitle1" fontWeight={700} gutterBottom>
          Recent Predictions
        </Typography>
        {(!data || data.recent_predictions.length === 0) ? (
          <Alert severity="info">No predictions yet. Try predicting a student or uploading a cohort.</Alert>
        ) : (
          <Box sx={{ display:'grid', gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr', gap: 1 }}>
            <Typography variant="caption" color="text.secondary">Student</Typography>
            <Typography variant="caption" color="text.secondary">Risk</Typography>
            <Typography variant="caption" color="text.secondary">Confidence</Typography>
            <Typography variant="caption" color="text.secondary">Attendance</Typography>
            <Typography variant="caption" color="text.secondary">Study Hours</Typography>
            {data.recent_predictions.map((r) => (
              <React.Fragment key={r.timestamp + r.student_id}>
                <Typography variant="body2">{r.student_id}</Typography>
                <RiskChip level={r.risk_level} />
                <Typography variant="body2">{(r.confidence * 100).toFixed(0)}%</Typography>
                <Typography variant="body2">{r.attendance_rate != null ? `${r.attendance_rate}%` : '—'}</Typography>
                <Typography variant="body2">{r.study_hours_per_week != null ? `${r.study_hours_per_week} h/wk` : '—'}</Typography>
              </React.Fragment>
            ))}
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default EducatorDashboard;

