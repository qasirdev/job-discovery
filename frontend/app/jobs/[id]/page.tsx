'use client';

import React, { useState, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, useRouter } from 'next/navigation';
import { Snackbar, Alert } from '@mui/material';
import CoverLetterViewer from '../../../components/CoverLetterViewer';
import QuestionAnswerPanel from '../../../components/QuestionAnswerPanel';

export default function JobDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();
  const queryClient = useQueryClient();
  const qaPanelRef = useRef<HTMLDivElement>(null);
  
  const scrollToQA = () => {
    qaPanelRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const [existingApplicationId, setExistingApplicationId] = useState<string | null>(null);
  const [interviewPrepBlocked, setInterviewPrepBlocked] = useState(false);
  const [showCoverLetter, setShowCoverLetter] = useState(false);
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

  const { data: job, isLoading: jobLoading, error } = useQuery({
    queryKey: ['job', id],
    queryFn: async () => {
      const res = await fetch(getApiUrl(`/jobs/${id}`));
      if (!res.ok) throw new Error('Failed to load job');
      return res.json();
    }
  });

  const { data: cvStatus, isLoading: cvStatusLoading } = useQuery({
    queryKey: ['cv-status'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/cv/status'));
      if (!res.ok) return { embedding_status: 'pending' };
      return res.json();
    }
  });

  const { data: companyResearch } = useQuery({
    queryKey: ['company-research', job?.company_slug],
    queryFn: async () => {
      if (!job?.company_slug) return null;
      const res = await fetch(getApiUrl(`/company-research?company_slug=${job.company_slug}`));
      if (!res.ok) return null;
      return res.json();
    },
    enabled: !!job?.company_slug,
  });

  const { data: interviewPrep } = useQuery({
    queryKey: ['interview-prep', id],
    queryFn: async () => {
      const res = await fetch(getApiUrl(`/interview-prep/${id}`));
      if (!res.ok) return null;
      return res.json();
    },
    refetchInterval: (query) => {
      // Poll every 3 seconds if status is generating or pending
      const status = query.state.data?.status;
      return (status === 'generating' || status === 'pending') ? 3000 : false;
    }
  });

  const { data: featureFlags, isLoading: flagsLoading } = useQuery({
    queryKey: ['feature-flags'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/feature-flags'));
      if (!res.ok) return { feature_interview_prep: false };
      return res.json();
    }
  });

  const isLoading = jobLoading || cvStatusLoading || flagsLoading;

  const toggleSave = useMutation({
    mutationFn: async () => {
      const method = job?.saved ? 'DELETE' : 'POST';
      const res = await fetch(getApiUrl(`/jobs/${id}/save`), { method });
      if (!res.ok) throw new Error('Failed to save job');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['job', id] });
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
    }
  });

  const logApp = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl(`/applications/`), { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_id: id })
      });
      if (!res.ok) {
        if (res.status === 409) {
          const errData = await res.json();
          setExistingApplicationId(errData.detail?.existing_id || errData.existing_id);
          throw new Error('Application already logged. View it now.');
        }
        throw new Error('Failed to log application');
      }
      return res.json();
    },
    onSuccess: (data) => {
      setExistingApplicationId(data.id);
      setSnackbar({ open: true, message: 'Application logged successfully!', severity: 'success' });
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.message, severity: 'error' });
    }
  });

  const generateCoverLetter = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl(`/cover-letter/${id}`), { method: 'POST' });
      if (!res.ok) throw new Error('Failed to start cover letter generation');
      return res.json();
    },
    onSuccess: () => {
      setSnackbar({ open: true, message: 'Cover letter generation started!', severity: 'success' });
      setShowCoverLetter(true);
    },
    onError: (error: any) => {
      setSnackbar({ open: true, message: error.message, severity: 'error' });
    }
  });

  const generateInterviewPrep = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl(`/interview-prep/${id}`), { method: 'POST' });
      if (!res.ok) {
        if (res.status === 503) {
          throw new Error('503');
        }
        throw new Error('Failed to start interview prep');
      }
      return res.json();
    },
    onSuccess: () => {
      setSnackbar({ open: true, message: 'Interview prep generation started!', severity: 'success' });
      queryClient.invalidateQueries({ queryKey: ['interview-prep', id] });
    },
    onError: (error: any) => {
      if (error.message === '503') {
        setInterviewPrepBlocked(true);
        setSnackbar({ open: true, message: 'Interview prep is not yet available.', severity: 'error' });
      } else {
        setSnackbar({ open: true, message: error.message, severity: 'error' });
      }
    }
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white p-8 rounded-2xl shadow-sm text-center max-w-md">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Job Not Found</h1>
          <p className="text-gray-500 mb-6">We couldn't find the job you're looking for. It might have been removed or the ID is incorrect.</p>
          <button onClick={() => router.back()} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">Go Back</button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Navigation */}
        <button onClick={() => router.back()} className="text-sm text-gray-500 hover:text-gray-900 transition flex items-center gap-2">
          &larr; Back to Dashboard
        </button>

        {/* Header Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8 relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-50 rounded-bl-full -mr-16 -mt-16 transition-transform group-hover:scale-110"></div>
          
          <div className="relative z-10 flex flex-col sm:flex-row sm:items-start justify-between gap-6">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full uppercase tracking-wider">
                  {job.source}
                </span>
                {job.relevance_score !== null && (
                  <span className="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-full flex items-center gap-1">
                    Match: {Math.round(job.relevance_score * 100)}%
                  </span>
                )}
              </div>
              <h1 className="text-3xl font-extrabold text-gray-900 mb-2 leading-tight">{job.title}</h1>
              <div className="flex flex-wrap items-center gap-4 text-gray-600 text-sm">
                <div className="flex items-center gap-1.5 font-medium text-gray-900">
                  <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" /></svg>
                  {job.company}
                </div>
                {job.location && (
                  <div className="flex items-center gap-1.5">
                    <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                    {job.location}
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              <button 
                onClick={() => toggleSave.mutate()}
                disabled={toggleSave.isPending}
                className={`p-3 rounded-xl border transition-all ${job.saved ? 'bg-rose-50 border-rose-100 text-rose-600' : 'bg-white border-gray-200 text-gray-400 hover:border-gray-300 hover:text-gray-600'}`}
                title={job.saved ? "Unsave Job" : "Save Job"}
              >
                <svg className="w-6 h-6" fill={job.saved ? "currentColor" : "none"} viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={job.saved ? 1 : 2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>
          </div>
          
          {/* Action Bar */}
          <div className="mt-6 pt-6 border-t border-gray-100 flex flex-wrap items-center gap-3">
            <a 
              href={job.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="px-6 py-2.5 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors shadow-sm flex items-center gap-2"
            >
              Apply on {job.source}
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
            </a>
            
            {existingApplicationId === null ? (
              <button 
                onClick={() => logApp.mutate()}
                disabled={logApp.isPending}
                className="px-4 py-2.5 bg-indigo-50 text-indigo-700 text-sm font-medium rounded-lg hover:bg-indigo-100 transition-colors shadow-sm flex items-center gap-2"
                title="Log this application to track its status"
              >
                {logApp.isPending ? 'Logging...' : 'Log Application'}
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
              </button>
            ) : (
              <button 
                onClick={() => router.push('/applications/' + existingApplicationId)}
                className="px-4 py-2.5 bg-emerald-50 text-emerald-700 text-sm font-medium rounded-lg hover:bg-emerald-100 transition-colors shadow-sm flex items-center gap-2"
                title="View this application"
              >
                View Application
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
              </button>
            )}

            <button 
              onClick={scrollToQA}
              className="px-4 py-2.5 bg-sky-50 text-sky-700 text-sm font-medium rounded-lg hover:bg-sky-100 transition-colors shadow-sm flex items-center gap-2"
              title="Ask a question about this job"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              Ask Question
            </button>

            <div className="flex-1"></div>

            <button 
              disabled={cvStatus?.embedding_status !== 'ready' || generateCoverLetter.isPending}
              onClick={() => generateCoverLetter.mutate()}
              className={`px-4 py-2.5 text-sm font-medium rounded-lg flex items-center gap-2 transition-colors shadow-sm ${
                cvStatus?.embedding_status === 'ready' 
                  ? 'bg-gray-900 text-white hover:bg-gray-800' 
                  : 'bg-gray-50 text-gray-400 border border-gray-200 cursor-not-allowed'
              }`}
              title={cvStatus?.embedding_status === 'pending' ? "Cover letter generation is available from MVP2. CV embedding is not yet active." : "Generate Cover Letter"}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
              {generateCoverLetter.isPending ? 'Generating...' : 'Generate Cover Letter'}
            </button>

            <button 
              disabled={!featureFlags?.feature_interview_prep || interviewPrepBlocked || generateInterviewPrep.isPending}
              onClick={() => generateInterviewPrep.mutate()}
              className={`px-4 py-2.5 text-sm font-medium rounded-lg flex items-center gap-2 transition-colors shadow-sm ${
                featureFlags?.feature_interview_prep && !interviewPrepBlocked
                  ? 'bg-purple-50 text-purple-700 border border-purple-100 hover:bg-purple-100' 
                  : 'bg-gray-50 text-gray-400 border border-gray-200 cursor-not-allowed'
              }`}
              title={!featureFlags?.feature_interview_prep ? "Coming in MVP 3: AI Interview Prep Generation" : "Generate Interview Prep"}
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" /></svg>
              {!featureFlags?.feature_interview_prep ? 'Interview Prep — Available from MVP3' : ((generateInterviewPrep.isPending || interviewPrep?.status === 'generating' || interviewPrep?.status === 'pending') ? 'Generating...' : 'Generate Interview Prep')}
            </button>
          </div>
        </div>

        {/* Content Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
          <h2 className="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-100">Job Description</h2>
          <div className="prose prose-indigo max-w-none text-gray-600 text-sm sm:text-base leading-relaxed whitespace-pre-line">
            {job.description}
          </div>
          
          {showCoverLetter && (
            <CoverLetterViewer jobId={id} />
          )}

          {/* Company Research Section */}
          {(!companyResearch || companyResearch.status === 'skipped' || !companyResearch.data || Object.keys(companyResearch.data).length === 0) ? (
            <div className="mt-8 pt-6 border-t border-gray-100">
              <h2 className="text-xl font-bold text-gray-400 mb-2 cursor-not-allowed">Company Intelligence</h2>
              <div className="p-4 bg-gray-50 rounded-xl border border-gray-100">
                <p className="text-sm text-gray-400 italic">Company intelligence is not available for this listing...</p>
              </div>
            </div>
          ) : (
            <div className="mt-8 pt-6 border-t border-gray-100">
              <details className="group" open>
                <summary className="flex justify-between items-center font-medium cursor-pointer list-none">
                  <h2 className="text-xl font-bold text-gray-900">Company Intelligence</h2>
                  <span className="transition group-open:rotate-180">
                    <svg fill="none" height="24" shapeRendering="geometricPrecision" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                  </span>
                </summary>
                <div className="text-neutral-600 mt-3 group-open:animate-fadeIn">
                  <pre className="whitespace-pre-wrap font-sans text-sm sm:text-base leading-relaxed bg-gray-50 p-6 rounded-xl border border-gray-200">
                    {JSON.stringify(companyResearch.data, null, 2)}
                  </pre>
                </div>
              </details>
            </div>
          )}

          {/* Interview Prep Section */}
          {interviewPrep && interviewPrep.status === 'ready' && (
            <div className="mt-8 pt-6 border-t border-gray-100">
              <h2 className="text-xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-100">Interview Preparation</h2>
              
              {interviewPrep.questions && interviewPrep.questions.length > 0 && (
                <details className="group mb-6" open>
                  <summary className="flex justify-between items-center font-medium cursor-pointer list-none mb-4">
                    <h3 className="text-lg font-bold text-gray-800">Practice Questions</h3>
                    <span className="transition group-open:rotate-180">
                      <svg fill="none" height="24" shapeRendering="geometricPrecision" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div className="text-neutral-600 mt-3 group-open:animate-fadeIn space-y-4 pl-4">
                    <ul className="list-disc space-y-2">
                      {interviewPrep.questions.map((q: string, idx: number) => (
                        <li key={idx} className="text-gray-700 leading-relaxed">{q}</li>
                      ))}
                    </ul>
                  </div>
                </details>
              )}

              {interviewPrep.company_research && interviewPrep.company_research.intel && (
                <details className="group" open>
                  <summary className="flex justify-between items-center font-medium cursor-pointer list-none mb-4">
                    <h3 className="text-lg font-bold text-gray-800">Synthesized Intel</h3>
                    <span className="transition group-open:rotate-180">
                      <svg fill="none" height="24" shapeRendering="geometricPrecision" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" viewBox="0 0 24 24" width="24"><path d="M6 9l6 6 6-6"></path></svg>
                    </span>
                  </summary>
                  <div className="text-neutral-600 mt-3 group-open:animate-fadeIn">
                    <p className="whitespace-pre-wrap font-sans text-sm sm:text-base leading-relaxed bg-gray-50 p-6 rounded-xl border border-gray-200">
                      {interviewPrep.company_research.intel}
                    </p>
                  </div>
                </details>
              )}
            </div>
          )}

          <div ref={qaPanelRef} className="mt-8 pt-6 border-t border-gray-100">
            <QuestionAnswerPanel jobId={id} />
          </div>
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
