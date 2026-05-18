import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface FilterState {
  keyword: string;
  source: string;
  setKeyword: (keyword: string) => void;
  setSource: (source: string) => void;
  clearFilters: () => void;
}

export const useFilterStore = create<FilterState>()(
  persist(
    (set) => ({
      keyword: '',
      source: '',
      setKeyword: (keyword: string) => set({ keyword }),
      setSource: (source: string) => set({ source }),
      clearFilters: () => set({ keyword: '', source: '' }),
    }),
    {
      name: 'job-discovery-filters',
    }
  )
);
