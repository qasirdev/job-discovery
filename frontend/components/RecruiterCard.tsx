'use client';

import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, TextField, Rating, Box } from '@mui/material';

export interface Recruiter {
  id: string;
  name: string;
  company: string;
  email?: string;
  interaction_score: number;
  notes?: string;
}

interface RecruiterCardProps {
  recruiter: Recruiter;
}

export default function RecruiterCard({ recruiter: initialRecruiter }: RecruiterCardProps) {
  const [recruiter, setRecruiter] = useState(initialRecruiter);
  const [notes, setNotes] = useState(initialRecruiter.notes || '');
  const [loggingInteraction, setLoggingInteraction] = useState(false);

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const handleLogInteraction = async () => {
    setLoggingInteraction(true);
    // Optimistic update
    setRecruiter(prev => ({ ...prev, interaction_score: prev.interaction_score + 1 }));

    try {
      const res = await fetch(`${getApiBase()}/recruiters/${recruiter.id}/interaction`, {
        method: 'POST',
      });
      if (!res.ok) throw new Error('Failed to log interaction');
    } catch (err) {
      console.error(err);
      // Revert
      setRecruiter(prev => ({ ...prev, interaction_score: prev.interaction_score - 1 }));
    } finally {
      setLoggingInteraction(false);
    }
  };

  const handleNotesBlur = async () => {
    if (notes === recruiter.notes) return;
    
    // Optimistic update locally not strictly needed if we just let the input hold its state,
    // but let's sync our local recruiter object too
    setRecruiter(prev => ({ ...prev, notes }));

    try {
      const res = await fetch(`${getApiBase()}/recruiters/${recruiter.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes }),
      });
      if (!res.ok) throw new Error('Failed to update notes');
    } catch (err) {
      console.error(err);
      // Revert if failed
      setNotes(recruiter.notes || '');
      setRecruiter(prev => ({ ...prev, notes: recruiter.notes }));
    }
  };

  return (
    <Card className="shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="flex flex-col gap-3">
        <Box>
          <Typography variant="h6" fontWeight="bold">{recruiter.name}</Typography>
          <Typography variant="body2" color="text.secondary">{recruiter.company}</Typography>
          {recruiter.email && (
            <Typography variant="body2" color="primary">{recruiter.email}</Typography>
          )}
        </Box>

        <Box className="flex items-center gap-2 mt-1">
          <Typography variant="body2" fontWeight="bold">Interaction Score:</Typography>
          <Rating 
            value={Math.min(recruiter.interaction_score, 5)} 
            max={5} 
            readOnly 
            size="small" 
          />
          <Typography variant="caption" color="text.secondary">({recruiter.interaction_score})</Typography>
        </Box>

        <Button
          variant="outlined"
          size="small"
          onClick={handleLogInteraction}
          disabled={loggingInteraction}
          sx={{ alignSelf: 'flex-start', mt: 1 }}
        >
          {loggingInteraction ? 'Logging...' : 'Log Interaction'}
        </Button>

        <TextField
          label="Notes"
          multiline
          rows={3}
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          onBlur={handleNotesBlur}
          fullWidth
          size="small"
          margin="normal"
          InputProps={{ style: { fontSize: '0.875rem' } }}
        />
      </CardContent>
    </Card>
  );
}
