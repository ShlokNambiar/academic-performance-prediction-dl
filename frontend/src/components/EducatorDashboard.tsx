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
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, LineChart, Line } from 'recharts';

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

interface StatsResponse {
  metrics?: { accuracy?: number | null; f1_weighted?: number | null; precision?: number | null; recall?: number | null };
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
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [recent, setRecent] = useState<RecentPredictionEntry[]>([]);

  const load = async () => {
    try {
      setLoading(true);
      const [insightsRes, statsRes, recentRes] = await Promise.all([
        axios.get(`${API_URL}/insights`),
        axios.get(`${API_URL}/stats`),
        axios.get(`${API_URL}/predictions/recent`, { params: { limit: 200 } })
      ]);
      setData(insightsRes.data);
      setStats(statsRes.data);
      setRecent(recentRes.data?.results || []);
      setError(null);
    } catch (e: any) {
      setError(e.response?.data?.error || 'Failed to load insights');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const riskChartData = useMemo(() => (data?.risk_distribution || []).map((d) => ({ name: d.label, value: d.count })), [data]);
  const highRiskCount = useMemo(() => (data?.risk_distribution || []).find(d => d.label === 'High Risk')?.count || 0, [data]);
  const accuracy = stats?.metrics?.accuracy ?? null;
  const avgPerf = stats?.metrics?.f1_weighted ?? null;

  const trendData = useMemo(() => {
    const byDate = new Map<string, { date: string; High: number; Medium: number; Low: number; total: number }>();
    for (const r of recent) {
      const date = (r.timestamp || '').slice(0, 10);
      if (!date) continue;
      const cur = byDate.get(date) || { date, High: 0, Medium: 0, Low: 0, total: 0 };
      if ((r.risk_level || '').includes('High')) cur.High += 1; else if ((r.risk_level || '').includes('Medium')) cur.Medium += 1; else cur.Low += 1;
      cur.total += 1;
      byDate.set(date, cur);
    }
    return Array.from(byDate.values()).sort((a, b) => a.date.localeCompare(b.date));
  }, [recent]);

  if (loading) return <Box sx={{ display:'flex', justifyContent:'center', py: 8 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;

  return (
    <Box>
      <Box sx={{ display:'grid', gridTemplateColumns: { xs: '1fr', md: '260px 1fr' }, gap: 2 }}>
        {/* Left Sidebar */}
        <Box>
          <Typography variant="overline" color="text.secondary">Quick Metrics</Typography>
          <Stack spacing={1} sx={{ mt: 1 }}>
            <Paper sx={{ p: 2, borderRadius: 2 }}>
              <Typography variant="h6" fontWeight={800}>{data?.predictions_count ?? 0}</Typography>
              <Typography variant="caption" color="text.secondary">Total Students</Typography>
            </Paper>
            <Paper sx={{ p: 2, borderRadius: 2 }}>
              <Typography variant="h6" fontWeight={800}>{highRiskCount}</Typography>
              <Typography variant="caption" color="text.secondary">At-Risk</Typography>
            </Paper>
            <Paper sx={{ p: 2, borderRadius: 2 }}>
              <Typography variant="h6" fontWeight={800}>{accuracy != null ? `${(accuracy*100).toFixed(1)}%` : '—'}</Typography>
              <Typography variant="caption" color="text.secondary">Model Accuracy</Typography>
            </Paper>
          </Stack>

          <Divider sx={{ my: 2 }} />
          <Typography variant="overline" color="text.secondary">Quick Actions</Typography>
          <Stack spacing={1} sx={{ mt: 1 }}>
            <Button fullWidth variant="outlined">Overview</Button>
            <Button fullWidth variant="outlined" onClick={() => onNavigateToTab?.(2)}>Student List</Button>
            <Button fullWidth variant="outlined" disabled>Settings</Button>
            <Button fullWidth variant="outlined" disabled>Documentation</Button>
          </Stack>
        </Box>

        {/* Main Content */}
        <Box>
          {/* Header */}
          <Paper sx={{ p: 3, borderRadius: 3, mb: 3 }}>
            <Stack direction="row" alignItems="center" spacing={1}>
              <DashboardIcon color="primary" />
              <Typography variant="h5" fontWeight={800}>Dashboard Overview</Typography>
            </Stack>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Real-time insights into student performance predictions and intervention recommendations.
            </Typography>
          </Paper>

          {/* KPI row */}
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}><StatCard label="Students Analyzed" value={data?.predictions_count ?? 0} /></Grid>
            <Grid item xs={12} sm={6} md={3}><StatCard label="High Risk" value={highRiskCount} /></Grid>
            <Grid item xs={12} sm={6} md={3}><StatCard label="Avg Performance" value={avgPerf != null ? `${(avgPerf*100).toFixed(1)}%` : '—'} /></Grid>
            <Grid item xs={12} sm={6} md={3}><StatCard label="Model Accuracy" value={accuracy != null ? `${(accuracy*100).toFixed(1)}%` : '—'} /></Grid>
          </Grid>

          <Grid container spacing={2} sx={{ mt: 1 }}>
            {/* Performance Distribution (bar) */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2.5, borderRadius: 2, height: 360 }}>
                <Typography variant="subtitle1" fontWeight={700} gutterBottom>
                  Performance Distribution
                </Typography>
                <Box sx={{ width:'100%', height: 280 }}>
                  <ResponsiveContainer>
                    <BarChart data={riskChartData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis allowDecimals={false} />
                      <Tooltip />
                      <Bar dataKey="value" fill="#6A5AE0" radius={[6,6,0,0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
              </Paper>
            </Grid>

            {/* Risk Level Analysis (pie) */}
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 2.5, borderRadius: 2, height: 360 }}>
                <Typography variant="subtitle1" fontWeight={700} gutterBottom>
                  Risk Level Analysis
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
          </Grid>

          {/* Prediction Trends */}
          <Paper sx={{ p: 2.5, borderRadius: 2, mt: 2 }}>
            <Typography variant="subtitle1" fontWeight={700} gutterBottom>
              Prediction Trends Over Time
            </Typography>
            {trendData.length === 0 ? (
              <Alert severity="info">No data yet. Run some predictions to see trends.</Alert>
            ) : (
              <Box sx={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="High" stroke="#ef4444" strokeWidth={2} />
                    <Line type="monotone" dataKey="Medium" stroke="#f59e0b" strokeWidth={2} />
                    <Line type="monotone" dataKey="Low" stroke="#22c55e" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            )}
          </Paper>

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

          {/* Actions */}
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={1} sx={{ mt: 2 }}>
            <Button startIcon={<UploadFileIcon />} variant="contained" color="primary" onClick={() => onNavigateToTab?.(2)}>
              Analyze a Cohort (Batch)
            </Button>
            <Button startIcon={<PsychologyIcon />} variant="outlined" onClick={() => onNavigateToTab?.(1)}>
              Predict a Student
            </Button>
            <Button onClick={load}>Refresh</Button>
          </Stack>
        </Box>
      </Box>
    </Box>
  );
};

export default EducatorDashboard;
