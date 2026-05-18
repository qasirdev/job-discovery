'use client';
import React, { useState } from 'react';

interface ScrapeButtonProps {
  onScrapeComplete?: () => void;
}

export function ScrapeButton({ onScrapeComplete }: ScrapeButtonProps) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const getApiUrl = (endpoint: string): string => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  const handleScrape = async () => {
    setLoading(true);
    setResult(null);
    try {
      const url = getApiUrl('/scrape/');
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_jobs: 5 }),
      });

      const data = await res.json();
      setResult('Scraping completed!');
      console.log('Scrape results:', data);
      if (onScrapeComplete) {
        onScrapeComplete();
      }
    } catch (err) {
      console.error(err);
      setResult('Error triggering scrape.');
    } finally {
      setLoading(false);
      setTimeout(() => setResult(null), 3000);
    }
  };

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={handleScrape}
        disabled={loading}
        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50 font-medium transition duration-150 ease-in-out"
      >
        {loading ? 'Scraping...' : 'Trigger Full Scrape'}
      </button>
      {result && <span className="text-sm font-medium text-green-600 animate-pulse">{result}</span>}
    </div>
  );
}
