import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface ConsentRequest {
  id: string;
  agent: string;
  action: string;
  scope: string;
  defaultDurationHours: number;
}

export interface GrantedConsent {
  agent: string;
  action: string;
  scope: string;
  expiresAt: number; // Unix timestamp in ms
}

interface ConsentState {
  activePrompts: ConsentRequest[];
  grantedConsents: GrantedConsent[];
  addPrompt: (request: ConsentRequest) => void;
  removePrompt: (id: string) => void;
  grantConsent: (request: ConsentRequest, durationHours: number) => void;
  clearExpiredConsents: () => void;
}

export const useConsentStore = create<ConsentState>()(
  persist(
    (set, get) => ({
      activePrompts: [],
      grantedConsents: [],
      addPrompt: (request) => {
        get().clearExpiredConsents();
        // JD-314: Consent Fatigue Prevention. Check if we already have a valid session consent
        const existing = get().grantedConsents.find(
          c => c.agent === request.agent && c.action === request.action && c.scope === request.scope && c.expiresAt > Date.now()
        );
        
        if (existing) {
          console.log(`Auto-approving consent for ${request.agent} (${request.action}) due to active session.`);
          // Fire API call or whatever callback is needed here in a real scenario
          return;
        }
        
        set((state) => ({ activePrompts: [...state.activePrompts, request] }));
      },
      removePrompt: (id) => set((state) => ({
        activePrompts: state.activePrompts.filter((prompt) => prompt.id !== id),
      })),
      grantConsent: (request, durationHours) => {
        const expiresAt = Date.now() + durationHours * 3600 * 1000;
        set((state) => ({
          grantedConsents: [
            ...state.grantedConsents.filter(c => !(c.agent === request.agent && c.action === request.action && c.scope === request.scope)),
            { agent: request.agent, action: request.action, scope: request.scope, expiresAt }
          ]
        }));
        get().removePrompt(request.id);
      },
      clearExpiredConsents: () => {
        set((state) => ({
          grantedConsents: state.grantedConsents.filter(c => c.expiresAt > Date.now())
        }));
      }
    }),
    {
      name: 'consent-storage',
      partialize: (state) => ({ grantedConsents: state.grantedConsents })
    }
  )
);
