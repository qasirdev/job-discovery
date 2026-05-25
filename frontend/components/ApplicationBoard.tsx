'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, Typography, Box, Select, MenuItem, SelectChangeEvent } from '@mui/material';
import ApplicationStatusBadge, { ApplicationStatus } from './ApplicationStatusBadge';

export interface Application {
  id: string;
  job_id: string;
  job_title: string;
  company: string;
  status: ApplicationStatus;
  applied_at: string;
  notes?: string;
}

interface ApplicationBoardProps {
  applications: Application[];
}

const columns: ApplicationStatus[] = [
  'draft',
  'applied',
  'awaiting_response',
  'interviewing',
  'offered',
  'rejected',
  'withdrawn',
];

const columnTitles: Record<ApplicationStatus, string> = {
  draft: 'Draft',
  applied: 'Applied',
  awaiting_response: 'Awaiting Response',
  interviewing: 'Interviewing',
  offered: 'Offered',
  rejected: 'Rejected',
  withdrawn: 'Withdrawn',
};

export default function ApplicationBoard({ applications: initialApplications }: ApplicationBoardProps) {
  const router = useRouter();
  const [apps, setApps] = useState<Application[]>(initialApplications);
  const [updating, setUpdating] = useState<string | null>(null);

  const getApiBase = () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || '/api/v1';
    const isDev = typeof window !== 'undefined' && window.location.hostname === 'localhost';
    const base = isDev ? 'http://localhost:8000/api/v1' : apiBase;
    return base.endsWith('/') ? base.slice(0, -1) : base;
  };

  const handleStatusChange = async (appId: string, newStatus: ApplicationStatus) => {
    setUpdating(appId);
    
    // Optimistic update
    setApps(prev => prev.map(app => 
      app.id === appId ? { ...app, status: newStatus } : app
    ));

    try {
      const res = await fetch(`${getApiBase()}/applications/${appId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus }),
      });

      if (!res.ok) {
        throw new Error('Failed to update status');
      }
    } catch (err) {
      console.error(err);
      // Revert on error
      setApps(prev => prev.map(app => 
        app.id === appId ? initialApplications.find(a => a.id === appId) || app : app
      ));
    } finally {
      setUpdating(null);
    }
  };

  const onDragStart = (e: React.DragEvent, appId: string) => {
    e.dataTransfer.setData('appId', appId);
  };

  const onDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const onDrop = (e: React.DragEvent, status: ApplicationStatus) => {
    e.preventDefault();
    const appId = e.dataTransfer.getData('appId');
    if (appId) {
      handleStatusChange(appId, status);
    }
  };

  return (
    <div className="flex overflow-x-auto gap-4 p-4 h-full min-h-[70vh] items-start">
      {columns.map((colStatus) => {
        const colApps = apps.filter(app => app.status === colStatus);
        
        return (
          <div 
            key={colStatus} 
            className="flex-shrink-0 w-80 bg-gray-50 rounded-lg p-3 border border-gray-200"
            onDragOver={onDragOver}
            onDrop={(e) => onDrop(e, colStatus)}
          >
            <div className="flex justify-between items-center mb-4 px-2">
              <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }} className="text-gray-700">
                {columnTitles[colStatus]}
              </Typography>
              <span className="bg-gray-200 text-gray-600 text-xs font-bold px-2 py-1 rounded-full">
                {colApps.length}
              </span>
            </div>
            
            <div className="flex flex-col gap-3 min-h-[50px]">
              {colApps.map(app => (
                <Card 
                  key={app.id} 
                  className={`cursor-pointer transition-shadow hover:shadow-md ${updating === app.id ? 'opacity-50' : ''}`}
                  draggable
                  onDragStart={(e) => onDragStart(e, app.id)}
                  onClick={() => router.push(`/applications/${app.id}`)}
                >
                  <CardContent className="p-3 pb-3 relative">
                    <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }} className="mb-1 leading-tight">
                      {app.job_title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" className="mb-3">
                      {app.company}
                    </Typography>
                    
                    <div className="flex justify-between items-center mt-2">
                      <Typography variant="caption" color="text.secondary">
                        {new Date(app.applied_at).toLocaleDateString()}
                      </Typography>
                      
                      <div onClick={(e) => e.stopPropagation()}>
                        <Select
                          value={app.status}
                          size="small"
                          sx={{ fontSize: '0.75rem', height: '28px', '.MuiSelect-select': { py: 0.5 } }}
                          onChange={(e: SelectChangeEvent) => handleStatusChange(app.id, e.target.value as ApplicationStatus)}
                        >
                          {columns.map(status => (
                            <MenuItem key={status} value={status} sx={{ fontSize: '0.8rem' }}>
                              {columnTitles[status]}
                            </MenuItem>
                          ))}
                        </Select>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
              
              {colApps.length === 0 && (
                <div className="text-center py-6 text-gray-400 text-sm border-2 border-dashed border-gray-200 rounded-md">
                  Drop here
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
