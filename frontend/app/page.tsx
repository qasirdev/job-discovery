'use client';
import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useFilterStore } from '../lib/store';
import { FilterBar } from '../components/FilterBar';
import { ScrapeButton } from '../components/ScrapeButton';
import { JobCard } from '../components/JobCard';
import { ObservabilityPanel } from '../components/ObservabilityPanel';

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
  const { keyword, sources } = useFilterStore();
  const [activeKeyword, setActiveKeyword] = useState('');
  
  // Pagination and Limit State
  const [limit, setLimit] = useState<number>(20);
  const [cursorHistory, setCursorHistory] = useState<string[]>([]); // To go back
  const [currentCursor, setCurrentCursor] = useState<string | null>(null);

  // Sync active search trigger with stored value
  useEffect(() => {
    setActiveKeyword(keyword);
    // Reset pagination on new search
    setCursorHistory([]);
    setCurrentCursor(null);
  }, [keyword, sources]);

  const getApiUrl = (endpoint: string): string => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${cleanBase}${cleanEndpoint}`;
  };

  // Fetch jobs dynamically using TanStack Query
  const { data: jobsResponse, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ['jobs', sources, activeKeyword, limit, currentCursor],
    queryFn: async () => {
      let queryParams = `?limit=${limit}`;
      if (sources && sources.length > 0) {
        queryParams += `&source=${sources.join(',')}`;
      }
      if (activeKeyword) {
        queryParams += `&keyword=${encodeURIComponent(activeKeyword)}`;
      }
      if (currentCursor) {
        queryParams += `&cursor=${encodeURIComponent(currentCursor)}`;
      }

      const url = getApiUrl(`/jobs/${queryParams}`);
      const res = await fetch(url);

      if (!res.ok) {
        throw new Error(`Failed to load jobs (status ${res.status})`);
      }
      return res.json();
    },
  });

  const jobs: Job[] = jobsResponse?.jobs || [];
  const nextCursor = jobsResponse?.next_cursor || null;



  const handleNextPage = () => {
    if (nextCursor) {
      setCursorHistory([...cursorHistory, currentCursor || '']);
      setCurrentCursor(nextCursor);
    }
  };

  const handlePrevPage = () => {
    if (cursorHistory.length > 0) {
      const newHistory = [...cursorHistory];
      const prev = newHistory.pop() || null;
      setCursorHistory(newHistory);
      setCurrentCursor(prev === '' ? null : prev);
    }
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
          <ScrapeButton onScrapeComplete={() => {
            setCursorHistory([]);
            setCurrentCursor(null);
            refetch();
          }} />
        </header>

        <ObservabilityPanel />

        <section className="bg-white rounded-lg shadow-sm overflow-hidden flex flex-col">
          <FilterBar />

          {/* Pagination & Limit Controls */}
          <div className="border-b px-6 py-3 flex justify-between items-center bg-gray-50">
            <div className="flex items-center gap-2">
              <label htmlFor="limit-select" className="text-sm font-medium text-gray-700">Show:</label>
              <select
                id="limit-select"
                value={limit}
                onChange={(e) => {
                  setLimit(Number(e.target.value));
                  setCursorHistory([]);
                  setCurrentCursor(null);
                }}
                className="text-sm border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
            
            <div className="flex items-center gap-4">
              <button
                onClick={handlePrevPage}
                disabled={cursorHistory.length === 0 || isLoading || isFetching}
                className="text-sm px-3 py-1 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 transition"
              >
                &larr; Previous
              </button>
              <button
                onClick={handleNextPage}
                disabled={!nextCursor || isLoading || isFetching}
                className="text-sm px-3 py-1 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 transition"
              >
                Next &rarr;
              </button>
            </div>
          </div>

          {isLoading ? (
            <div className="p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600 mb-2"></div>
              <p className="text-gray-600 font-medium">Fetching job matches from database...</p>
            </div>
          ) : error ? (
            <div className="p-8 text-center bg-red-50 text-red-700 border-t border-red-100">
              <p className="font-semibold">Error Loading Dashboard Data</p>
              <p className="text-sm mt-1">{(error as any).message || 'Error fetching jobs from server.'}</p>
              <button
                onClick={() => refetch()}
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
            <div className="p-6 flex flex-col gap-6 relative">
              {isFetching && (
                <div className="absolute inset-0 bg-white/50 z-10 flex items-center justify-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
                </div>
              )}
              {jobs.map((job) => (
                <JobCard key={job.id} {...job} />
              ))}
            </div>
          )}
          
          {/* Bottom Pagination */}
          {!isLoading && !error && jobs.length > 0 && (
            <div className="border-t px-6 py-4 flex justify-end items-center bg-gray-50">
               <div className="flex items-center gap-4">
                <button
                  onClick={handlePrevPage}
                  disabled={cursorHistory.length === 0 || isLoading || isFetching}
                  className="text-sm px-3 py-1 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 transition"
                >
                  &larr; Previous
                </button>
                <button
                  onClick={handleNextPage}
                  disabled={!nextCursor || isLoading || isFetching}
                  className="text-sm px-3 py-1 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 transition"
                >
                  Next &rarr;
                </button>
              </div>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
