import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Box,
  Paper,
  Typography,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import Grid from '@mui/material/Grid2';
import InsightsIcon from '@mui/icons-material/Insights';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const API_URL = 'http://localhost:5000';

interface TopFeature { feature: string; importance: number }

interface StatsResponse {
  model_info: {
    model_type: string;
    risk_levels: string[];
    total_features: number;
  };
  top_features: TopFeature[];
}

const StatCard: React.FC<{ label: string; value: string | number }> = ({ label, value }) => (
  <Paper elevation={2} sx={{ p: 2, borderRadius: 2 }}>
    <Typography variant="overline" color="text.secondary">{label}</Typography>
    <Typography variant="h5" fontWeight={700}>{value}</Typography>
  </Paper>
);

const ModelInsights: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await axios.get(`${API_URL}/stats`);
        setStats(res.data);
      } catch (e: any) {
        setError(e.response?.data?.error || 'Failed to load model stats');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <Box sx={{ display:'flex', justifyContent:'center', py: 8 }}><CircularProgress /></Box>;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!stats) return null;

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
        <Box sx={{ display:'flex', alignItems:'center', gap: 1, mb: 2 }}>
          <InsightsIcon color="primary" />
          <Typography variant="h5" fontWeight={700}>Model Insights</Typography>
        </Box>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <StatCard label="Model Type" value={stats.model_info.model_type} />
          </Grid>
          <Grid item xs={12} md={4}>
            <StatCard label="Total Features" value={stats.model_info.total_features} />
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper elevation={2} sx={{ p: 2, borderRadius: 2 }}>
              <Typography variant="overline" color="text.secondary">Risk Levels</Typography>
              <Box sx={{ display:'flex', gap: 1, flexWrap:'wrap', mt: 1 }}>
                {stats.model_info.risk_levels.map((r) => (
                  <Chip key={r} label={r} color={r.includes('High') ? 'error' : r.includes('Medium') ? 'warning' : 'success'} size="small" />
                ))}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Paper>

      <Paper sx={{ p: 3, borderRadius: 3 }}>
        <Typography variant="h6" fontWeight={700} gutterBottom>
          Top Feature Importances
        </Typography>
        <Box sx={{ width: '100%', height: 360 }}>
          <ResponsiveContainer>
            <BarChart data={stats.top_features} margin={{ left: 12, right: 12, top: 12, bottom: 12 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="feature" tick={{ fontSize: 12 }} interval={0} angle={-25} textAnchor="end" height={80} />
              <YAxis tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
              <Tooltip formatter={(v: number) => `${(v * 100).toFixed(2)}%`} />
              <Bar dataKey="importance" fill="#7c4dff" radius={[6,6,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </Paper>
    </Box>
  );
};

export default ModelInsights;
