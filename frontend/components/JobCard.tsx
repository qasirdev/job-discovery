import React from 'react';

interface JobCardProps {
  id: string;
  title: string;
  company: string;
  location?: string;
  description: string;
  url: string;
  source: string;
}

export function JobCard({ title, company, location, description, url, source }: JobCardProps) {
  return (
    <div className="p-4 border rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <h3 className="text-xl font-bold">{title}</h3>
      <p className="text-gray-600">{company} {location && `- ${location}`}</p>
      <p className="mt-2 text-sm text-gray-800 line-clamp-3">{description}</p>
      <div className="mt-4 flex justify-between items-center">
        <span className="text-xs bg-gray-100 px-2 py-1 rounded text-gray-600 uppercase tracking-wider">{source}</span>
        <a href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline text-sm font-medium">
          View Job
        </a>
      </div>
    </div>
  );
}
