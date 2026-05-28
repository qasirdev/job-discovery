'use client';

import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box,
  Alert
} from '@mui/material';
import { useConsentStore } from '../store/useConsentStore';

export default function ConsentPromptModal() {
  const { activePrompts, removePrompt, grantConsent } = useConsentStore();
  
  // We process one prompt at a time (queue behavior)
  const currentPrompt = activePrompts.length > 0 ? activePrompts[0] : null;
  const [duration, setDuration] = useState<number>(currentPrompt?.defaultDurationHours || 4);

  // Update local state when a new prompt appears
  React.useEffect(() => {
    if (currentPrompt) {
      setDuration(currentPrompt.defaultDurationHours);
    }
  }, [currentPrompt]);

  if (!currentPrompt) return null;

  const handleApprove = () => {
    // In a real implementation, this would call the backend to register the living contract
    console.log(`Approved consent for ${currentPrompt.id} with duration ${duration}h`);
    // Use JD-314 grantConsent to create a session-bound consent
    grantConsent(currentPrompt, duration);
  };

  const handleReject = () => {
    console.log(`Rejected consent for ${currentPrompt.id}`);
    removePrompt(currentPrompt.id);
  };

  return (
    <Dialog open={true} maxWidth="sm" fullWidth>
      <DialogTitle sx={{ fontWeight: 'bold', color: 'primary.main' }}>
        Agent Authorization Required
      </DialogTitle>
      <DialogContent dividers>
        <Alert severity="info" sx={{ mb: 3 }}>
          The <strong>{currentPrompt.agent}</strong> is requesting permission to perform an action on your behalf.
        </Alert>
        
        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">Requested Action</Typography>
          <Typography variant="body1" sx={{ fontWeight: 500 }}>{currentPrompt.action}</Typography>
        </Box>

        <Box sx={{ mb: 3 }}>
          <Typography variant="subtitle2" color="text.secondary">Data Scope</Typography>
          <Typography variant="body1">{currentPrompt.scope}</Typography>
        </Box>

        <FormControl fullWidth size="small">
          <InputLabel id="duration-label">Authorization Duration</InputLabel>
          <Select
            labelId="duration-label"
            value={duration}
            label="Authorization Duration"
            onChange={(e) => setDuration(Number(e.target.value))}
          >
            <MenuItem value={1}>1 Hour (Single Session)</MenuItem>
            <MenuItem value={4}>4 Hours (Half Day)</MenuItem>
            <MenuItem value={24}>24 Hours (Full Day)</MenuItem>
          </Select>
        </FormControl>
        
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 1 }}>
          This Living Contract will automatically expire after the selected duration. You can revoke it at any time from the Consent Dashboard.
        </Typography>

      </DialogContent>
      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={handleReject} color="inherit" variant="outlined">
          Reject
        </Button>
        <Button onClick={handleApprove} color="primary" variant="contained">
          Authorize Agent
        </Button>
      </DialogActions>
    </Dialog>
  );
}
