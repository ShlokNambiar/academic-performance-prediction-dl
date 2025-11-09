import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import {
  Box,
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


const StatCard: React.FC<{ label: string; value: string | number; sublabel?: string; color?: string }> = ({ label, value, sublabel, color }) => (
  <Paper
    elevation={0}
    sx={{
      p: 3,
      borderRadius: 2,
      border: '1px solid',
      borderColor: 'divider',
      bgcolor: 'white',
      transition: 'border-color 0.2s',
      '&:hover': {
        borderColor: color || 'primary.main'
      }
    }}
  >
    <Typography variant="caption" color="text.secondary" fontWeight={600} textTransform="uppercase" letterSpacing={0.5}>{label}</Typography>
    <Typography variant="h4" fontWeight={700} sx={{ my: 1, color: color || 'text.primary' }}>{value}</Typography>
    {sublabel && <Typography variant="body2" color="text.secondary">{sublabel}</Typography>}
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
      <Box sx={{ display:'grid', gridTemplateColumns: { xs: '1fr', md: '280px 1fr' }, gap: 3 }}>
        {/* Left Sidebar */}
        <Box>
          <Typography variant="overline" color="text.secondary" fontWeight={700} sx={{ letterSpacing: 1.2 }}>Quick Metrics</Typography>
          <Stack spacing={2} sx={{ mt: 2 }}>
            <Paper
              elevation={0}
              sx={{
                p: 2.5,
                borderRadius: 2,
                border: '1px solid',
                borderColor: 'divider',
                bgcolor: 'white'
              }}
            >
              <Typography variant="h4" fontWeight={700} color="primary.main">{data?.predictions_count ?? 0}</Typography>
              <Typography variant="caption" color="text.secondary" fontWeight={600} textTransform="uppercase">Total Students</Typography>
            </Paper>
            <Paper
              elevation={0}
              sx={{
                p: 2.5,
                borderRadius: 2,
                border: '1px solid',
                borderColor: 'divider',
                bgcolor: 'white'
              }}
            >
              <Typography variant="h4" fontWeight={700} color="error.main">{highRiskCount}</Typography>
              <Typography variant="caption" color="text.secondary" fontWeight={600} textTransform="uppercase">At-Risk Students</Typography>
            </Paper>
            <Paper
              elevation={0}
              sx={{
                p: 2.5,
                borderRadius: 2,
                border: '1px solid',
                borderColor: 'divider',
                bgcolor: 'white'
              }}
            >
              <Typography variant="h4" fontWeight={700} color="success.main">{accuracy != null ? `${(accuracy*100).toFixed(1)}%` : '—'}</Typography>
              <Typography variant="caption" color="text.secondary" fontWeight={600} textTransform="uppercase">Model Accuracy</Typography>
            </Paper>
          </Stack>

          <Divider sx={{ my: 3 }} />
          <Typography variant="overline" color="text.secondary" fontWeight={700} sx={{ letterSpacing: 1.2 }}>Quick Actions</Typography>
          <Stack spacing={1.5} sx={{ mt: 1.5 }}>
            <Button
              fullWidth
              variant="contained"
              size="small"
              sx={{ justifyContent: 'flex-start', textTransform: 'none', fontWeight: 500 }}
            >
              Overview
            </Button>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => onNavigateToTab?.(2)}
              sx={{ borderRadius: 2, textTransform: 'none', fontWeight: 600 }}
            >
              Batch Upload
            </Button>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => onNavigateToTab?.(1)}
              sx={{ borderRadius: 2, textTransform: 'none', fontWeight: 600 }}
            >
              Single Prediction
            </Button>
            <Button
              fullWidth
              variant="text"
              onClick={load}
              sx={{ borderRadius: 2, textTransform: 'none', fontWeight: 600 }}
            >
              Refresh Data
            </Button>
          </Stack>
        </Box>

        {/* Main Content */}
        <Box>
          {/* Header */}
          <Box sx={{ mb: 3 }}>
            <Stack direction="row" alignItems="center" spacing={1.5} sx={{ mb: 1 }}>
              <DashboardIcon sx={{ fontSize: 28, color: 'primary.main' }} />
              <Typography variant="h5" fontWeight={700} color="text.primary">Dashboard Overview</Typography>
            </Stack>
            <Typography variant="body2" color="text.secondary">
              Real-time insights into student performance predictions and intervention recommendations.
            </Typography>
          </Box>

          {/* KPI row */}
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr', md: 'repeat(4, 1fr)' }, gap: 2 }}>
            <StatCard
              label="Students Analyzed"
              value={data?.predictions_count ?? 0}
              color="primary.main"
            />
            <StatCard
              label="High Risk"
              value={highRiskCount}
              color="error.main"
            />
            <StatCard
              label="Avg Performance"
              value={avgPerf != null ? `${(avgPerf*100).toFixed(1)}%` : '—'}
              color="warning.main"
            />
            <StatCard
              label="Model Accuracy"
              value={accuracy != null ? `${(accuracy*100).toFixed(1)}%` : '—'}
              color="success.main"
            />
          </Box>

          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' }, gap: 2.5, mt: 2.5 }}>
            {/* Performance Distribution (bar) */}
            <Box>
              <Paper
                elevation={0}
                sx={{
                  p: 3,
                  borderRadius: 4,
                  height: 400,
                  border: '1px solid',
                  borderColor: 'divider',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
                  transition: 'box-shadow 0.3s',
                  '&:hover': {
                    boxShadow: '0 8px 32px rgba(0,0,0,0.12)'
                  }
                }}
              >
                <Typography variant="h6" fontWeight={800} gutterBottom sx={{ mb: 2 }}>
                  📊 Performance Distribution
                </Typography>
                <Box sx={{ width:'100%', height: 310 }}>
                  <ResponsiveContainer>
                    <BarChart data={riskChartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                      <XAxis dataKey="name" style={{ fontSize: 12, fontWeight: 600 }} />
                      <YAxis allowDecimals={false} style={{ fontSize: 12 }} />
                      <Tooltip
                        contentStyle={{
                          borderRadius: 8,
                          border: 'none',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                        }}
                      />
                      <Bar dataKey="value" fill="url(#colorGradient)" radius={[8,8,0,0]} />
                      <defs>
                        <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor="#667eea" stopOpacity={1}/>
                          <stop offset="100%" stopColor="#764ba2" stopOpacity={0.8}/>
                        </linearGradient>
                      </defs>
                    </BarChart>
                  </ResponsiveContainer>
                </Box>
              </Paper>
            </Box>

            {/* Risk Level Analysis (pie) */}
            <Box>
              <Paper
                elevation={0}
                sx={{
                  p: 3,
                  borderRadius: 4,
                  height: 400,
                  border: '1px solid',
                  borderColor: 'divider',
                  boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
                  transition: 'box-shadow 0.3s',
                  '&:hover': {
                    boxShadow: '0 8px 32px rgba(0,0,0,0.12)'
                  }
                }}
              >
                <Typography variant="h6" fontWeight={800} gutterBottom sx={{ mb: 2 }}>
                  🎯 Risk Level Analysis
                </Typography>
                <Box sx={{ width: '100%', height: 310 }}>
                  <ResponsiveContainer>
                    <PieChart>
                      <Pie
                        dataKey="value"
                        data={riskChartData}
                        cx="50%"
                        cy="50%"
                        outerRadius={110}
                        label={(entry) => `${entry.name}: ${entry.value}`}
                        labelLine={{ stroke: '#999', strokeWidth: 1 }}
                      >
                        {riskChartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{
                          borderRadius: 8,
                          border: 'none',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                        }}
                      />
                      <Legend
                        verticalAlign="bottom"
                        height={36}
                        iconType="circle"
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </Box>
              </Paper>
            </Box>
          </Box>

          {/* Prediction Trends */}
          <Paper
            elevation={0}
            sx={{
              p: 3,
              borderRadius: 4,
              mt: 2.5,
              border: '1px solid',
              borderColor: 'divider',
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              transition: 'box-shadow 0.3s',
              '&:hover': {
                boxShadow: '0 8px 32px rgba(0,0,0,0.12)'
              }
            }}
          >
            <Typography variant="h6" fontWeight={800} gutterBottom sx={{ mb: 2 }}>
              📈 Prediction Trends Over Time
            </Typography>
            {trendData.length === 0 ? (
              <Alert
                severity="info"
                sx={{
                  borderRadius: 3,
                  '& .MuiAlert-icon': { fontSize: 28 }
                }}
              >
                No data yet. Run some predictions to see trends over time.
              </Alert>
            ) : (
              <Box sx={{ width: '100%', height: 320 }}>
                <ResponsiveContainer>
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                    <XAxis dataKey="date" style={{ fontSize: 11, fontWeight: 600 }} />
                    <YAxis allowDecimals={false} style={{ fontSize: 11 }} />
                    <Tooltip
                      contentStyle={{
                        borderRadius: 8,
                        border: 'none',
                        boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
                      }}
                    />
                    <Legend iconType="circle" />
                    <Line type="monotone" dataKey="High" stroke="#ef4444" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    <Line type="monotone" dataKey="Medium" stroke="#f59e0b" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                    <Line type="monotone" dataKey="Low" stroke="#22c55e" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            )}
          </Paper>

          {/* Recent predictions */}
          <Paper
            elevation={0}
            sx={{
              p: 3,
              borderRadius: 4,
              mt: 2.5,
              border: '1px solid',
              borderColor: 'divider',
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
              transition: 'box-shadow 0.3s',
              '&:hover': {
                boxShadow: '0 8px 32px rgba(0,0,0,0.12)'
              }
            }}
          >
            <Typography variant="h6" fontWeight={800} gutterBottom sx={{ mb: 2 }}>
              🕒 Recent Predictions
            </Typography>
            {(!data || data.recent_predictions.length === 0) ? (
              <Alert
                severity="info"
                sx={{
                  borderRadius: 3,
                  '& .MuiAlert-icon': { fontSize: 28 }
                }}
              >
                No predictions yet. Try predicting a student or uploading a cohort.
              </Alert>
            ) : (
              <Box sx={{
                display:'grid',
                gridTemplateColumns: '2fr 1fr 1fr 1fr 1fr',
                gap: 2,
                '& > *': { py: 1.5, borderBottom: '1px solid', borderColor: 'divider' }
              }}>
                <Typography variant="caption" color="text.secondary" fontWeight={700} sx={{ textTransform: 'uppercase', letterSpacing: 1 }}>Student</Typography>
                <Typography variant="caption" color="text.secondary" fontWeight={700} sx={{ textTransform: 'uppercase', letterSpacing: 1 }}>Risk</Typography>
                <Typography variant="caption" color="text.secondary" fontWeight={700} sx={{ textTransform: 'uppercase', letterSpacing: 1 }}>Confidence</Typography>
                <Typography variant="caption" color="text.secondary" fontWeight={700} sx={{ textTransform: 'uppercase', letterSpacing: 1 }}>Attendance</Typography>
                <Typography variant="caption" color="text.secondary" fontWeight={700} sx={{ textTransform: 'uppercase', letterSpacing: 1 }}>Study Hours</Typography>
                {data.recent_predictions.slice(0, 10).map((r) => (
                  <React.Fragment key={r.timestamp + r.student_id}>
                    <Typography variant="body2" fontWeight={600}>{r.student_id}</Typography>
                    <RiskChip level={r.risk_level} />
                    <Typography variant="body2" fontWeight={600}>{(r.confidence * 100).toFixed(0)}%</Typography>
                    <Typography variant="body2">{r.attendance_rate != null ? `${r.attendance_rate}%` : '—'}</Typography>
                    <Typography variant="body2">{r.study_hours_per_week != null ? `${r.study_hours_per_week} h/wk` : '—'}</Typography>
                  </React.Fragment>
                ))}
              </Box>
            )}
          </Paper>

          {/* Actions */}
          <Stack direction={{ xs: 'column', md: 'row' }} spacing={2} sx={{ mt: 3 }}>
            <Button
              startIcon={<UploadFileIcon />}
              variant="contained"
              size="large"
              onClick={() => onNavigateToTab?.(2)}
              sx={{
                borderRadius: 3,
                textTransform: 'none',
                fontWeight: 700,
                px: 4,
                boxShadow: '0 4px 14px rgba(106, 90, 224, 0.4)',
                '&:hover': {
                  boxShadow: '0 6px 20px rgba(106, 90, 224, 0.5)'
                }
              }}
            >
              Analyze a Cohort (Batch)
            </Button>
            <Button
              startIcon={<PsychologyIcon />}
              variant="outlined"
              size="large"
              onClick={() => onNavigateToTab?.(1)}
              sx={{
                borderRadius: 3,
                textTransform: 'none',
                fontWeight: 700,
                px: 4,
                borderWidth: 2,
                '&:hover': {
                  borderWidth: 2
                }
              }}
            >
              Predict a Student
            </Button>
          </Stack>
        </Box>
      </Box>
    </Box>
  );
};

export default EducatorDashboard;
