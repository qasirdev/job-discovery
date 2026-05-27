'use client';

import React from 'react';

export default function ConsentSettingsPage() {
  return (
    <main className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <h1 className="text-3xl font-extrabold text-gray-900 mb-2 leading-tight">Agentic Consent Management</h1>
        <p className="text-gray-500 mb-8">Manage active living contracts and data access for your AI agents.</p>
        
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-8">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-xl">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Coming in MVP 3</h2>
              <p className="text-gray-600 mb-4">
                The Agentic Consent Model provides policy-driven governance over autonomous agents,
                allowing you to issue time-bound and transaction-scoped permissions.
              </p>
              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 text-sm text-gray-500 italic">
                Active living contracts will appear here once the Security and Orchestrator agents are fully deployed.
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
