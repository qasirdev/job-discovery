import React from 'react';
import { Skeleton, Box, Typography } from '@mui/material';

const columns = ['Draft', 'Applied', 'Awaiting Response', 'Interviewing', 'Offered', 'Rejected', 'Withdrawn'];

export default function ApplicationBoardSkeleton() {
  return (
    <div className="flex overflow-x-auto gap-4 p-4 h-full min-h-[70vh] items-start">
      {columns.map((title) => (
        <div 
          key={title} 
          className="flex-shrink-0 w-80 bg-gray-50 rounded-lg p-3 border border-gray-200"
        >
          <div className="flex justify-between items-center mb-4 px-2">
            <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }} className="text-gray-700">
              {title}
            </Typography>
            <Skeleton variant="circular" width={24} height={24} />
          </div>
          
          <div className="flex flex-col gap-3 min-h-[50px]">
            {/* Generate 1-3 skeleton cards per column pseudo-randomly based on title length */}
            {Array.from({ length: (title.length % 3) + 1 }).map((_, idx) => (
              <Box key={idx} className="bg-white rounded p-3 shadow-sm border border-gray-100">
                <Skeleton variant="text" sx={{ fontSize: '1rem', width: '80%', mb: 0.5 }} />
                <Skeleton variant="text" sx={{ fontSize: '0.875rem', width: '60%', mb: 2 }} />
                
                <div className="flex justify-between items-center">
                  <Skeleton variant="text" width={60} />
                  <Skeleton variant="rectangular" width={100} height={28} sx={{ borderRadius: 1 }} />
                </div>
              </Box>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
