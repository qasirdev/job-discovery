'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Alert, Button, CircularProgress } from '@mui/material';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { POLLING_INTERVAL_MS } from '../lib/constants';

export default function OnboardingBanner() {
  const pathname = usePathname();
  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ['profile'],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/profile`);
      if (res.status === 404) return null;
      if (!res.ok) throw new Error('Failed to fetch profile');
      return res.json();
    },
    retry: false,
  });

    const { data: cvStatus, isLoading: cvLoading } = useQuery({
    queryKey: ['cv-status'],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/cv/status`);
      if (res.status === 404) return { embedding_status: 'none' };
      if (!res.ok) throw new Error('Failed to fetch cv status');
      return res.json();
    },
    retry: false,
    refetchInterval: (query) => {
      const data = query.state.data as any;
      if (data && (data.embedding_status === 'pending' || data.embedding_status === 'processing')) {
        return POLLING_INTERVAL_MS;
      }
      return false;
    },
  });

  if (pathname === '/onboarding') {
    return null;
  }

  if (profileLoading || cvLoading) {
    return null; // Suppress until resolved to prevent flashing
  }

  // 1. profile missing
  if (!profile) {
    return (
      <Alert 
        severity="info" 
        className="mb-4"
        action={
          <Link href="/onboarding" passHref>
            <Button color="inherit" size="small">
              Start Onboarding
            </Button>
          </Link>
        }
      >
        Complete your profile
      </Alert>
    );
  }

  // 2. CV not uploaded
  if (!cvStatus || cvStatus.embedding_status === 'none' || cvStatus.embedding_status === 'failed') {
    return (
      <Alert 
        severity="warning" 
        className="mb-4"
        action={
          <Link href="/onboarding" passHref>
            <Button color="inherit" size="small">
              Upload CV
            </Button>
          </Link>
        }
      >
        Upload your CV
      </Alert>
    );
  }

  // 3. Embedding pending
  if (cvStatus.embedding_status === 'pending') {
    return (
      <Alert severity="info" className="mb-4">
        CV uploaded — embedding available from MVP2
      </Alert>
    );
  }

  // 4. Embedding processing
  if (cvStatus.embedding_status === 'processing') {
    return (
      <Alert severity="info" className="mb-4 flex items-center gap-2">
        <CircularProgress size={16} color="inherit" />
        Processing your CV — this takes about 30 seconds
      </Alert>
    );
  }

  // 5. Ready
  return null;
}
