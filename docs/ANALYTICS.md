# ANALYTICS & USER TRACKING

To continuously improve the platform experience and agent effectiveness, we integrate comprehensive analytics tracking.

## Integrations
- **Microsoft Clarity**: Embedded in the Next.js frontend for deep UX insights.

### Microsoft Clarity Integration Instructions
1. Obtain the Clarity Project ID from the Clarity dashboard.
2. Add the ID to the `.env` file as `NEXT_PUBLIC_CLARITY_PROJECT_ID`.
3. Add the Clarity script to `frontend/app/layout.tsx` within the `<head>` tag.
4. If the GDPR consent banner is active, ensure the script is only loaded after user consent is granted.

## Tracked Signals
We monitor the following signals to identify UX bottlenecks:
- **User Journeys**: Flow through onboarding, application tracking, and job discovery.
- **Rage Clicks**: Highlighting frustration points in the UI (e.g., unresponsive buttons during loading).
- **Session Replay**: Reviewing problematic sessions to understand user intent vs platform behaviour.
- **UX Bottlenecks**: Identifying drop-off points in the application flow.
