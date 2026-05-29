'use client';

import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { CircularProgress, Button, Snackbar, Alert, Typography } from '@mui/material';
import { POLLING_INTERVAL_MS } from '../lib/constants';

export default function CoverLetterViewer({ jobId }: { jobId: string }) {
  const queryClient = useQueryClient();
  const [coverLetterExpired, setCoverLetterExpired] = useState(false);
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error'}>({
    open: false, message: '', severity: 'success'
  });

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    return `${cleanBase}${endpoint}`;
  };

  const { data: coverLetter, isLoading, error } = useQuery({
    queryKey: ['cover-letter', jobId],
    queryFn: async () => {
      const res = await fetch(getApiUrl(`/cover-letter/${jobId}`));
      if (!res.ok) {
        if (res.status === 404 || res.status === 422) {
          setCoverLetterExpired(true);
        }
        throw new Error('Failed to load cover letter');
      }
      return res.json();
    },
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === 'pending' || status === 'generating' ? POLLING_INTERVAL_MS : false;
    },
    retry: false
  });

  const handleDownload = async (format: 'pdf' | 'markdown') => {
    try {
      const res = await fetch(getApiUrl(`/cover-letter/${jobId}/export?format=${format}`));
      
      if (!res.ok) {
        if (res.status === 422) {
          queryClient.invalidateQueries({ queryKey: ['cover-letter', jobId] });
          setCoverLetterExpired(true);
          setSnackbar({ open: true, message: 'Cover letter is no longer available. Please regenerate it.', severity: 'error' });
          return;
        }
        throw new Error('Download failed');
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cover-letter.${format === 'markdown' ? 'md' : 'pdf'}`;
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      if (format === 'pdf') {
        // JD-312: Fallback to clipboard copy if PDF export fails
        try {
          await navigator.clipboard.writeText(coverLetter.content);
          setSnackbar({ open: true, message: 'PDF export failed. Cover letter copied to clipboard instead.', severity: 'success' });
        } catch (clipboardErr) {
          setSnackbar({ open: true, message: 'Export failed and could not copy to clipboard.', severity: 'error' });
        }
      } else {
        setSnackbar({ open: true, message: 'Download failed. Please try again.', severity: 'error' });
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <CircularProgress />
      </div>
    );
  }

  if (coverLetterExpired || error || !coverLetter) {
    return (
      <div className="mt-8 pt-8 border-t border-gray-100">
        <div className="p-4 bg-gray-50 text-gray-700 rounded-lg flex flex-col gap-2 items-start border border-gray-200">
          <p>Cover letter data is absent or expired.</p>
          <a href={`/jobs/${jobId}`} className="text-indigo-600 hover:text-indigo-800 font-medium transition-colors">
            Regenerate Cover Letter &rarr;
          </a>
        </div>
      </div>
    );
  }

  if (coverLetter.status === 'pending' || coverLetter.status === 'generating') {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4 mt-8 pt-8 border-t border-gray-100">
        <CircularProgress />
        <Typography variant="body1" className="text-gray-600">Generating your cover letter...</Typography>
      </div>
    );
  }

  if (coverLetter.status === 'failed') {
    return (
      <div className="p-4 bg-red-50 text-red-800 rounded-lg mt-8 pt-8 border-t border-gray-100">
        Cover letter generation failed.
      </div>
    );
  }

  return (
    <div className="mt-8 border-t border-gray-100 pt-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-gray-900">Cover Letter</h2>
        {!coverLetterExpired && (
          <div className="flex gap-3">
            <Button 
              variant="outlined" 
              size="small" 
              onClick={() => handleDownload('pdf')}
              sx={{ textTransform: 'none' }}
            >
              Download PDF
            </Button>
            <Button 
              variant="outlined" 
              size="small" 
              onClick={() => handleDownload('markdown')}
              sx={{ textTransform: 'none' }}
            >
              Download Markdown
            </Button>
          </div>
        )}
      </div>
      
      <div className="bg-gray-50 p-6 sm:p-8 rounded-xl border border-gray-200">
        <pre className="whitespace-pre-wrap font-sans text-gray-700 text-sm sm:text-base leading-relaxed">
          {coverLetter.content}
        </pre>
      </div>

      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={4000} 
        onClose={() => setSnackbar(prev => ({...prev, open: false}))}
      >
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </div>
  );
}
