'use client';

import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Box, Typography, Button, CircularProgress, Alert } from '@mui/material';

interface CoverLetterViewerProps {
  job_id: string;
}

export default function CoverLetterViewer({ job_id }: CoverLetterViewerProps) {
  const queryClient = useQueryClient();
  const [downloading, setDownloading] = useState<'pdf' | 'markdown' | null>(null);
  const [downloadError, setDownloadError] = useState<string | null>(null);

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const { data, isLoading, error } = useQuery({
    queryKey: ['cover-letter', job_id],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/cover-letter/${job_id}`);
      if (!res.ok) {
        if (res.status === 404) return null;
        throw new Error('Failed to fetch cover letter');
      }
      return res.json();
    },
    refetchInterval: (query) => {
      const d = query.state.data as any;
      if (d && (d.status === 'pending' || d.status === 'generating')) {
        return 3000; // Poll every 3 seconds
      }
      return false;
    }
  });

  const handleDownload = async (format: 'pdf' | 'markdown') => {
    setDownloading(format);
    setDownloadError(null);

    try {
      const res = await fetch(`${getApiBase()}/cover-letter/${job_id}/export?format=${format}`);
      
      if (!res.ok) {
        if (res.status === 422) {
          setDownloadError('Cover letter is no longer available. Please regenerate it.');
          queryClient.invalidateQueries({ queryKey: ['cover-letter', job_id] });
          return;
        }
        throw new Error('Download failed. Please try again.');
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `cover-letter-${job_id}.${format === 'markdown' ? 'md' : 'pdf'}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setDownloadError(err.message || 'Download failed. Please try again.');
    } finally {
      setDownloading(null);
    }
  };

  if (isLoading) return <CircularProgress size={24} />;
  
  if (error) return <Alert severity="error">{(error as Error).message}</Alert>;

  if (!data) return null;

  if (data.status === 'pending' || data.status === 'generating') {
    return (
      <Box className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg border border-gray-200">
        <CircularProgress size={20} />
        <Typography variant="body2">Generating cover letter...</Typography>
      </Box>
    );
  }

  if (data.status === 'ready') {
    return (
      <Box className="p-4 bg-white rounded-lg border border-gray-200 shadow-sm mt-4">
        <Typography variant="h6" className="mb-4 font-bold">Cover Letter</Typography>
        
        <Box className="bg-gray-50 p-4 rounded text-sm whitespace-pre-wrap font-serif border border-gray-100 max-h-96 overflow-y-auto mb-4">
          {data.content}
        </Box>

        {downloadError && (
          <Alert severity="error" className="mb-4">
            {downloadError}
          </Alert>
        )}

        <div className="flex gap-3">
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => handleDownload('pdf')}
            disabled={downloading !== null}
          >
            {downloading === 'pdf' ? 'Downloading...' : 'Download PDF'}
          </Button>
          <Button 
            variant="outlined" 
            color="primary"
            onClick={() => handleDownload('markdown')}
            disabled={downloading !== null}
          >
            {downloading === 'markdown' ? 'Downloading...' : 'Download Markdown'}
          </Button>
        </div>
      </Box>
    );
  }

  return null;
}
