'use client';

import React, { useState } from 'react';
import { Card, CardContent, Typography, Button, Box, Chip, Divider } from '@mui/material';

interface LivingContract {
  id: string;
  agent: string;
  scope: string;
  expiresAt: string; // ISO String
  status: 'active' | 'revoked' | 'expired';
}

export default function ConsentSettingsPage() {
  // Mock data for the dashboard
  const [contracts, setContracts] = useState<LivingContract[]>([
    {
      id: 'lc_123',
      agent: 'Application Assistant Agent',
      scope: 'Submit applications to Workday and Greenhouse portals',
      expiresAt: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(), // +2 hours
      status: 'active',
    },
    {
      id: 'lc_456',
      agent: 'LinkedIn Scraper Agent',
      scope: 'Read profile data and saved jobs',
      expiresAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // -24 hours
      status: 'expired',
    }
  ]);

  const handleRevoke = (id: string) => {
    setContracts(prev => prev.map(c => 
      c.id === id ? { ...c, status: 'revoked' } : c
    ));
    // In a real app, make DELETE /api/v1/user/consent/{id} call here
  };

  const getStatusChip = (status: LivingContract['status']) => {
    switch (status) {
      case 'active':
        return <Chip label="Active" color="success" size="small" />;
      case 'revoked':
        return <Chip label="Revoked" color="error" size="small" />;
      case 'expired':
        return <Chip label="Expired" color="default" size="small" />;
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" sx={{ fontWeight: 'bold', color: 'gray.900', mb: 1 }}>
            Agentic Consent Management
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage active Living Contracts and data access for your AI agents.
          </Typography>
        </Box>

        <Card className="shadow-sm border border-gray-100">
          <CardContent className="p-0">
            {contracts.length === 0 ? (
              <Box className="p-8 text-center text-gray-500">
                No active or past consents found.
              </Box>
            ) : (
              <Box className="flex flex-col">
                {contracts.map((contract, index) => (
                  <React.Fragment key={contract.id}>
                    <Box className="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <Box>
                        <Box className="flex items-center gap-3 mb-1">
                          <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {contract.agent}
                          </Typography>
                          {getStatusChip(contract.status)}
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                          <strong>Scope:</strong> {contract.scope}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {contract.status === 'active' 
                            ? `Expires at: ${new Date(contract.expiresAt).toLocaleString()}`
                            : contract.status === 'revoked'
                              ? 'Contract was manually revoked.'
                              : `Expired on: ${new Date(contract.expiresAt).toLocaleString()}`
                          }
                        </Typography>
                      </Box>
                      <Box>
                        <Button 
                          variant="outlined" 
                          color="error" 
                          disabled={contract.status !== 'active'}
                          onClick={() => handleRevoke(contract.id)}
                        >
                          Revoke Access
                        </Button>
                      </Box>
                    </Box>
                    {index < contracts.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </Box>
            )}
          </CardContent>
        </Card>
      </div>
    </main>
  );
}
