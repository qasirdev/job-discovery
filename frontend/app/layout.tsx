import './globals.css';
import type { Metadata } from 'next';
import QueryProvider from '../components/QueryProvider';

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
      <body>
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  );
}
