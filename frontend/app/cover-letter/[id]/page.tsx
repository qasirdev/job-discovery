'use client';

import React from 'react';
import { useParams, useRouter } from 'next/navigation';
import CoverLetterViewer from '../../../components/CoverLetterViewer';

export default function CoverLetterPage() {
  const params = useParams();
  const id = params.id as string;
  const router = useRouter();

  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <button onClick={() => router.back()} className="text-sm text-gray-500 hover:text-gray-900 transition flex items-center gap-2">
          &larr; Back to Job Detail
        </button>
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-6 pb-4 border-b border-gray-100">Cover Letter</h1>
          <CoverLetterViewer jobId={id} />
        </div>
      </div>
    </main>
  );
}
