'use client';

import React, { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useParams, useRouter } from 'next/navigation';
import { CircularProgress, Button, Snackbar, Alert, Typography } from '@mui/material';

export default function InterviewPrepPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const queryClient = useQueryClient();
  
  const [prepExpired, setPrepExpired] = useState(false);
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error'}>({
    open: false, message: '', severity: 'success'
  });

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  const { data: interviewPrep, isLoading, error } = useQuery({
    queryKey: ['interview-prep', id],
    queryFn: async () => {
      const res = await fetch(getApiUrl(`/interview-prep/${id}`));
      if (!res.ok) {
        if (res.status === 404 || res.status === 422) {
          setPrepExpired(true);
        }
        throw new Error('Failed to load interview prep');
      }
      return res.json();
    },
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === 'pending' || status === 'generating') {
        const count = query.state.dataUpdateCount || 0;
        return Math.min(3000 * Math.pow(1.5, count), 30000);
      }
      return false;
    },
    retry: false
  });

  const handleDownload = async (format: 'pdf' | 'markdown') => {
    try {
      const res = await fetch(getApiUrl(`/interview-prep/${id}/export?format=${format}`));
      
      if (!res.ok) {
        if (res.status === 422) {
          queryClient.invalidateQueries({ queryKey: ['interview-prep', id] });
          setPrepExpired(true);
          setSnackbar({ open: true, message: 'Interview prep is no longer available. Please regenerate it.', severity: 'error' });
          return;
        }
        throw new Error('Download failed');
      }

      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `interview-prep.${format === 'markdown' ? 'md' : 'pdf'}`;
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err: any) {
      setSnackbar({ open: true, message: 'Download failed. Please try again.', severity: 'error' });
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <button onClick={() => router.back()} className="text-sm text-gray-500 hover:text-gray-900 transition flex items-center gap-2">
          &larr; Back to Job Detail
        </button>
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
          
          <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-100">
            <h1 className="text-2xl font-bold text-gray-900">Interview Preparation</h1>
            {interviewPrep?.status === 'ready' && !prepExpired && (
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

          {isLoading ? (
            <div className="flex justify-center items-center py-12">
              <CircularProgress />
            </div>
          ) : prepExpired || error || !interviewPrep ? (
            <div className="mt-4">
              <div className="p-4 bg-gray-50 text-gray-700 rounded-lg flex flex-col gap-2 items-start border border-gray-200">
                <p>Interview prep data is absent or expired.</p>
                <a href={`/jobs/${id}`} className="text-indigo-600 hover:text-indigo-800 font-medium transition-colors">
                  Regenerate Interview Prep &rarr;
                </a>
              </div>
            </div>
          ) : (interviewPrep.status === 'pending' || interviewPrep.status === 'generating') ? (
            <div className="flex flex-col items-center justify-center py-12 space-y-4 mt-4">
              <CircularProgress />
              <Typography variant="body1" className="text-gray-600">Generating your interview prep...</Typography>
            </div>
          ) : interviewPrep.status === 'failed' ? (
            <div className="p-4 bg-red-50 text-red-800 rounded-lg mt-4 border border-red-100">
              Interview prep generation failed.
            </div>
          ) : (
            <div className="mt-6 space-y-8">
              {interviewPrep.questions && interviewPrep.questions.length > 0 && (
                <details className="group" open>
                  <summary className="flex justify-between items-center font-medium cursor-pointer list-none mb-4">
                    <h2 className="text-xl font-bold text-gray-800">Practice Questions</h2>
                    <span className="transition group-open:rotate-180">
                      <svg fill="none" height="24" shapeRendering="geometricPrecision" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div className="text-neutral-600 mt-3 group-open:animate-fadeIn space-y-4 pl-4">
                    <ul className="list-disc space-y-2">
                      {interviewPrep.questions.map((q: any, idx: number) => (
                        <li key={idx} className="text-gray-700 leading-relaxed">{typeof q === 'string' ? q : q.question}</li>
                      ))}
                    </ul>
                  </div>
                </details>
              )}

              {interviewPrep.company_research && (
                <details className="group" open>
                  <summary className="flex justify-between items-center font-medium cursor-pointer list-none mb-4">
                    <h2 className="text-xl font-bold text-gray-800">Company Intelligence</h2>
                    <span className="transition group-open:rotate-180">
                      <svg fill="none" height="24" shapeRendering="geometricPrecision" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div className="text-neutral-600 mt-3 group-open:animate-fadeIn">
                    <pre className="whitespace-pre-wrap font-sans text-sm sm:text-base leading-relaxed bg-gray-50 p-6 rounded-xl border border-gray-200">
                      {interviewPrep.company_research.intel || JSON.stringify(interviewPrep.company_research, null, 2)}
                    </pre>
                  </div>
                </details>
              )}
            </div>
          )}

        </div>
      </div>

      <Snackbar 
        open={snackbar.open} 
        autoHideDuration={4000} 
        onClose={() => setSnackbar(prev => ({...prev, open: false}))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
    </main>
  );
}
