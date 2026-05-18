import React from 'react';

export function FilterBar() {
  return (
    <div className="flex gap-4 p-4 bg-gray-50 border-b">
      <input 
        type="text" 
        placeholder="Search jobs..." 
        className="px-4 py-2 border rounded-md w-full max-w-md"
      />
      <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
        Search
      </button>
    </div>
  );
}
