'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { JobCard } from './JobCard';
import { Skeleton, Box, Typography, Button } from '@mui/material';
import Link from 'next/link';

import { Job } from '../types/job';

export default function SavedJobsList() {
  const { data: jobs, isLoading, error } = useQuery<Job[]>({
    queryKey: ['saved-jobs'],
    queryFn: async () => {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
      const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
      const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
      const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;

      const res = await fetch(`${cleanBase}/jobs/saved`);
      if (!res.ok) {
        throw new Error('Failed to fetch saved jobs');
      }
      return res.json();
    },
  });

  if (isLoading) {
    return (
      <div className="flex flex-col gap-4">
        {[1, 2, 3].map((i) => (
          <Box key={i} className="p-4 border rounded-lg shadow-sm bg-white flex flex-col md:flex-row gap-6">
            <div className="flex-1">
              <Skeleton variant="text" sx={{ fontSize: '1.5rem', width: '60%' }} />
              <Skeleton variant="text" sx={{ fontSize: '1rem', width: '40%' }} />
              <Skeleton variant="rectangular" height={60} sx={{ mt: 2 }} />
            </div>
            <div className="w-full md:w-72">
              <Skeleton variant="rectangular" height={40} />
            </div>
          </Box>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-800 rounded">
        Failed to load saved jobs: {(error as Error).message}
      </div>
    );
  }

  if (!jobs || jobs.length === 0) {
    return (
      <div className="text-center p-8 bg-gray-50 rounded-lg border border-gray-200">
        <Typography variant="h6" className="mb-2 text-gray-700">
          No saved jobs yet.
        </Typography>
        <Typography variant="body1" className="mb-4 text-gray-500">
          Browse the job feed and save roles you're interested in.
        </Typography>
        <Link href="/" passHref>
          <Button variant="contained" color="primary">
            Browse jobs
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-4">
      {jobs.map((job) => (
        <JobCard
          key={job.id}
          id={job.id}
          title={job.title}
          company={job.company}
          location={job.location}
          description={job.description}
          url={job.url}
          source={job.source}
        />
      ))}
    </div>
  );
}
