'use client';
import React, { useState, useEffect, useCallback } from 'react';
import { FilterBar } from '../components/FilterBar';
import { ScrapeButton } from '../components/ScrapeButton';
import { JobCard } from '../components/JobCard';

interface Job {
  id: string;
  title: string;
  company: string;
  location: string | null;
  description: string;
  url: string;
  source: string;
}

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filter states
  const [keywordInput, setKeywordInput] = useState('');
  const [activeKeyword, setActiveKeyword] = useState('');
  const [sourceFilter, setSourceFilter] = useState('');

  // Fetch jobs dynamically from backend
  const fetchJobs = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let url = '/api/v1/jobs/?limit=50';
      if (sourceFilter) {
        url += `&source=${sourceFilter}`;
      }
      if (activeKeyword) {
        url += `&keyword=${encodeURIComponent(activeKeyword)}`;
      }

      const res = await fetch(url);
      if (!res.ok) {
        throw new Error(`Failed to load jobs (status ${res.status})`);
      }
      const payload = await res.json();
      setJobs(payload.data || []);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Error fetching jobs from server.');
    } finally {
      setLoading(false);
    }
  }, [activeKeyword, sourceFilter]);

  // Initial fetch and fetch on filter state adjustments
  useEffect(() => {
    fetchJobs();
  }, [fetchJobs]);

  const handleSearchSubmit = () => {
    setActiveKeyword(keywordInput);
  };

  const handleSourceChange = (newSource: string) => {
    setSourceFilter(newSource);
  };

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-white p-6 rounded-lg shadow-sm gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Job Discovery Dashboard</h1>
            <p className="text-sm text-gray-500 mt-1">
              AI-powered automated job search and profile ranking platform.
            </p>
          </div>
          <ScrapeButton onScrapeComplete={fetchJobs} />
        </header>

        <section className="bg-white rounded-lg shadow-sm overflow-hidden">
          <FilterBar
            keyword={keywordInput}
            onKeywordChange={setKeywordInput}
            source={sourceFilter}
            onSourceChange={handleSourceChange}
            onSearch={handleSearchSubmit}
          />

          {loading ? (
            <div className="p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600 mb-2"></div>
              <p className="text-gray-600 font-medium">Fetching job matches from database...</p>
            </div>
          ) : error ? (
            <div className="p-8 text-center bg-red-50 text-red-700 border-t border-red-100">
              <p className="font-semibold">Error Loading Dashboard Data</p>
              <p className="text-sm mt-1">{error}</p>
              <button
                onClick={fetchJobs}
                className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-xs font-semibold rounded transition"
              >
                Retry Request
              </button>
            </div>
          ) : jobs.length === 0 ? (
            <div className="p-12 text-center">
              <svg
                className="mx-auto h-12 w-12 text-gray-400 mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <p className="text-gray-900 font-semibold text-lg">No Job Matches Found</p>
              <p className="text-gray-500 text-sm mt-1 max-w-md mx-auto">
                No jobs are stored in the database. Click the **"Trigger Full Scrape"** button above to search LinkedIn and JobServe dynamically!
              </p>
            </div>
          ) : (
            <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {jobs.map((job) => (
                <JobCard key={job.id} {...job} />
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
