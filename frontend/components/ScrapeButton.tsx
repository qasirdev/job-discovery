'use client';
import React, { useState } from 'react';

export function ScrapeButton() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleScrape = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch('/api/v1/scrape/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ max_jobs: 5 })
      });
      const data = await res.json();
      setResult(`Scrape triggered! Check console.`);
      console.log('Scrape results:', data);
    } catch (err) {
      console.error(err);
      setResult('Error triggering scrape.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center gap-4">
      <button 
        onClick={handleScrape} 
        disabled={loading}
        className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? 'Scraping...' : 'Trigger Full Scrape'}
      </button>
      {result && <span className="text-sm text-gray-600">{result}</span>}
    </div>
  );
}
