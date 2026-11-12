# Project Guide

This file is a short pointer into the documentation set. A more detailed,
narrative version of this guide is also provided as a separate Word
document (see the project deliverables) for offline reading and for adding
your own notes.

## Documentation folders

- `project_proposal/` - the original/locked proposal materials
  (problem statement, research gap, novelty statement).
- `literature_review/` - the literature overlap analysis (NyayGraph,
  LegalGraphRAG, Falkor-IRAC, Domain-Partitioned Hybrid RAG, etc.) and
  positioning notes for the proposal defense.
- `base_paper/` - notes on the base paper(s) this project extends or is
  most closely compared against.
- `architecture/` - system architecture, knowledge graph schema decisions,
  authority-scoring formula, agent design, tech stack.
- `methodology/` - dataset selection process, evaluation/ablation study
  design, experimental protocol.
- `experiments/` - experiment logs and (eventually) results write-ups.
  Empty until real experiments are run.
- `paper/` - drafts of the eventual research paper / final report.

## Suggested build order

1. Finalize dataset source(s) -> `docs/methodology/dataset_plan.md`
2. Implement `ingestion/` against real data
3. Implement `knowledge_graph/` build scripts
4. Implement `retrieval/` (BM25 -> vector -> hybrid)
5. Implement `backend/core/graph_retriever.py`
6. Implement `backend/core/authority_ranker.py` and `temporal_validator.py`
   (the core novelty)
7. Implement `backend/core/conflict_detector.py` and `citation_verifier.py`
8. Wire everything together in `backend/core/rag_pipeline.py`
9. Implement `frontend/`
10. Run `evaluation/experiments/run_baselines.py`, then
    `run_authority_experiment.py`, then `run_ablation.py`
11. Write up results in `docs/experiments/` and `docs/paper/`
