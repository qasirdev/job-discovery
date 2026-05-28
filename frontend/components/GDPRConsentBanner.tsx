'use client';

import React, { useEffect, useState } from 'react';
import { Box, Button, Typography, Paper } from '@mui/material';

export default function GDPRConsentBanner() {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    // Check if consent has already been given or denied
    const consent = localStorage.getItem('gdpr_analytics_consent');
    if (!consent) {
      setShowBanner(true);
    } else if (consent === 'granted') {
      loadClarity();
    }
  }, []);

  const loadClarity = () => {
    if (typeof window !== 'undefined' && process.env.NEXT_PUBLIC_CLARITY_PROJECT_ID) {
      const projectId = process.env.NEXT_PUBLIC_CLARITY_PROJECT_ID;
      (function(c: any,l: any,a: any,r: any,i: any,t?: any,y?: any){
          c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
          t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
          y=l.getElementsByTagName(r)[0];if(y && y.parentNode) y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", projectId);
    }
  };

  const handleAccept = () => {
    localStorage.setItem('gdpr_analytics_consent', 'granted');
    setShowBanner(false);
    loadClarity();
  };

  const handleDecline = () => {
    localStorage.setItem('gdpr_analytics_consent', 'denied');
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <Paper 
      elevation={3} 
      sx={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        p: 2,
        display: 'flex',
        flexDirection: { xs: 'column', sm: 'row' },
        justifyContent: 'space-between',
        alignItems: 'center',
        bgcolor: 'background.paper',
        borderTop: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Box sx={{ mb: { xs: 2, sm: 0 }, pr: { sm: 2 } }}>
        <Typography variant="body2" color="text.primary">
          We use tracking cookies to understand how you use the product and help us improve it. 
          Please accept to allow us to load Microsoft Clarity. You have the right to erase your data from the Profile page.
        </Typography>
      </Box>
      <Box sx={{ display: 'flex', gap: 2, flexShrink: 0 }}>
        <Button variant="outlined" color="inherit" onClick={handleDecline}>
          Decline
        </Button>
        <Button variant="contained" color="primary" onClick={handleAccept}>
          Accept Analytics
        </Button>
      </Box>
    </Paper>
  );
}
