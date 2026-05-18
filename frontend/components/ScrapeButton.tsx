'use client';
import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

interface ScrapeButtonProps {
  onScrapeComplete?: () => void;
}

export function ScrapeButton({ onScrapeComplete }: ScrapeButtonProps) {
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const getApiUrl = (endpoint: string): string => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  const scrapeMutation = useMutation({
    mutationFn: async () => {
      const url = getApiUrl('/scrape/');
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_jobs: 5 }),
      });
      if (!res.ok) {
        throw new Error('Scraping request failed');
      }
      return res.json();
    },
    onSuccess: (data) => {
      console.log('Scrape results:', data);
      setSuccessMsg('Scraping completed!');
      if (onScrapeComplete) {
        onScrapeComplete();
      }
      setTimeout(() => setSuccessMsg(null), 3000);
    },
    onError: (err) => {
      console.error(err);
      setSuccessMsg('Error triggering scrape.');
      setTimeout(() => setSuccessMsg(null), 3000);
    },
  });

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={() => scrapeMutation.mutate()}
        disabled={scrapeMutation.isPending}
        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 font-medium transition duration-150 ease-in-out"
      >
        {scrapeMutation.isPending ? 'Scraping...' : 'Trigger Full Scrape'}
      </button>
      {successMsg && <span className="text-sm font-medium text-green-600 animate-pulse">{successMsg}</span>}
    </div>
  );
}
