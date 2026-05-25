'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { CircularProgress } from '@mui/material';
import AdminPanel from '../../components/AdminPanel';
import { useRouter } from 'next/navigation';

export default function AdminPage() {
  const router = useRouter();

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    return `${cleanBase}${endpoint}`;
  };

  const { data: featureFlags, isLoading, error } = useQuery({
    queryKey: ['feature-flags'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/feature-flags'));
      if (!res.ok) throw new Error('Failed to load feature flags');
      return res.json();
    }
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <CircularProgress />
      </div>
    );
  }

  if (error || !featureFlags?.feature_admin_panel) {
    // If flag is false or missing, don't show the admin panel
    return (
      <div className="min-h-screen flex items-center justify-center p-4 bg-gray-50">
        <div className="text-center bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-md">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h2>
          <p className="text-gray-500 mb-6">This feature is currently hidden behind a feature flag.</p>
          <button onClick={() => router.push('/')} className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
            Return to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Admin Control Panel</h1>
          <p className="text-gray-500">Developer mode dashboard for background task visibility.</p>
        </div>
        
        <AdminPanel />
      </div>
    </main>
  );
}
