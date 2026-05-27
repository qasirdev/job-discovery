'use client';

import React from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';

export default function InterviewPrepPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  const { data, isLoading, error } = useQuery({
    queryKey: ['interview-prep', id],
    queryFn: async () => {
      const res = await fetch(getApiUrl(`/interview-prep/${id}`));
      if (!res.ok) throw new Error('Failed to load interview prep');
      return res.json();
    }
  });

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <button onClick={() => router.back()} className="text-sm text-gray-500 hover:text-gray-900 transition flex items-center gap-2">
          &larr; Back to Job Detail
        </button>
        
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-100">Interview Preparation</h1>
          
          {isLoading ? (
            <div className="flex justify-center p-8">
              <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
            </div>
          ) : error ? (
            <div className="p-4 bg-rose-50 text-rose-700 rounded-lg">
              Failed to load interview preparation. Please try generating it again.
            </div>
          ) : !data || data.status !== 'ready' ? (
            <div className="p-8 text-center text-gray-500 border border-dashed border-gray-300 rounded-xl">
              Interview prep is currently generating or not available.
            </div>
          ) : (
            <div className="space-y-8">
              {data.questions && data.questions.length > 0 && (
                <div>
                  <h3 className="text-lg font-bold text-gray-800 mb-3">Practice Questions</h3>
                  <ul className="list-disc pl-5 space-y-2 text-gray-700">
                    {data.questions.map((q: string, idx: number) => (
                      <li key={idx}>{q}</li>
                    ))}
                  </ul>
                </div>
              )}
              {data.company_research && data.company_research.intel && (
                <div>
                  <h3 className="text-lg font-bold text-gray-800 mb-3">Company Intel</h3>
                  <div className="bg-gray-50 p-6 rounded-xl border border-gray-200 text-gray-700 whitespace-pre-wrap">
                    {data.company_research.intel}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
