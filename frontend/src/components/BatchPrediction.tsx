import React, { useState } from 'react';
import axios from 'axios';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import DownloadIcon from '@mui/icons-material/Download';

const API_URL = 'http://localhost:5000';

const COLORS = {
  'High Risk': 'error',
  'Medium Risk': 'warning',
  'Low Risk': 'success'
} as const;

interface BatchResult {
  student_id: string;
  risk_level: string;
  confidence: number;
}

const BatchPrediction: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<BatchResult[]>([]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const text = await file.text();
      const data = JSON.parse(text);
      
      const response = await axios.post(`${API_URL}/predict/batch`, data);
      setResults(response.data.results);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to process batch predictions');
    } finally {
      setLoading(false);
    }
  };

  const downloadResults = () => {
    const csv = [
      ['Student ID', 'Risk Level', 'Confidence'],
      ...results.map(r => [r.student_id, r.risk_level, (r.confidence * 100).toFixed(2) + '%'])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'batch_predictions.csv';
    a.click();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Batch Predictions
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Upload a JSON file with multiple student records to get batch predictions.
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
          <Button
            variant="contained"
            component="label"
            startIcon={<UploadFileIcon />}
            disabled={loading}
          >
            Upload JSON File
            <input
              type="file"
              hidden
              accept=".json"
              onChange={handleFileUpload}
            />
          </Button>
          
          {results.length > 0 && (
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={downloadResults}
            >
              Download Results (CSV)
            </Button>
          )}

          {loading && <CircularProgress size={24} />}
        </Box>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </Paper>

      {results.length > 0 && (
        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Student ID</TableCell>
                  <TableCell>Risk Level</TableCell>
                  <TableCell align="right">Confidence</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {results.map((result, index) => (
                  <TableRow key={index}>
                    <TableCell>{result.student_id}</TableCell>
                    <TableCell>
                      <Chip
                        label={result.risk_level}
                        color={COLORS[result.risk_level as keyof typeof COLORS]}
                        size="small"
                      />
                    </TableCell>
                    <TableCell align="right">
                      {(result.confidence * 100).toFixed(1)}%
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      )}
    </Box>
  );
};

export default BatchPrediction;

