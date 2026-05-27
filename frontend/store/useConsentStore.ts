import { create } from 'zustand';

export interface ConsentRequest {
  id: string;
  agent: string;
  action: string;
  scope: string;
  defaultDurationHours: number;
}

interface ConsentState {
  activePrompts: ConsentRequest[];
  addPrompt: (request: ConsentRequest) => void;
  removePrompt: (id: string) => void;
}

export const useConsentStore = create<ConsentState>((set) => ({
  activePrompts: [],
  addPrompt: (request) => set((state) => ({ activePrompts: [...state.activePrompts, request] })),
  removePrompt: (id) => set((state) => ({
    activePrompts: state.activePrompts.filter((prompt) => prompt.id !== id),
  })),
}));
