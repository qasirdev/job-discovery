'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import ApplicationBoard, { Application } from '../../components/ApplicationBoard';
import { CircularProgress } from '@mui/material';

export default function ApplicationsPage() {
  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    return `${cleanBase}${endpoint}`;
  };

  const { data: applications, isLoading, error } = useQuery<Application[]>({
    queryKey: ['applications'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/applications'));
      if (!res.ok) throw new Error('Failed to load applications');
      const rawData = await res.json();
      
      // Map ApplicationWithJob from backend to expected Application interface
      return rawData.map((item: any) => ({
        id: item.id,
        job_id: item.job_id,
        job_title: item.job?.title || 'Unknown Title',
        company: item.job?.company || 'Unknown Company',
        status: item.status,
        applied_at: item.created_at, // Use created_at if applied_at is null
        notes: item.notes,
      }));
    }
  });

  return (
    <main className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-extrabold text-gray-900 mb-8">Application Tracking</h1>
        
        {isLoading ? (
          <div className="flex justify-center items-center h-64">
            <CircularProgress />
          </div>
        ) : error ? (
          <div className="p-4 bg-red-50 text-red-800 rounded">
            Failed to load applications.
          </div>
        ) : (
          <ApplicationBoard applications={applications || []} />
        )}
      </div>
    </main>
  );
}
