'use client';
import React, { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Button, CircularProgress, Snackbar, Alert } from '@mui/material';

interface ScrapeButtonProps {
  onScrapeComplete?: () => void;
}

export function ScrapeButton({ onScrapeComplete }: ScrapeButtonProps) {
  const queryClient = useQueryClient();
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success' | 'error' | 'warning' }>({
    open: false,
    message: '',
    severity: 'success',
  });
  const [done, setDone] = useState(false);

  const getApiUrl = (endpoint: string): string => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  const scrapeMutation = useMutation({
    mutationFn: async () => {
      const url = getApiUrl('/scrape');
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      if (!res.ok) {
        if (res.status === 409) {
          throw new Error('409');
        }
        throw new Error(`Error ${res.status}: Failed to scrape`);
      }
      return res.json();
    },
    onSuccess: (data) => {
      // Invalidate jobs to refetch data on the dashboard
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      
      const results = data.results || {};
      const counts = Object.entries(results).map(([source, result]: [string, any]) => `${source}: ${result.jobs_inserted}`).join(', ');
      
      setSnackbar({ open: true, message: `Scraping completed! ${counts}`, severity: 'success' });
      setDone(true);
      
      if (onScrapeComplete) {
        onScrapeComplete();
      }
      
      setTimeout(() => setDone(false), 2000);
    },
    onError: (err: any) => {
      if (err.message === '409') {
        setSnackbar({ open: true, message: 'Scrape already in progress', severity: 'warning' });
      } else {
        setSnackbar({ open: true, message: err.message, severity: 'error' });
      }
    },
  });

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <>
      <Button
        variant="contained"
        color="primary"
        onClick={() => scrapeMutation.mutate()}
        disabled={scrapeMutation.isPending || done}
        startIcon={scrapeMutation.isPending ? <CircularProgress size={20} color="inherit" /> : null}
      >
        {done ? 'Done' : scrapeMutation.isPending ? 'Scraping...' : 'Scrape Jobs'}
      </Button>

      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={6000} 
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </>
  );
}
