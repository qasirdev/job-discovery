'use client';
import React, { useEffect, useState } from 'react';
import { useFilterStore, FilterState } from '../lib/store';
import { Button, Checkbox, FormControlLabel, TextField } from '@mui/material';

export function FilterBar() {
  const { keyword, setKeyword, sources, setSources, clearFilters } = useFilterStore();
  
  // Local state for debouncing
  const [localKeyword, setLocalKeyword] = useState(keyword);

  // Debounce keyword
  useEffect(() => {
    const handler = setTimeout(() => {
      if (localKeyword !== keyword) {
        setKeyword(localKeyword);
      }
    }, 300);
    return () => clearTimeout(handler);
  }, [localKeyword, keyword, setKeyword]);

  const handleSourceChange = (source: string, checked: boolean) => {
    if (checked) {
      setSources([...sources, source]);
    } else {
      setSources(sources.filter((s) => s !== source));
    }
  };

  const handleClear = () => {
    setLocalKeyword('');
    clearFilters();
  };

  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 p-5 bg-white border-b border-gray-200">
      <div className="flex-1 w-full">
        <TextField
          value={localKeyword}
          onChange={(e) => setLocalKeyword(e.target.value)}
          placeholder="Search job titles or descriptions..."
          size="small"
          fullWidth
          variant="outlined"
        />
      </div>

      <div className="flex gap-4 items-center">
        <div className="flex items-center gap-2">
          <FormControlLabel
            control={
              <Checkbox 
                checked={sources.includes('linkedin')} 
                onChange={(e) => handleSourceChange('linkedin', e.target.checked)} 
                size="small"
              />
            }
            label={<span className="text-sm font-medium text-gray-700">LinkedIn</span>}
          />
          <FormControlLabel
            control={
              <Checkbox 
                checked={sources.includes('jobserve')} 
                onChange={(e) => handleSourceChange('jobserve', e.target.checked)} 
                size="small"
              />
            }
            label={<span className="text-sm font-medium text-gray-700">JobServe</span>}
          />
        </div>

        <Button 
          variant="outlined" 
          color="secondary" 
          onClick={handleClear}
          size="small"
        >
          Clear All
        </Button>
      </div>

      {sources.length === 0 && (
        <div className="w-full text-xs text-red-600 font-medium text-center sm:text-left mt-2 sm:hidden">
          No sources selected
        </div>
      )}
    </div>
  );
}
