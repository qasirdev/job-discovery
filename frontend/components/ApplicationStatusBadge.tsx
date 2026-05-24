import React from 'react';
import { Chip } from '@mui/material';

export type ApplicationStatus = 
  | 'draft' 
  | 'applied' 
  | 'awaiting_response' 
  | 'interviewing' 
  | 'offered' 
  | 'rejected' 
  | 'withdrawn';

interface ApplicationStatusBadgeProps {
  status: ApplicationStatus;
}

const statusColors: Record<ApplicationStatus, "default" | "primary" | "secondary" | "error" | "info" | "success" | "warning"> = {
  draft: 'default',
  applied: 'info',
  awaiting_response: 'warning',
  interviewing: 'secondary',
  offered: 'success',
  rejected: 'error',
  withdrawn: 'default',
};

const statusLabels: Record<ApplicationStatus, string> = {
  draft: 'Draft',
  applied: 'Applied',
  awaiting_response: 'Awaiting Response',
  interviewing: 'Interviewing',
  offered: 'Offered',
  rejected: 'Rejected',
  withdrawn: 'Withdrawn',
};

export default function ApplicationStatusBadge({ status }: ApplicationStatusBadgeProps) {
  return (
    <Chip 
      label={statusLabels[status] || status} 
      color={statusColors[status] || 'default'} 
      size="small" 
      sx={{ fontWeight: 'bold' }} 
    />
  );
}
