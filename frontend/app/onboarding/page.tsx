'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useQueryClient, useQuery } from '@tanstack/react-query';
import ProfileForm from '../../components/ProfileForm';
import CVUploadPanel from '../../components/CVUploadPanel';
import { Container, Typography, Box, Paper, CircularProgress, Alert } from '@mui/material';
import { POLLING_INTERVAL_MS } from '../../lib/constants';

export default function OnboardingPage() {
    const router = useRouter();
    const queryClient = useQueryClient();
    const [cvUploading, setCvUploading] = useState(false);

    const getApiBase = () => {
        const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
        const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
        const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
        return base.endsWith('/') ? base.slice(0, -1) : base;
    };

    // Check if profile exists
    const { data: profile, isLoading: profileLoading } = useQuery({
        queryKey: ['profile'],
        queryFn: async () => {
            const res = await fetch(`${getApiBase()}/profile`);
            if (res.status === 404) return null;
            if (!res.ok) throw new Error('Failed to fetch profile');
            return res.json();
        }
    });

    // Check CV status
    const { data: cvStatus } = useQuery({
        queryKey: ['cv-status'],
        queryFn: async () => {
            const res = await fetch(`${getApiBase()}/cv/status`);
            if (res.status === 404) return { embedding_status: 'none' };
            if (!res.ok) throw new Error('Failed to fetch cv status');
            return res.json();
        },
        refetchInterval: (query) => {
            const data = query.state.data as any;
            if (data && (data.embedding_status === 'pending' || data.embedding_status === 'processing')) {
                return POLLING_INTERVAL_MS;
            }
            return false;
        }
    });

    // Redirect when ready
    React.useEffect(() => {
        if (profile && cvStatus?.embedding_status === 'ready') {
            router.push('/');
        }
    }, [profile, cvStatus, router]);

    const handleProfileSubmit = async (data: any) => {
        const method = profile ? 'PATCH' : 'POST';
        const res = await fetch(`${getApiBase()}/profile`, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Failed to save profile');
        
        // Invalidate to transition to CV upload step
        await queryClient.invalidateQueries({ queryKey: ['profile'] });
    };

    const handleCVUpload = async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const res = await fetch(`${getApiBase()}/cv`, {
            method: 'POST',
            body: formData
        });
        
        if (!res.ok) throw new Error('Failed to upload CV');
        await queryClient.invalidateQueries({ queryKey: ['cv-status'] });
    };

    // JD-311: Onboarding Timeout Fallback
    const [isTimeout, setIsTimeout] = useState(false);
    React.useEffect(() => {
        let timer: NodeJS.Timeout;
        if (profileLoading) {
            timer = setTimeout(() => {
                setIsTimeout(true);
            }, 30000); // 30 seconds timeout
        }
        return () => clearTimeout(timer);
    }, [profileLoading]);

    if (profileLoading && !isTimeout) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', flexDirection: 'column' }}>
                <CircularProgress />
                <Typography sx={{ mt: 2 }} color="text.secondary">Loading your profile...</Typography>
            </Box>
        );
    }

    return (
        <Container maxWidth="md" sx={{ py: 8 }}>
            <Paper elevation={0} sx={{ p: 4, border: '1px solid #e5e7eb', borderRadius: 2 }}>
                <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
                    Welcome to Job Discovery
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                    Let's get your profile set up so we can find the best matches for you.
                </Typography>

                <Box sx={{ mt: 4 }}>
                    {isTimeout && (
                        <Alert severity="warning" sx={{ mb: 3 }}>
                            The server is taking too long to respond. You can proceed with manual setup.
                        </Alert>
                    )}
                    {!profile ? (
                        <Box>
                            <Typography variant="h6" gutterBottom color="primary">Step 1: Complete Your Profile</Typography>
                            <ProfileForm onSubmit={handleProfileSubmit} />
                        </Box>
                    ) : (
                        <Box>
                            <Typography variant="h6" gutterBottom color="primary">Step 2: Upload Your CV</Typography>
                            <Typography color="text.secondary" sx={{ mb: 2 }}>
                                Your profile is saved. Now, upload your CV to enable AI features.
                            </Typography>
                            <CVUploadPanel onUpload={handleCVUpload} />
                        </Box>
                    )}
                </Box>
            </Paper>
        </Container>
    );
}
