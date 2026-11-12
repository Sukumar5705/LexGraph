# Knowledge Graph — Relationship Schema (Draft)

Status: **DRAFT / PLACEHOLDER**.

## Candidate relationship types

- `(Case)-[:CITES]->(Case)`
- `(Case)-[:OVERRULES]->(Case)`
- `(Case)-[:DISTINGUISHES]->(Case)`
- `(Case)-[:FOLLOWS]->(Case)`
- `(Case)-[:DECIDED_BY]->(Court)`
- `(Case)-[:REFERENCES]->(Section)`
- `(Section)-[:PART_OF]->(Statute)`

> TODO: finalize relationship taxonomy and directionality; align with
> `backend/models/citation.py`. No example/sample relationship instances
> are included here.
