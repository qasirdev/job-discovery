'use client';
import React, { useState } from 'react';

interface ScrapeButtonProps {
  onScrapeComplete?: () => void;
}

export function ScrapeButton({ onScrapeComplete }: ScrapeButtonProps) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleScrape = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('/api/v1/scrape/', {
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
