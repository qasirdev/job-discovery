# SKILLS — Orchestrator Agent

This file outlines the sequencing skills of the Orchestrator Agent.

## 1. Pipeline State Machine
- Guide incoming items sequentially through: Security $\rightarrow$ Ranking $\rightarrow$ RAG Context Extraction $\rightarrow$ Cover Letter Drafting.
- Halt processing instantly on a failed safety gate.

## 2. Dynamic Threshold Dispatching
- Route only top-tier postings (score $> 80$) to RAG/Cover Letter services to conserve processing cost and token budgets.
