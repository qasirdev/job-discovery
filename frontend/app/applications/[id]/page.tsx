'use client';

import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useRouter } from 'next/navigation';
import { CircularProgress, Button, TextField, Select, MenuItem, Snackbar, Alert } from '@mui/material';

const columns = [
  'draft',
  'applied',
  'awaiting_response',
  'interviewing',
  'offered',
  'rejected',
  'withdrawn',
];

const columnTitles: Record<string, string> = {
  draft: 'Draft',
  applied: 'Applied',
  awaiting_response: 'Awaiting Response',
  interviewing: 'Interviewing',
  offered: 'Offered',
  rejected: 'Rejected',
  withdrawn: 'Withdrawn',
};

export default function ApplicationDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const queryClient = useQueryClient();

  const [notes, setNotes] = useState('');
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

  const { data: application, isLoading, error } = useQuery({
    queryKey: ['application', id],
    queryFn: async () => {
      const res = await fetch(getApiUrl(`/applications/${id}`));
      if (!res.ok) throw new Error('Failed to load application');
      return res.json();
    }
  });

  useEffect(() => {
    if (application?.notes) {
      setNotes(application.notes);
    }
  }, [application]);

  const { data: featureFlags } = useQuery({
    queryKey: ['feature-flags'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/feature-flags'));
      if (!res.ok) return { feature_application_assistant: false, feature_interview_prep: false };
      return res.json();
    }
  });

  const updateApp = useMutation({
    mutationFn: async (data: { status?: string; notes?: string }) => {
      const res = await fetch(getApiUrl(`/applications/${id}`), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Failed to update application');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['application', id] });
      queryClient.invalidateQueries({ queryKey: ['applications'] });
      setSnackbar({ open: true, message: 'Application updated successfully!', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.message, severity: 'error' });
    }
  });

  const triggerAssistant = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl(`/applications/${id}/assistant`), {
        method: 'POST',
      });
      if (!res.ok) {
        if (res.status === 503) {
          throw new Error('Application Assistant is not available right now.');
        }
        throw new Error('Failed to trigger Application Assistant');
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['application', id] });
      setSnackbar({ open: true, message: 'Application Assistant started! The package will appear when ready.', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.message, severity: 'error' });
    }
  });

  const triggerInterviewPrep = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl(`/applications/${id}/interview-prep`), {
        method: 'POST',
      });
      if (!res.ok) {
        if (res.status === 503) {
          throw new Error('Interview Prep Assistant is not available right now.');
        }
        throw new Error('Failed to trigger Interview Prep Assistant');
      }
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['application', id] });
      setSnackbar({ open: true, message: 'Interview Prep started! Data will appear when ready.', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.message, severity: 'error' });
    }
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <CircularProgress />
      </div>
    );
  }

  if (error || !application) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-sm text-center max-w-md">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Application Not Found</h1>
          <p className="text-gray-500 mb-6">We couldn't find this application.</p>
          <Button onClick={() => router.back()} variant="contained" color="primary">Go Back</Button>
        </div>
      </div>
    );
  }

  const job = application.job;

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <button onClick={() => router.back()} className="text-sm text-gray-500 hover:text-gray-900 transition flex items-center gap-2">
          &larr; Back to Applications
        </button>

        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
          <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-6">
            <div>
              <h1 className="text-3xl font-extrabold text-gray-900 mb-2 leading-tight">{job?.title || 'Unknown Role'}</h1>
              <div className="flex flex-wrap items-center gap-4 text-gray-600 text-sm">
                <div className="font-medium text-gray-900">{job?.company || 'Unknown Company'}</div>
                {job?.location && <div>{job.location}</div>}
              </div>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              <Select
                value={application.status}
                size="small"
                onChange={(e) => updateApp.mutate({ status: e.target.value })}
                disabled={updateApp.isPending}
                sx={{ minWidth: 160 }}
              >
                {columns.map(status => (
                  <MenuItem key={status} value={status}>
                    {columnTitles[status]}
                  </MenuItem>
                ))}
              </Select>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-gray-100">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Application Notes</h2>
            <TextField
              fullWidth
              multiline
              rows={6}
              variant="outlined"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Keep track of interviews, recruiter contacts, etc."
            />
            <div className="mt-4 flex justify-end">
              <Button 
                variant="contained" 
                color="primary"
                onClick={() => updateApp.mutate({ notes })}
                disabled={updateApp.isPending || notes === application.notes}
                sx={{ textTransform: 'none' }}
              >
                {updateApp.isPending ? 'Saving...' : 'Save Notes'}
              </Button>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-gray-100">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-gray-900">Application Package</h2>
              <div className="flex gap-2">
                <Button
                  variant="outlined"
                  color="secondary"
                  onClick={() => triggerInterviewPrep.mutate()}
                  disabled={triggerInterviewPrep.isPending || !featureFlags?.feature_interview_prep}
                  sx={{ textTransform: 'none' }}
                  title={!featureFlags?.feature_interview_prep ? "Available in MVP 4+" : "Trigger Interview Prep"}
                >
                  {!featureFlags?.feature_interview_prep ? 'Prep Unavailable' : (triggerInterviewPrep.isPending ? 'Starting...' : 'Generate Interview Prep')}
                </Button>
                <Button
                  variant="outlined"
                  color="primary"
                  onClick={() => triggerAssistant.mutate()}
                  disabled={triggerAssistant.isPending || !featureFlags?.feature_application_assistant}
                  sx={{ textTransform: 'none' }}
                  title={!featureFlags?.feature_application_assistant ? "Available in MVP 4+" : "Trigger the Application Assistant to synthesize documents"}
                >
                  {!featureFlags?.feature_application_assistant ? 'Assistant Unavailable' : (triggerAssistant.isPending ? 'Starting...' : 'Generate Application Package')}
                </Button>
              </div>
            </div>
            {application.compound_package ? (
              <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
                <h3 className="font-semibold text-gray-800 mb-2">Summary</h3>
                <p className="text-gray-700 mb-4">{application.compound_package.summary}</p>
                
                <h3 className="font-semibold text-gray-800 mb-2">Cover Letter Reference</h3>
                <p className="text-gray-700 mb-4">{application.compound_package.cover_letter_ref}</p>
                
                {application.compound_package.interview_highlights && (
                  <>
                    <h3 className="font-semibold text-gray-800 mb-2">Interview Highlights</h3>
                    <ul className="list-disc pl-5 mb-4 space-y-1">
                      {application.compound_package.interview_highlights.map((highlight: string, idx: number) => (
                        <li key={idx} className="text-gray-700">{highlight}</li>
                      ))}
                    </ul>
                  </>
                )}
                
                {application.compound_package.company_culture_notes && (
                  <>
                    <h3 className="font-semibold text-gray-800 mb-2">Company Culture Notes</h3>
                    <p className="text-gray-700">{application.compound_package.company_culture_notes}</p>
                  </>
                )}
              </div>
            ) : (
              <div className="bg-gray-50 p-6 rounded-xl border border-gray-200 text-center">
                <p className="text-gray-500 italic">No application package generated yet. Click "Generate Application Package" to synthesize data.</p>
              </div>
            )}
          </div>
        </div>
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
    </main>
  );
}
