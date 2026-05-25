import './globals.css';
import type { Metadata } from 'next';
import QueryProvider from '../components/QueryProvider';
import { ThemeProvider, createTheme, CssBaseline, Box, AppBar, Toolbar, Typography, Button } from '@mui/material';
import Link from 'next/link';
import OnboardingBanner from '../components/OnboardingBanner';

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
    <html lang="en">
      <head>
        {process.env.NEXT_PUBLIC_CLARITY_PROJECT_ID && (
          <script
            type="text/javascript"
            dangerouslySetInnerHTML={{
              __html: `
                (function(c,l,a,r,i,t,y){
                    c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
                })(window, document, "clarity", "script", "${process.env.NEXT_PUBLIC_CLARITY_PROJECT_ID}");
              `,
            }}
          />
        )}
      </head>
      <body>
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
          </Box>
        </QueryProvider>
      </body>
    </html>
  );
}
