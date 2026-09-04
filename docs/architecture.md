# LocalConnect AI Architecture

## Phase 1

User
↓
React Frontend
↓
FastAPI Backend

The current phase establishes the application foundation.

Future phases will introduce:

React
↓
FastAPI
↓
├── Lead Extraction
│   ↓
│   LLM
│   ↓
│   PostgreSQL
│
├── RAG
│   ↓
│   Embeddings
│   ↓
│   pgvector
│   ↓
│   Relevant Documents
│   ↓
│   LLM
│
└── MCP
    ↓
    AI Agent
    ↓
    Business Actions