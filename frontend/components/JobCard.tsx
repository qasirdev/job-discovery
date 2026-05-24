'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, Typography, IconButton, Chip, Box } from '@mui/material';
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import BookmarkIcon from '@mui/icons-material/Bookmark';

export interface Job {
  id: string;
  title: string;
  company: string;
  location?: string | null;
  description: string;
  url: string;
  source: string;
  saved: boolean;
  salary_min?: number;
  salary_max?: number;
  scraped_at?: string;
  relevance_score?: number | null;
}

interface JobCardProps {
  id: string;
  title: string;
  company: string;
  location?: string | null;
  description: string;
  url: string;
  source: string;
  saved?: boolean;
  salary_min?: number;
  salary_max?: number;
  scraped_at?: string;
  relevance_score?: number | null;
}

export function JobCard({ 
  id, 
  title, 
  company, 
  location, 
  description, 
  source, 
  saved = false,
  salary_min,
  salary_max,
  scraped_at,
  relevance_score
}: JobCardProps) {
  const router = useRouter();
  
  // React 19's useOptimistic could be used here, but for simplicity we'll manage with useState
  // as useOptimistic is a hook that takes state and an update function.
  const [isSaved, setIsSaved] = useState(saved);

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const handleSaveToggle = async (e: React.MouseEvent) => {
    e.stopPropagation(); // prevent card click
    
    // optimistic update
    const newSavedState = !isSaved;
    setIsSaved(newSavedState);

    try {
      const method = newSavedState ? 'POST' : 'DELETE';
      const res = await fetch(`${getApiBase()}/jobs/${id}/save`, {
        method,
      });

      if (!res.ok) {
        throw new Error('Failed to toggle save state');
      }
    } catch (err) {
      console.error(err);
      // Revert optimistic update on failure
      setIsSaved(!newSavedState);
    }
  };

  const formatSalary = () => {
    if (salary_min && salary_max) return `£${salary_min} - £${salary_max}`;
    if (salary_min) return `From £${salary_min}`;
    if (salary_max) return `Up to £${salary_max}`;
    return null;
  };

  return (
    <Card 
      onClick={() => router.push(`/jobs/${id}`)}
      className="shadow-sm hover:shadow-md transition-shadow cursor-pointer bg-white"
    >
      <CardContent className="flex flex-col gap-2 p-5 relative">
        <Box className="flex justify-between items-start gap-4 pr-8">
          <Typography 
            variant="h6" 
            component="h3" 
            fontWeight="bold" 
            className="leading-tight hover:text-indigo-600 transition-colors"
          >
            {title}
          </Typography>
        </Box>

        <IconButton 
          onClick={handleSaveToggle}
          size="small"
          className="absolute top-4 right-4"
          color="primary"
        >
          {isSaved ? <BookmarkIcon /> : <BookmarkBorderIcon />}
        </IconButton>

        <Typography variant="body2" fontWeight="medium" color="text.primary">
          {company || 'Unknown company'} {location && `• ${location}`}
        </Typography>

        {formatSalary() && (
          <Typography variant="body2" color="text.secondary" fontWeight="bold">
            {formatSalary()}
          </Typography>
        )}

        <Typography 
          variant="body2" 
          color="text.secondary" 
          className="line-clamp-2 mt-1"
        >
          {description}
        </Typography>

        <Box className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100">
          <Chip 
            label={source} 
            size="small" 
            sx={{ 
              bgcolor: source.toLowerCase() === 'linkedin' ? '#0077b5' : source.toLowerCase() === 'jobserve' ? '#2e7d32' : 'grey.300',
              color: 'white',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              fontSize: '0.65rem'
            }} 
          />
          
          {relevance_score !== null && relevance_score !== undefined && (
            <Chip 
              label={`Score: ${relevance_score}`} 
              size="small"
              variant="outlined"
              color={relevance_score >= 80 ? 'success' : relevance_score >= 50 ? 'warning' : 'default'}
            />
          )}

          {scraped_at && (
            <Typography variant="caption" color="text.secondary" className="ml-auto">
              {new Date(scraped_at).toLocaleDateString()}
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}
