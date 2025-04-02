import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Box,
  Typography,
  CircularProgress
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';

const ChatInterface = () => {
  const [businessIdea, setBusinessIdea] = useState('');
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!businessIdea.trim()) return;

    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post('http://localhost:5002/api/analyze', {
        business_idea: businessIdea
      });
      setAnalysis(response.data.result);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred while analyzing your business idea');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper 
      elevation={3}
      sx={{
        width: '100%',
        maxWidth: '800px',
        p: 3,
        display: 'flex',
        flexDirection: 'column',
        gap: 2
      }}
    >
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Enter your business idea..."
          value={businessIdea}
          onChange={(e) => setBusinessIdea(e.target.value)}
          disabled={loading}
        />
        <Button
          variant="contained"
          type="submit"
          disabled={loading || !businessIdea.trim()}
          endIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
        >
          Analyze
        </Button>
      </form>

      {error && (
        <Typography color="error" variant="body2">
          {error}
        </Typography>
      )}

      {analysis && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Analysis Result:
          </Typography>
          <Paper 
            variant="outlined" 
            sx={{ 
              p: 2,
              backgroundColor: 'rgba(144, 202, 249, 0.08)',
              whiteSpace: 'pre-wrap'
            }}
          >
            {analysis}
          </Paper>
        </Box>
      )}
    </Paper>
  );
};

export default ChatInterface;
