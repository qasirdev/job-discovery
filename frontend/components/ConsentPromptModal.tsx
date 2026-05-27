'use client';

import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

interface ConsentPromptModalProps {
  open: boolean;
  title: string;
  message: string;
  onApprove: () => void;
  onDecline: () => void;
}

export default function ConsentPromptModal({ open, title, message, onApprove, onDecline }: ConsentPromptModalProps) {
  return (
    <Dialog open={open} onClose={onDecline} maxWidth="sm" fullWidth>
      <DialogTitle className="font-bold text-gray-900 border-b border-gray-100">{title}</DialogTitle>
      <DialogContent className="pt-4 pb-6">
        <Typography className="text-gray-700 whitespace-pre-line mt-2">
          {message}
        </Typography>
        <div className="mt-4 p-3 bg-amber-50 border border-amber-100 rounded-lg">
          <Typography className="text-sm text-amber-800 flex items-start gap-2">
            <svg className="w-5 h-5 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            This action requires your explicit consent. You can revoke this permission at any time in the Settings dashboard.
          </Typography>
        </div>
      </DialogContent>
      <DialogActions className="p-4 border-t border-gray-100">
        <Button onClick={onDecline} color="inherit" className="text-gray-600 hover:bg-gray-50">
          Decline
        </Button>
        <Button onClick={onApprove} variant="contained" className="bg-indigo-600 hover:bg-indigo-700 shadow-none">
          Approve
        </Button>
      </DialogActions>
    </Dialog>
  );
}
