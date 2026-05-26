'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Box, Chip, CircularProgress, Alert } from '@mui/material';

interface TokenBudgetAlert {
  agent_id: string;
  budget: number;
  actual: number;
  overage_pct: number;
}

interface AgentTrace {
  span_id: string;
  agent: string;
  duration_ms: number;
  status: string;
}

interface ObservabilityStatus {
  schema_conformance_rate: number | null;
  hallucination_rate: number | null;
  retrieval_precision: number | null;
  token_budget_alerts: TokenBudgetAlert[];
  recent_traces?: AgentTrace[];
}

export function ObservabilityPanel() {
  const [status, setStatus] = useState<ObservabilityStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
        const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
        const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
        const baseUrl = base.endsWith('/') ? base.slice(0, -1) : base;

        const res = await fetch(`${baseUrl}/observability/status`);
        if (!res.ok) throw new Error('Failed to fetch observability status');
        const data = await res.json();
        setStatus(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    // Poll every 30 seconds
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !status) {
    return <CircularProgress size={24} />;
  }

  if (error) {
    return <Alert severity="error">Error loading observability data: {error}</Alert>;
  }

  if (!status) return null;

  return (
    <Card className="shadow-sm bg-white mb-6">
      <CardContent className="flex flex-col gap-4 p-5">
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
          System Observability & AI Metrics
        </Typography>

        <Box className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
          {/* Schema Conformance */}
          <Box className="p-4 border rounded-md shadow-sm">
            <Typography variant="subtitle2" color="text.secondary">Schema Conformance Rate</Typography>
            <Typography variant="h4" color={status.schema_conformance_rate && status.schema_conformance_rate < 0.99 ? 'error' : 'primary'}>
              {status.schema_conformance_rate !== null ? `${(status.schema_conformance_rate * 100).toFixed(1)}%` : 'N/A'}
            </Typography>
          </Box>

          {/* Hallucination Rate */}
          <Box className="p-4 border rounded-md shadow-sm">
            <Typography variant="subtitle2" color="text.secondary">Hallucination Rate</Typography>
            <Typography variant="h4" color={status.hallucination_rate && status.hallucination_rate > 0.01 ? 'error' : 'primary'}>
              {status.hallucination_rate !== null ? `${(status.hallucination_rate * 100).toFixed(2)}%` : 'N/A'}
            </Typography>
          </Box>

          {/* Retrieval Precision */}
          <Box className="p-4 border rounded-md shadow-sm">
            <Typography variant="subtitle2" color="text.secondary">Retrieval Precision (RAG)</Typography>
            <Typography variant="h4" color={status.retrieval_precision && status.retrieval_precision < 0.80 ? 'error' : 'primary'}>
              {status.retrieval_precision !== null ? `${(status.retrieval_precision * 100).toFixed(1)}%` : 'N/A'}
            </Typography>
          </Box>
        </Box>

        {/* Token Usage Alerts */}
        <Box className="mt-4">
          <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }} className="mb-2">
            Token Budget Alerts
          </Typography>
          {status.token_budget_alerts && status.token_budget_alerts.length > 0 ? (
            <Box className="flex flex-col gap-2">
              {status.token_budget_alerts.map((alert) => (
                <Alert severity="warning" key={alert.agent_id}>
                  Agent <strong>{alert.agent_id}</strong> has exceeded its token budget by <strong>{alert.overage_pct}%</strong> (Used: {alert.actual} / Budget: {alert.budget})
                </Alert>
              ))}
            </Box>
          ) : (
            <Typography variant="body2" color="text.secondary">
              No token budget alerts active. All agents are within budget.
            </Typography>
          )}
        </Box>

        {/* Recent Traces */}
        <Box className="mt-4">
          <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }} className="mb-2">
            Recent Agent Traces
          </Typography>
          {status.recent_traces && status.recent_traces.length > 0 ? (
            <Box className="flex flex-col gap-2">
              {status.recent_traces.map((trace) => (
                <Box key={trace.span_id} className="p-3 border rounded-md shadow-sm flex justify-between items-center bg-gray-50">
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{trace.agent}</Typography>
                    <Typography variant="caption" color="text.secondary">ID: {trace.span_id}</Typography>
                  </Box>
                  <Box className="flex items-center gap-3">
                    <Typography variant="body2">{trace.duration_ms}ms</Typography>
                    <Chip 
                      label={trace.status} 
                      size="small" 
                      color={trace.status === 'success' ? 'success' : 'error'} 
                      variant="outlined" 
                    />
                  </Box>
                </Box>
              ))}
            </Box>
          ) : (
            <Typography variant="body2" color="text.secondary">
              No recent traces available.
            </Typography>
          )}
        </Box>
      </CardContent>
    </Card>
  );
}
