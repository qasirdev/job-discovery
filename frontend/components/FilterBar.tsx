'use client';
import React from 'react';
import { useFilterStore } from '../lib/store';

interface FilterBarProps {
  onSearch: () => void;
}

export function FilterBar({ onSearch }: FilterBarProps) {
  const { keyword, setKeyword, source, setSource } = useFilterStore();

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      onSearch();
    }
  };

  return (
    <div className="flex flex-col sm:flex-row gap-4 p-5 bg-gray-50 border-b border-gray-200">
      <div className="flex-1 flex gap-2">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search job titles or descriptions..."
          className="px-4 py-2 border border-gray-300 rounded-md w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition text-gray-900"
        />
        <button
          onClick={onSearch}
          className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-md transition duration-150"
        >
          Search
        </button>
      </div>

      <div className="flex gap-2 items-center">
        <label className="text-sm font-medium text-gray-700">Source:</label>
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none bg-white text-gray-900 font-medium transition"
        >
          <option value="">All Sources</option>
          <option value="linkedin">LinkedIn</option>
          <option value="jobserve">JobServe</option>
        </select>
      </div>
    </div>
  );
}
