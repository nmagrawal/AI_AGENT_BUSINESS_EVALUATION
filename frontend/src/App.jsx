import React, { useState } from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { createTheme } from '@mui/material/styles';
import ChatInterface from './components/ChatInterface';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    background: {
      default: '#121212',
      paper: '#1e1e1e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div style={{ 
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '2rem'
      }}>
        <h1 style={{ color: '#90caf9', marginBottom: '2rem' }}>
          Business Idea Analyzer
        </h1>
        <ChatInterface />
      </div>
    </ThemeProvider>
  );
}

export default App;
