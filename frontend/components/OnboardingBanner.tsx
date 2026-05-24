'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Alert, Button, CircularProgress } from '@mui/material';
import Link from 'next/link';

export default function OnboardingBanner() {
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
  });

  if (profileLoading || cvLoading) {
    return null; // Suppress until resolved to prevent flashing
  }

  // 1. profile 404 or null
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
        Complete your profile to get started
      </Alert>
    );
  }

  // 2. profile exists but cv_status != ready
  if (!cvStatus || cvStatus.embedding_status !== 'ready') {
    // If it's the stub message (e.g. pending but "Embedding available from MVP 2"),
    // wait, the spec says "cv_status != ready: show banner 'Upload your CV to enable AI features'".
    // What if MVP 1 stub keeps it at 'pending'? The banner would stay unless we consider the stub.
    // The spec says "until embedding_status = ready or the MVP1 stub message applies".
    // For now, let's just stick to the spec text: "profile exists but cv_status != ready"
    
    // Check if it's the MVP1 stub where we don't need to ask them to upload anymore.
    // The spec for cv.py: returns {embedding_status: 'pending', message: 'CV received. Embedding available from MVP 2.'}
    if (cvStatus?.message === 'CV received. Embedding available from MVP 2.') {
      return null;
    }

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
        Upload your CV to enable AI features
      </Alert>
    );
  }

  // 3. both ready
  return null;
}
