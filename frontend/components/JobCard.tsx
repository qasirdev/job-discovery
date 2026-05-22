import React, { useState } from 'react';

interface JobCardProps {
  id: string;
  title: string;
  company: string;
  location?: string | null;
  description: string;
  url: string;
  source: string;
}

export function JobCard({ id, title, company, location, description, url, source }: JobCardProps) {
  const [loading, setLoading] = useState(false);
  const [coverLetterData, setCoverLetterData] = useState<{ cover_letter: string, ats_match: number, score: number } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string | null>(null);

  const handleGenerateLetter = async () => {
    setLoading(true);
    setError(null);
    setCoverLetterData(null);
    setStatus(null);

    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
      const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
      const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
      const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;

      const res = await fetch(`${cleanBase}/jobs/${id}/process`, {
        method: 'POST',
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      
      if (data.status === 'success') {
        setCoverLetterData(data);
      } else if (data.status === 'filtered') {
        setStatus(`Job scored ${data.score}. Not relevant enough for a cover letter.`);
      } else if (data.status === 'rejected') {
        setStatus(`Security rejection: ${data.reason}`);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to generate cover letter.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow flex flex-col">
      <h3 className="text-xl font-bold">{title}</h3>
      <p className="text-gray-600">{company} {location && `- ${location}`}</p>
      <p className="mt-2 text-sm text-gray-800 line-clamp-3">{description}</p>
      
      <div className="mt-4 mb-2">
        <button
          onClick={handleGenerateLetter}
          disabled={loading}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded text-sm transition-colors disabled:opacity-50"
        >
          {loading ? 'Processing via AI Orchestrator...' : 'Generate Cover Letter'}
        </button>
      </div>

      {status && (
        <div className="mt-2 text-sm p-2 bg-yellow-50 text-yellow-800 border border-yellow-200 rounded">
          {status}
        </div>
      )}

      {error && (
        <div className="mt-2 text-sm p-2 bg-red-50 text-red-800 border border-red-200 rounded">
          {error}
        </div>
      )}

      {coverLetterData && (
        <div className="mt-4 p-3 bg-indigo-50 border border-indigo-100 rounded-md">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs font-bold text-indigo-800 uppercase">AI Generated Match</span>
            <span className="text-xs bg-indigo-200 text-indigo-800 py-1 px-2 rounded-full">
              Score: {coverLetterData.score} | ATS: {(coverLetterData.ats_match * 100).toFixed(0)}%
            </span>
          </div>
          <p className="text-xs text-gray-700 whitespace-pre-wrap max-h-40 overflow-y-auto custom-scrollbar">
            {coverLetterData.cover_letter}
          </p>
        </div>
      )}

      <div className="mt-auto pt-4 flex justify-between items-center">
        <span className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-600 uppercase tracking-wider">{source}</span>
        <a href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-sm font-medium">
          View Job
        </a>
      </div>
    </div>
  );
}
