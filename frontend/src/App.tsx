import React, { useState } from 'react';
import {
  Container,
  AppBar,
  Toolbar,
  Typography,
  Box,
  Tab,
  Tabs,
  ThemeProvider,
  createTheme,
  CssBaseline
} from '@mui/material';
import SchoolIcon from '@mui/icons-material/School';
import PsychologyIcon from '@mui/icons-material/Psychology';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import InsightsIcon from '@mui/icons-material/Insights';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ComprehensivePrediction from './components/ComprehensivePrediction';
import BatchPrediction from './components/BatchPrediction';
import ModelInsights from './components/ModelInsights';
import EducatorDashboard from './components/EducatorDashboard';
import './App.css';

const theme = createTheme({
  palette: {
    primary: { main: '#2563eb' },
    secondary: { main: '#64748b' },
    success: { main: '#10b981' },
    warning: { main: '#f59e0b' },
    error: { main: '#ef4444' },
    background: { default: '#f8fafc', paper: '#ffffff' },
    text: { primary: '#0f172a', secondary: '#64748b' }
  },
  shape: { borderRadius: 8 },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h4: { fontWeight: 700, letterSpacing: '-0.02em' },
    h5: { fontWeight: 600, letterSpacing: '-0.01em' },
    h6: { fontWeight: 600 }
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 500,
          borderRadius: 8,
          boxShadow: 'none',
          '&:hover': { boxShadow: 'none' }
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)'
        }
      }
    }
  }
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
        <AppBar
          position="static"
          elevation={0}
          sx={{
            bgcolor: 'white',
            borderBottom: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Toolbar sx={{ py: 1.5 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mr: 2 }}>
              <SchoolIcon sx={{ fontSize: 28, color: 'primary.main' }} />
            </Box>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h6" component="div" fontWeight={600} color="text.primary">
                Academic Performance Prediction
              </Typography>
              <Typography variant="caption" color="text.secondary">
                AI-Powered Student Risk Assessment
              </Typography>
            </Box>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {/* Hero section */}
        <Box sx={{
          width: '100%',
          bgcolor: 'white',
          borderRadius: 2,
          mb: 4,
          p: { xs: 3, md: 4 },
          border: '1px solid',
          borderColor: 'divider'
        }}>
          <Typography variant="h4" fontWeight={700} gutterBottom color="text.primary">
            📚 Academic Performance Prediction
          </Typography>
          <Typography variant="body1" color="text.secondary">
            AI-powered risk assessment, insights, and personalized recommendations to support student success.
          </Typography>
        </Box>

        <Box
          sx={{
            borderBottom: 2,
            borderColor: 'divider',
            bgcolor: 'background.paper',
            borderRadius: '12px 12px 0 0',
            boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
          }}
        >
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="dashboard tabs"
            variant="scrollable"
            allowScrollButtonsMobile
            sx={{
              '& .MuiTab-root': {
                fontWeight: 700,
                fontSize: '0.95rem',
                textTransform: 'none',
                minHeight: 64,
                '&.Mui-selected': {
                  color: 'primary.main'
                }
              }
            }}
          >
            <Tab icon={<DashboardIcon />} iconPosition="start" label="Dashboard" />
            <Tab icon={<PsychologyIcon />} iconPosition="start" label="Single Prediction" />
            <Tab icon={<UploadFileIcon />} iconPosition="start" label="Batch Predictions" />
            <Tab icon={<InsightsIcon />} iconPosition="start" label="Model Insights" />
          </Tabs>
        </Box>

          <TabPanel value={tabValue} index={0}>
            <EducatorDashboard onNavigateToTab={(i) => setTabValue(i)} />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <ComprehensivePrediction />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <BatchPrediction />
          </TabPanel>

          <TabPanel value={tabValue} index={3}>
            <ModelInsights />
          </TabPanel>
        </Container>

        <Box
          component="footer"
          sx={{
            py: 4,
            px: 2,
            mt: 6,
            bgcolor: 'white',
            borderTop: '1px solid',
            borderColor: 'divider'
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="body2" align="center" color="text.secondary">
              © 2025 Academic Performance Prediction System
            </Typography>
            <Typography variant="caption" align="center" display="block" color="text.secondary" sx={{ mt: 0.5 }}>
              Deep Learning Project | AI-Powered Education Analytics
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
