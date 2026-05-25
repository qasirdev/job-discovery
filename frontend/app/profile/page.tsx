'use client';

import React from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import ProfileForm from '../../components/ProfileForm';
import CVUploadPanel from '../../components/CVUploadPanel';
import { Container, Typography, Box, Paper, CircularProgress, Alert, Snackbar } from '@mui/material';

export default function ProfilePage() {
    const queryClient = useQueryClient();
    const [snackbar, setSnackbar] = React.useState<{open: boolean, message: string, severity: 'success' | 'error'}>({ open: false, message: '', severity: 'success' });

    const getApiBase = () => {
        const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
        const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
        const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
        return base.endsWith('/') ? base.slice(0, -1) : base;
    };

    const { data: profile, isLoading } = useQuery({
        queryKey: ['profile'],
        queryFn: async () => {
            const res = await fetch(`${getApiBase()}/profile`);
            if (res.status === 404) return null;
            if (!res.ok) throw new Error('Failed to fetch profile');
            return res.json();
        }
    });

    const handleCreateProfile = async (data: any) => {
        const res = await fetch(`${getApiBase()}/profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Failed to create profile');
        
        await queryClient.invalidateQueries({ queryKey: ['profile'] });
        setSnackbar({ open: true, message: 'Profile created successfully!', severity: 'success' });
    };

    const handleUpdateProfile = async (data: any) => {
        const res = await fetch(`${getApiBase()}/profile`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('Failed to update profile');
        
        await queryClient.invalidateQueries({ queryKey: ['profile'] });
        setSnackbar({ open: true, message: 'Profile updated successfully!', severity: 'success' });
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
        await queryClient.invalidateQueries({ queryKey: ['profile'] });
        setSnackbar({ open: true, message: 'CV uploaded successfully!', severity: 'success' });
    };

    if (isLoading) {
        return (
            <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Container maxWidth="md" sx={{ py: 8 }}>
            <Paper elevation={0} sx={{ p: 4, border: '1px solid #e5e7eb', borderRadius: 2 }}>
                <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
                    Edit Profile
                </Typography>
                <Typography color="text.secondary" sx={{ mb: 4 }}>
                    Manage your target roles and update your CV.
                </Typography>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                    <Box>
                        <ProfileForm onSubmit={profile ? handleUpdateProfile : handleCreateProfile} initialData={profile || undefined} />
                    </Box>
                    <Box>
                        <CVUploadPanel onUpload={handleCVUpload} currentFilename={profile?.cv_filename} />
                    </Box>
                </Box>
            </Paper>

            <Snackbar 
                open={snackbar.open} 
                autoHideDuration={4000} 
                onClose={() => setSnackbar(prev => ({...prev, open: false}))}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
            >
                <Alert severity={snackbar.severity} sx={{ width: '100%' }}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Container>
    );
}
