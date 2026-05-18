import React from 'react';
import { FilterBar } from '../components/FilterBar';
import { ScrapeButton } from '../components/ScrapeButton';
import { JobCard } from '../components/JobCard';

export default function DashboardPage() {
  // Mock data for MVP 1 static layout
  const mockJobs = [
    {
      id: "1",
      title: "Senior AI Engineer",
      company: "TechNova",
      location: "Remote",
      description: "Looking for an engineer to build RAG pipelines.",
      url: "#",
      source: "linkedin"
    },
    {
      id: "2",
      title: "Backend Developer (Python)",
      company: "DataCorp",
      location: "London, UK",
      description: "FastAPI and PostgreSQL experience required.",
      url: "#",
      source: "jobserve"
    }
  ];

  return (
    <main className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex justify-between items-center bg-white p-6 rounded-lg shadow-sm">
          <h1 className="text-3xl font-bold text-gray-900">Job Discovery Platform</h1>
          <ScrapeButton />
        </header>

        <section className="bg-white rounded-lg shadow-sm overflow-hidden">
          <FilterBar />
          <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockJobs.map(job => (
              <JobCard key={job.id} {...job} />
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
