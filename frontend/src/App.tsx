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
import ComprehensivePrediction from './components/ComprehensivePrediction';
import BatchPrediction from './components/BatchPrediction';
import ModelInsights from './components/ModelInsights';
import './App.css';

const theme = createTheme({
  palette: {
    primary: { main: '#6A5AE0' },
    secondary: { main: '#FF6B6B' },
    success: { main: '#22c55e' },
    warning: { main: '#f59e0b' },
    error: { main: '#ef4444' },
    background: { default: '#f7f7fb' }
  },
  shape: { borderRadius: 12 },
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
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <SchoolIcon sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Academic Performance Prediction System
            </Typography>
            <Typography variant="body2">
              AI-Powered Student Risk Assessment
            </Typography>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        {/* Hero section */}
        <Box sx={{
          width: '100%',
          background: 'linear-gradient(135deg, #6A5AE0 0%, #8A67F4 100%)',
          color: 'white',
          borderRadius: 2,
          mb: 3,
          p: { xs: 3, md: 5 }
        }}>
          <Typography variant="h4" fontWeight={800} gutterBottom>
            Academic Performance Prediction
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.9 }}>
            AI-powered risk assessment, insights, and recommendations to support student success.
          </Typography>
        </Box>

        <Box sx={{ borderBottom: 1, borderColor: 'divider', bgcolor: 'background.default' }}>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="dashboard tabs" variant="scrollable" allowScrollButtonsMobile>
            <Tab icon={<PsychologyIcon />} iconPosition="start" label="Single Prediction" />
            <Tab icon={<UploadFileIcon />} iconPosition="start" label="Batch Predictions" />
            <Tab icon={<InsightsIcon />} iconPosition="start" label="Model Insights" />
          </Tabs>
        </Box>

          <TabPanel value={tabValue} index={0}>
            <ComprehensivePrediction />
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <BatchPrediction />
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            <ModelInsights />
          </TabPanel>
        </Container>

        <Box
          component="footer"
          sx={{
            py: 3,
            px: 2,
            mt: 'auto',
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[200]
                : theme.palette.grey[800],
          }}
        >
          <Container maxWidth="sm">
            <Typography variant="body2" color="text.secondary" align="center">
              © 2025 Academic Performance Prediction System | Deep Learning Project
            </Typography>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
