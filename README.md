# Authority- and Temporal-Aware Knowledge Graph RAG Framework for Indian Legal Precedent Retrieval

## 1. Project Overview

This repository contains the source code, documentation, and evaluation
scaffolding for a CSE final-year research project on retrieval-augmented
generation (RAG) for Indian legal precedent research.

The core research contribution is an **authority-aware and temporally-aware
ranking mechanism** layered on top of a hybrid (lexical + vector + knowledge
graph) retrieval pipeline, aimed at improving the reliability of AI-assisted
Indian legal case research.

> **Status:** This repository is currently a **project skeleton**. Modules
> contain interface definitions, docstrings, and `TODO` markers only. No
> legal data, experimental results, or performance numbers have been added
> yet — these will only be added once real data and real experiments exist.

## 2. Research Baselines (Evaluation Ladder)

The project is evaluated against an incremental ladder of baselines, from
simplest to the proposed method:

```
BM25  →  Vector RAG  →  Hybrid RAG  →  GraphRAG  →  Authority + Temporal-Aware GraphRAG (proposed)
```

Each baseline is implemented independently under `evaluation/baselines/` so
that comparisons are fair and reproducible.

## 3. High-Level Development Flow

```
data/  →  ingestion/  →  knowledge_graph/  →  retrieval/  →  backend/core/  →  frontend/  →  evaluation/  →  docs/paper/
```

## 4. Folder Structure

```
authority-aware-graphrag/
├── backend/           FastAPI backend: API routes, core RAG pipeline, agents, models, utils
├── frontend/           React frontend: search UI, case explorer, knowledge graph view
├── data/               Raw / processed / metadata / benchmark data (empty — no data checked in)
├── knowledge_graph/    Graph schema, Cypher scripts, graph-building scripts
├── ingestion/           Downloading, extraction, preprocessing, chunking of source documents
├── retrieval/           BM25, vector, hybrid, and reranking retrieval modules
├── evaluation/          Baselines, metrics, experiment runners, and results
├── notebooks/           Exploratory analysis notebooks
├── tests/                Unit test placeholders for every core module
├── docs/                 Literature review, base paper notes, architecture, methodology, experiments, paper drafts
└── scripts/              Setup and run scripts
```

See `docs/PROJECT_GUIDE.md` (and the accompanying guide document) for a
walkthrough of the repository and suggested build order.

## 5. Tech Stack (kept intentionally minimal)

- **Backend:** Python, FastAPI
- **Frontend:** React (Vite)
- **Graph database:** Neo4j
- **Vector store:** to be finalized (e.g. a local/managed vector database) — see `retrieval/vector/`
- **Lexical retrieval:** BM25 (e.g. via `rank_bm25` or Elasticsearch — TBD)
- **LLM / embeddings:** pluggable via `backend/core/llm_service.py`

No blockchain, no quantum computing, no unrelated AI components are used in
this project.

## 6. Getting Started

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r ../requirements.txt
cp ../.env.example ../.env   # then fill in real values locally, never commit .env
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Environment variables
Copy `.env.example` to `.env` and fill in real values. **Never commit `.env`.**

## 7. Important Notes

- No legal judgments, datasets, or benchmark data are included in this
  repository. The final dataset(s) have not yet been selected — see
  `data/README.md`.
- No experimental results, accuracy numbers, or graphs are included yet.
  These will be added only once real experiments have been run, under
  `evaluation/results/` and `docs/experiments/`.
- No API keys or credentials are hardcoded anywhere in this repository.
  Use `.env` (git-ignored) for all secrets.

## 8. License

TBD (add a license once decided, e.g. MIT/Apache-2.0 for code; note that any
third-party legal data used must respect its own licensing/usage terms).
