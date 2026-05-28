import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], display: 'swap' });

import QueryProvider from '../components/QueryProvider';
import { ThemeProvider, createTheme, CssBaseline, Box, AppBar, Toolbar, Typography, Button } from '@mui/material';
import Link from 'next/link';
import OnboardingBanner from '../components/OnboardingBanner';
import GDPRConsentBanner from '../components/GDPRConsentBanner';
import ThemeRegistry from '../components/ThemeRegistry';
import { ToastProvider } from '../components/ToastProvider';

export const metadata: Metadata = {
  title: 'Job Discovery Platform',
  description: 'AI-Powered Job Discovery',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.className}>
      <head>
        {/* Microsoft Clarity is now loaded conditionally via GDPRConsentBanner */}
      </head>
      <body className="animate-fade-in-up">
        <ThemeRegistry>
          <ToastProvider>
            <QueryProvider>
              <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <AppBar position="static" color="default" elevation={1}>
              <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
                  <Link href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                    Job Discovery
                  </Link>
                </Typography>
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Link href="/" passHref><Button color="inherit">Dashboard</Button></Link>
                  <Link href="/saved" passHref><Button color="inherit">Saved</Button></Link>
                  <Link href="/applications" passHref><Button color="inherit">Applications</Button></Link>
                  <Link href="/recruiters" passHref><Button color="inherit">Recruiters</Button></Link>
                  <Link href="/profile" passHref><Button color="inherit">Profile</Button></Link>
                  <Link href="/admin" passHref><Button color="inherit">Admin</Button></Link>
                </Box>
              </Toolbar>
            </AppBar>
            <Box sx={{ p: 2, pb: 0 }}>
              <OnboardingBanner />
            </Box>
            <Box component="main" sx={{ flexGrow: 1 }}>
              {children}
            </Box>
            <GDPRConsentBanner />
            </Box>
            </QueryProvider>
          </ToastProvider>
        </ThemeRegistry>
      </body>
    </html>
  );
}
