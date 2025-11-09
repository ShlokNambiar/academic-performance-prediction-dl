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
    primary: { main: '#6A5AE0' },
    secondary: { main: '#FF6B6B' },
    success: { main: '#22c55e' },
    warning: { main: '#f59e0b' },
    error: { main: '#ef4444' },
    background: { default: '#f8f9fd', paper: '#ffffff' }
  },
  shape: { borderRadius: 12 },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: { fontWeight: 800 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 }
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
          borderRadius: 10
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none'
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
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            borderBottom: '1px solid rgba(255,255,255,0.1)'
          }}
        >
          <Toolbar sx={{ py: 1 }}>
            <Box
              sx={{
                p: 1,
                borderRadius: 2,
                bgcolor: 'rgba(255,255,255,0.15)',
                display: 'flex',
                alignItems: 'center',
                mr: 2
              }}
            >
              <SchoolIcon sx={{ fontSize: 28 }} />
            </Box>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h6" component="div" fontWeight={800}>
                Academic Performance Prediction System
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                AI-Powered Student Risk Assessment
              </Typography>
            </Box>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {/* Hero section */}
        <Box sx={{
          width: '100%',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          borderRadius: 4,
          mb: 4,
          p: { xs: 4, md: 6 },
          boxShadow: '0 10px 40px rgba(102, 126, 234, 0.3)',
          position: 'relative',
          overflow: 'hidden',
          '&::before': {
            content: '""',
            position: 'absolute',
            top: 0,
            right: 0,
            width: '40%',
            height: '100%',
            background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
            pointerEvents: 'none'
          }
        }}>
          <Typography variant="h3" fontWeight={900} gutterBottom sx={{ position: 'relative', zIndex: 1 }}>
            📚 Academic Performance Prediction
          </Typography>
          <Typography variant="h6" sx={{ opacity: 0.95, position: 'relative', zIndex: 1, fontWeight: 400 }}>
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
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: '12px 12px 0 0'
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="body1" align="center" fontWeight={600}>
              © 2025 Academic Performance Prediction System
            </Typography>
            <Typography variant="body2" align="center" sx={{ opacity: 0.9, mt: 0.5 }}>
              Deep Learning Project | AI-Powered Education Analytics
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
