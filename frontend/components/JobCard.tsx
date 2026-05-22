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

  // Q&A State
  const [question, setQuestion] = useState("");
  const [qaLoading, setQaLoading] = useState(false);
  const [qaAnswer, setQaAnswer] = useState<string | null>(null);
  const [qaError, setQaError] = useState<string | null>(null);

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const handleGenerateLetter = async () => {
    setLoading(true);
    setError(null);
    setCoverLetterData(null);
    setStatus(null);

    try {
      const res = await fetch(`${getApiBase()}/jobs/${id}/process`, {
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

  const handleAskQuestion = async () => {
    if (!question.trim()) return;
    setQaLoading(true);
    setQaError(null);
    setQaAnswer(null);

    try {
      const res = await fetch(`${getApiBase()}/jobs/${id}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      setQaAnswer(data.answer);
    } catch (err: any) {
      setQaError(err.message || 'Failed to get an answer.');
    } finally {
      setQaLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow flex flex-col md:flex-row gap-6 bg-white">
      {/* Left side: Job Details */}
      <div className="flex-1 flex flex-col">
        <h3 className="text-xl font-bold">{title}</h3>
        <p className="text-gray-600 font-medium">{company} {location && `- ${location}`}</p>
        <p className="mt-2 text-sm text-gray-700 line-clamp-3">{description}</p>
        
        {qaAnswer && (
          <div className="mt-4 p-3 bg-gray-50 border border-gray-200 rounded-md shadow-sm">
            <p className="text-xs font-semibold text-gray-700 mb-1">AI Answer:</p>
            <p className="text-xs text-gray-800 whitespace-pre-wrap">{qaAnswer}</p>
          </div>
        )}

        {coverLetterData && (
          <div className="mt-4 p-4 bg-indigo-50 border border-indigo-100 rounded-md shadow-sm">
            <div className="flex justify-between items-center mb-3">
              <span className="text-xs font-bold text-indigo-800 uppercase">AI Generated Match</span>
              <span className="text-xs bg-indigo-200 text-indigo-800 py-1 px-3 rounded-full font-semibold">
                Score: {coverLetterData.score} | ATS: {(coverLetterData.ats_match * 100).toFixed(0)}%
              </span>
            </div>
            <p className="text-xs text-gray-700 whitespace-pre-wrap max-h-40 overflow-y-auto custom-scrollbar">
              {coverLetterData.cover_letter}
            </p>
          </div>
        )}

        <div className="mt-auto pt-4 flex items-center gap-3">
          <span className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-600 uppercase tracking-wider font-semibold">{source}</span>
          <a href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-sm font-medium">
            View Original Job &rarr;
          </a>
        </div>
      </div>

      {/* Right side: Actions */}
      <div className="w-full md:w-72 flex flex-col gap-3 justify-start shrink-0 border-t md:border-t-0 md:border-l pt-4 md:pt-0 md:pl-6">
        
        {/* Cover Letter Button */}
        <div>
          <button
            onClick={handleGenerateLetter}
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2.5 px-4 rounded-md text-sm transition-colors shadow-sm disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'Generate Cover Letter'}
          </button>
          
          {status && (
            <div className="mt-2 text-xs p-2 bg-yellow-50 text-yellow-800 border border-yellow-200 rounded">
              {status}
            </div>
          )}
          {error && (
            <div className="mt-2 text-xs p-2 bg-red-50 text-red-800 border border-red-200 rounded">
              {error}
            </div>
          )}
        </div>

        {/* Q&A Button */}
        <div className="flex flex-col gap-2 mt-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask AI about this job..."
            className="w-full border rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-indigo-500 shadow-sm"
            onKeyDown={(e) => e.key === 'Enter' && handleAskQuestion()}
          />
          <button
            onClick={handleAskQuestion}
            disabled={qaLoading || !question.trim()}
            className="w-full bg-gray-800 hover:bg-gray-900 text-white py-2 rounded-md text-sm disabled:opacity-50 transition-colors shadow-sm font-semibold"
          >
            {qaLoading ? 'Thinking...' : 'Ask Question'}
          </button>
          
          {qaError && (
            <div className="mt-1 text-xs text-red-600 font-medium">
              Error: {qaError}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
