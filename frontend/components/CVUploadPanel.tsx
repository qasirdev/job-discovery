'use client';

import React, { useState, useRef } from 'react';
import { Box, Button, Typography, LinearProgress, Alert } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { POLLING_INTERVAL_MS } from '../lib/constants';

interface CVUploadPanelProps {
  currentFilename?: string;
  onUpload: (file: File) => Promise<void>;
}

export default function CVUploadPanel({ currentFilename, onUpload }: CVUploadPanelProps) {
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const { data: statusData } = useQuery({
    queryKey: ['cv-status'],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/cv/status`);
      if (!res.ok) throw new Error('Failed to fetch status');
      return res.json();
    },
    // Poll every 5s if we are currently processing or pending
    refetchInterval: (query) => {
      const data = query.state.data as any;
      if (data && (data.embedding_status === 'pending' || data.embedding_status === 'processing')) {
        return POLLING_INTERVAL_MS;
      }
      return false;
    },
  });

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // reset input so same file can be selected again if needed
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }

    setUploadError(null);
    setUploading(true);
    
    try {
      await onUpload(file);
    } catch (err: any) {
      setUploadError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const getStatusMessage = () => {
    if (!statusData) return null;
    if (statusData.message === 'CV received. Embedding available from MVP 2.') {
      return statusData.message;
    }
    if (statusData.embedding_status === 'ready') {
      return 'CV is ready and embedded.';
    }
    if (statusData.embedding_status === 'pending' || statusData.embedding_status === 'processing') {
      return 'CV uploaded — processing...';
    }
    return null;
  };

  return (
    <Box className="flex flex-col gap-4 max-w-md bg-white p-6 rounded-lg shadow-sm border border-gray-200 mt-6">
      <Typography variant="h6" className="mb-2">CV Upload</Typography>

      {currentFilename && (
        <Typography variant="body2" className="text-gray-600">
          Current CV: <span className="font-semibold">{currentFilename}</span>
        </Typography>
      )}

      <div className="flex flex-col gap-2 mt-2">
        <input
          type="file"
          accept=".pdf,.docx"
          style={{ display: 'none' }}
          ref={fileInputRef}
          onChange={handleFileChange}
        />
        <Button 
          variant="outlined" 
          color="primary" 
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
        >
          {uploading ? 'Uploading...' : 'Select File (.pdf, .docx)'}
        </Button>
      </div>

      {uploading && <LinearProgress className="mt-2" />}

      {uploadError && (
        <Alert severity="error" className="mt-2">
          {uploadError}
        </Alert>
      )}

      {getStatusMessage() && !uploading && (
        <Alert severity="info" className="mt-2">
          {getStatusMessage()}
        </Alert>
      )}
    </Box>
  );
}
