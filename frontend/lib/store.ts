import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface FilterState {
  keyword: string;
  sources: string[];
  setKeyword: (keyword: string) => void;
  setSources: (sources: string[]) => void;
  clearFilters: () => void;
}

export const useFilterStore = create<FilterState>()(
  persist(
    (set) => ({
      keyword: '',
      sources: ['linkedin', 'jobserve'],
      setKeyword: (keyword: string) => set({ keyword }),
      setSources: (sources: string[]) => set({ sources }),
      clearFilters: () => set({ keyword: '', sources: ['linkedin', 'jobserve'] }),
    }),
    {
      name: 'job-discovery-filters',
    }
  )
);
