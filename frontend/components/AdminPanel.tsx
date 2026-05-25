'use client';

import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper,
  Button, Typography, CircularProgress, Card, CardContent, Divider
} from '@mui/material';

export default function AdminPanel() {
  const queryClient = useQueryClient();

  const getApiUrl = (endpoint: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
    return `${cleanBase}${endpoint}`;
  };

  const { data: dlq, isLoading: dlqLoading } = useQuery({
    queryKey: ['admin-dlq'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/admin/dlq'));
      if (!res.ok) throw new Error('Failed to load DLQ');
      return res.json();
    }
  });

  const { data: schedule, isLoading: scheduleLoading } = useQuery({
    queryKey: ['admin-schedule'],
    queryFn: async () => {
      const res = await fetch(getApiUrl('/admin/schedule'));
      if (!res.ok) throw new Error('Failed to load schedule');
      return res.json();
    }
  });

  const retryMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(getApiUrl(`/admin/dlq/${id}/retry`), { method: 'POST' });
      if (!res.ok) throw new Error('Failed to retry task');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-dlq'] });
    }
  });

  const discardMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(getApiUrl(`/admin/dlq/${id}/discard`), { method: 'POST' });
      if (!res.ok) throw new Error('Failed to discard task');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-dlq'] });
    }
  });

  const pauseMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl('/admin/schedule/pause'), { method: 'POST' });
      if (!res.ok) throw new Error('Failed to pause schedule');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-schedule'] });
    }
  });

  const resumeMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(getApiUrl('/admin/schedule/resume'), { method: 'POST' });
      if (!res.ok) throw new Error('Failed to resume schedule');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-schedule'] });
    }
  });

  if (dlqLoading || scheduleLoading) {
    return (
      <div className="flex justify-center p-12">
        <CircularProgress />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Schedule Controls */}
      <Card className="shadow-sm border border-gray-200">
        <CardContent className="p-6">
          <div className="flex justify-between items-center">
            <div>
              <Typography variant="h6" className="font-bold text-gray-900 mb-1">
                Scraper Schedules
              </Typography>
              <Typography variant="body2" className="text-gray-500">
                Current status: <span className="font-semibold text-gray-700">{schedule?.status || 'Unknown'}</span>
              </Typography>
            </div>
            <div className="flex gap-3">
              <Button 
                variant="outlined" 
                color="warning" 
                onClick={() => pauseMutation.mutate()}
                disabled={pauseMutation.isPending || schedule?.status === 'paused'}
              >
                Pause All
              </Button>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={() => resumeMutation.mutate()}
                disabled={resumeMutation.isPending || schedule?.status === 'active'}
              >
                Resume All
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* DLQ Table */}
      <Card className="shadow-sm border border-gray-200">
        <CardContent className="p-0">
          <div className="p-6 pb-4">
            <Typography variant="h6" className="font-bold text-gray-900 mb-1">
              Dead Letter Queue (DLQ)
            </Typography>
            <Typography variant="body2" className="text-gray-500">
              Failed background tasks requiring manual intervention.
            </Typography>
          </div>
          <Divider />
          
          {!dlq || dlq.length === 0 ? (
            <div className="p-12 text-center">
              <Typography variant="body1" className="text-gray-500">
                No failed jobs in queue
              </Typography>
            </div>
          ) : (
            <TableContainer component={Paper} elevation={0}>
              <Table>
                <TableHead className="bg-gray-50">
                  <TableRow>
                    <TableCell className="font-semibold text-gray-700">ID</TableCell>
                    <TableCell className="font-semibold text-gray-700">Agent</TableCell>
                    <TableCell className="font-semibold text-gray-700">Error</TableCell>
                    <TableCell className="font-semibold text-gray-700">Created At</TableCell>
                    <TableCell className="font-semibold text-gray-700">Retries</TableCell>
                    <TableCell className="font-semibold text-gray-700" align="right">Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {dlq.map((row: any) => (
                    <TableRow key={row.id}>
                      <TableCell className="font-mono text-xs">{row.id.split('-')[0]}</TableCell>
                      <TableCell>{row.agent}</TableCell>
                      <TableCell className="text-red-600 text-sm max-w-xs truncate" title={row.error}>
                        {row.error}
                      </TableCell>
                      <TableCell className="text-sm">
                        {new Date(row.created_at).toLocaleString()}
                      </TableCell>
                      <TableCell>{row.retry_count}</TableCell>
                      <TableCell align="right">
                        <div className="flex justify-end gap-2">
                          <Button 
                            size="small" 
                            variant="outlined" 
                            onClick={() => retryMutation.mutate(row.id)}
                            disabled={retryMutation.isPending}
                          >
                            Retry
                          </Button>
                          <Button 
                            size="small" 
                            variant="outlined" 
                            color="error"
                            onClick={() => discardMutation.mutate(row.id)}
                            disabled={discardMutation.isPending}
                          >
                            Discard
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
