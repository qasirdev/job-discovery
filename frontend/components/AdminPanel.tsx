'use client';

import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
  Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Alert 
} from '@mui/material';

export default function AdminPanel() {
  const queryClient = useQueryClient();

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const { data: featureFlags, isLoading: flagsLoading } = useQuery({
    queryKey: ['feature-flags'],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/feature-flags`);
      if (!res.ok) throw new Error('Failed to fetch feature flags');
      return res.json();
    }
  });

  const { data: dlq, isLoading: dlqLoading } = useQuery({
    queryKey: ['admin-dlq'],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/admin/dlq`);
      if (!res.ok) throw new Error('Failed to fetch DLQ');
      return res.json();
    },
    enabled: featureFlags?.feature_admin_panel === true
  });

  const { data: schedule, isLoading: scheduleLoading } = useQuery({
    queryKey: ['admin-schedule'],
    queryFn: async () => {
      const res = await fetch(`${getApiBase()}/admin/schedule`);
      if (!res.ok) throw new Error('Failed to fetch schedule');
      return res.json();
    },
    enabled: featureFlags?.feature_admin_panel === true
  });

  const retryMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(`${getApiBase()}/admin/dlq/${id}/retry`, { method: 'POST' });
      if (!res.ok) throw new Error('Retry failed');
      return res.json();
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-dlq'] })
  });

  const discardMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(`${getApiBase()}/admin/dlq/${id}/discard`, { method: 'POST' });
      if (!res.ok) throw new Error('Discard failed');
      return res.json();
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-dlq'] })
  });

  if (flagsLoading) return <Typography>Loading admin panel...</Typography>;

  if (!featureFlags?.feature_admin_panel) {
    return <Alert severity="error">Admin panel is disabled.</Alert>;
  }

  return (
    <Box className="flex flex-col gap-8">
      <Box>
        <Typography variant="h5" fontWeight="bold" className="mb-4">Dead Letter Queue (DLQ)</Typography>
        {dlqLoading ? (
          <Typography>Loading DLQ...</Typography>
        ) : dlq?.length === 0 ? (
          <Typography color="text.secondary">No failed jobs in queue.</Typography>
        ) : (
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead className="bg-gray-50">
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Agent</TableCell>
                  <TableCell>Error</TableCell>
                  <TableCell>Created At</TableCell>
                  <TableCell align="right">Retry Count</TableCell>
                  <TableCell align="center">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dlq?.map((row: any) => (
                  <TableRow key={row.id}>
                    <TableCell className="font-mono text-xs">{row.id}</TableCell>
                    <TableCell>{row.agent}</TableCell>
                    <TableCell className="text-red-600 max-w-xs truncate" title={row.error}>{row.error}</TableCell>
                    <TableCell>{new Date(row.created_at).toLocaleString()}</TableCell>
                    <TableCell align="right">{row.retry_count}</TableCell>
                    <TableCell align="center">
                      <div className="flex gap-2 justify-center">
                        <Button 
                          size="small" 
                          variant="outlined" 
                          color="primary"
                          disabled={retryMutation.isPending}
                          onClick={() => retryMutation.mutate(row.id)}
                        >
                          Retry
                        </Button>
                        <Button 
                          size="small" 
                          variant="outlined" 
                          color="error"
                          disabled={discardMutation.isPending}
                          onClick={() => discardMutation.mutate(row.id)}
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
      </Box>

      <Box>
        <Typography variant="h5" fontWeight="bold" className="mb-4">Agent Schedules</Typography>
        {scheduleLoading ? (
          <Typography>Loading schedules...</Typography>
        ) : (
          <TableContainer component={Paper} className="max-w-md">
            <Table size="small">
              <TableHead className="bg-gray-50">
                <TableRow>
                  <TableCell>Agent</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell align="center">Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {schedule?.map((item: any) => (
                  <TableRow key={item.agent}>
                    <TableCell>{item.agent}</TableCell>
                    <TableCell>
                      <span className={`px-2 py-1 rounded text-xs font-bold ${item.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {item.status.toUpperCase()}
                      </span>
                    </TableCell>
                    <TableCell align="center">
                      {item.status === 'active' ? (
                        <Button size="small" variant="contained" color="warning">Pause</Button>
                      ) : (
                        <Button size="small" variant="contained" color="success">Resume</Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Box>
    </Box>
  );
}
