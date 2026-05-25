'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { CircularProgress } from '@mui/material';
import RecruiterCard, { Recruiter } from '../../components/RecruiterCard';

export default function RecruitersPage() {
  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    return `${cleanBase}${endpoint}`;
  };

  const { data: recruiters, isLoading, error } = useQuery<Recruiter[]>({
    queryKey: ['recruiters'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/recruiters'));
      if (!res.ok) throw new Error('Failed to load recruiters');
      return res.json();
    }
  });

  return (
    <main className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-extrabold text-gray-900 mb-8">Recruiters Network</h1>
        
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <CircularProgress />
          </div>
        ) : error ? (
          <div className="p-4 bg-red-50 text-red-800 rounded">
            Failed to load recruiters.
          </div>
        ) : !recruiters || recruiters.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-2xl border border-gray-100">
            <h3 className="text-lg font-medium text-gray-900 mb-2">No recruiters found</h3>
            <p className="text-gray-500">Recruiters will appear here as you log interactions.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recruiters.map((recruiter) => (
              <RecruiterCard key={recruiter.id} recruiter={recruiter} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
