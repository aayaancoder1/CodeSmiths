# CodeSmiths

# AI Company Brain

An enterprise knowledge intelligence platform that transforms fragmented organizational data into a searchable, explainable, and actionable organizational memory system.

---

# Problem Statement

Employees spend approximately 20% of their working hours searching for information across:

- Google Drive
- Confluence
- Notion
- Slack
- Teams
- Jira
- Internal documentation
- Email
- Ticketing systems

Traditional enterprise search engines return documents.

We aim to build a system that returns:

- Answers
- Context
- Relationships
- Organizational memory
- Actionable workflows

---

# Vision

Build an AI-powered organizational brain capable of:

- Understanding company knowledge
- Building organizational memory
- Reasoning across disconnected systems
- Executing workflows
- Preserving institutional knowledge

---

# Core Features

## Unified Data Connectors

Connect and ingest:

- Google Drive
- Notion/Wiki
- Slack
- Jira
- Internal documents

---

## Hybrid Retrieval Engine

Combination of:

- BM25 lexical search
- Dense vector search
- Cross-encoder reranking

---

## Knowledge Graph

Create an organizational graph containing:

- Employees
- Teams
- Projects
- Incidents
- Products
- Documents
- Decisions

---

## Graph-Augmented RAG

Question answering through:

Question
↓
Hybrid Retrieval
↓
Knowledge Graph Expansion
↓
Reranking
↓
LLM Synthesis
↓
Citations

---

## Multi-Agent Workflows

Agents capable of:

- Planning
- Tool execution
- Ticket creation
- Document generation
- Incident analysis

---

## Enterprise Governance

- ACL enforcement
- Audit logs
- Permission filtering
- Multi-tenancy

---

# Additional Features Beyond Problem Statement

## Organizational Decision Memory

Track:

- Why decisions were made
- Who made them
- When they were made

---

## Expertise Discovery

Example:

"Who knows the payment service best?"

---

## Knowledge Gap Detection

Detect:

- Missing documentation
- Missing ownership
- Unanswered organizational questions

---

## Incident Timeline Reconstruction

Automatically reconstruct:

- Events
- Discussions
- Tickets
- Root causes

---

## Employee Onboarding Generator

Generate personalized onboarding paths for:

- Developers
- Managers
- Designers
- Operations teams

---

## Proactive Briefings

Daily summaries:

- New incidents
- Project updates
- Knowledge changes

---

# Architecture

Frontend
↓
API Gateway
↓
AI Services
(RAG + KG + Agents)
↓
Domain Services
↓
Databases

---

# Tech Stack

Frontend:
- React
- Tailwind

Backend:
- FastAPI

Databases:
- PostgreSQL
- Neo4j
- Qdrant

AI:
- LangGraph
- LlamaIndex
- Rerankers

Infrastructure:
- Docker
- Redis

---

# Team

Aayaan
- AI/RAG
- Knowledge Graph
- Retrieval

Kishan
- Backend
- Ingestion
- Permissions

Thanmayee
- Frontend
- Dashboard

Nikshitha
- Agents
- DevOps
- Testing

---

# Branch Workflow

feature/*
        ↓
integration
        ↓
testing
        ↓
main
