# ARCHITECTURE — AI Job Discovery Platform

## System Role
An autonomous, AI-driven backend engine paired with a highly responsive frontend dashboard designed to discover, filter, and score job opportunities based on a hyper-personalized professional profile.

## Personas
1. **The Candidate (End User)**: Consumes curated job feeds, approves AI-generated cover letters, and utilizes the platform to optimize application efforts.
2. **The Developer/AI Agent**: Interacts with the platform via strict ReAct loops, managing the infrastructure, adding scraper capabilities, and debugging observability metrics.

## Primary Objective
To drastically reduce the "time-to-application" metric while increasing the "interview-to-application" ratio through high-fidelity, RAG-powered personalization and intelligent filtering.

## Platform Priorities
- **Deterministic AI Outcomes**: No rogue agents. All AI actions are bounded by strict contracts.
- **Observability**: If an agent hallucinates or a scraper breaks, the system must emit immediately actionable alerts.
- **Modularity**: Scrapers, agents, and infrastructure must be loosely coupled to survive UI/API changes from target websites.
