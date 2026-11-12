# Knowledge Graph — Node Schema (Draft)

Status: **DRAFT / PLACEHOLDER** — to be finalized during the architecture
phase (see `docs/architecture/`).

## Candidate node types

- `Case` — a legal case/precedent (properties: case_id, title, court,
  decision_date, citation, ...)
- `Court` — a court entity (properties: name, level/hierarchy rank, ...)
- `Judge` — a judge entity (properties: name, ...)
- `Statute` — a statute/act referenced by a case
- `Section` — a specific section of a statute

> TODO: finalize exact property lists once the dataset schema is confirmed.
> No example/sample node instances are included here.
