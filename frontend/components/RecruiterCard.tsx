'use client';

import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, TextField, Rating } from '@mui/material';
import { useMutation, useQueryClient } from '@tanstack/react-query';

export interface Recruiter {
  id: string;
  name: string;
  company: string;
  email?: string;
  quality_score: number;
  notes?: string;
}

export default function RecruiterCard({ recruiter }: { recruiter: Recruiter }) {
  const queryClient = useQueryClient();
  const [notes, setNotes] = useState(recruiter.notes || '');

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    return `${cleanBase}${endpoint}`;
  };

  const logInteraction = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl(`/recruiters/${recruiter.id}/interaction`), { method: 'POST' });
      if (!res.ok) throw new Error('Failed to log interaction');
      return res.json();
    },
    onMutate: async () => {
      await queryClient.cancelQueries({ queryKey: ['recruiters'] });
      const previousRecruiters = queryClient.getQueryData<Recruiter[]>(['recruiters']);
      
      if (previousRecruiters) {
        queryClient.setQueryData<Recruiter[]>(['recruiters'], (old) => {
          if (!old) return old;
          return old.map(r => r.id === recruiter.id ? { ...r, quality_score: Math.min(10, r.quality_score + 1) } : r);
        });
      }
      return { previousRecruiters };
    },
    onError: (err, newTodo, context) => {
      if (context?.previousRecruiters) {
        queryClient.setQueryData(['recruiters'], context.previousRecruiters);
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['recruiters'] });
    }
  });

  const updateNotes = useMutation({
    mutationFn: async (newNotes: string) => {
      const res = await fetch(getApiUrl(`/recruiters/${recruiter.id}`), {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes: newNotes })
      });
      if (!res.ok) throw new Error('Failed to update notes');
      return res.json();
    }
  });

  return (
    <Card className="hover:shadow-md transition-shadow h-full flex flex-col">
      <CardContent className="flex flex-col h-full gap-4">
        <div>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }} className="leading-tight mb-1">
            {recruiter.name}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {recruiter.company}
          </Typography>
          {recruiter.email && (
            <Typography variant="caption" className="text-indigo-600">
              {recruiter.email}
            </Typography>
          )}
        </div>

        <div className="flex items-center gap-2">
          <Typography variant="body2" sx={{ fontWeight: 'medium' }}>Score:</Typography>
          <Rating value={recruiter.quality_score / 2} max={5} precision={0.5} readOnly size="small" />
        </div>

        <div className="flex-grow">
          <TextField
            label="Notes"
            multiline
            rows={3}
            fullWidth
            size="small"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            onBlur={() => {
              if (notes !== recruiter.notes) {
                updateNotes.mutate(notes);
              }
            }}
            placeholder="Add interaction notes..."
            sx={{ '& .MuiInputBase-input': { fontSize: '0.875rem' } }}
          />
        </div>

        <Button 
          variant="contained" 
          color="primary"
          onClick={() => logInteraction.mutate()}
          disabled={logInteraction.isPending}
          sx={{ textTransform: 'none' }}
          fullWidth
        >
          {logInteraction.isPending ? 'Logging...' : 'Log Interaction'}
        </Button>
      </CardContent>
    </Card>
  );
}
