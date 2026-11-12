// Knowledge graph schema creation script (DRAFT / PLACEHOLDER)
// Status: not yet finalized — see knowledge_graph/schema/nodes.md and
// relationships.md. No sample data is created by this script.

// TODO: CREATE constraints/indexes for Case, Court, Judge, Statute, Section
// Example shape (do not run until schema is finalized):
// CREATE CONSTRAINT case_id_unique IF NOT EXISTS FOR (c:Case) REQUIRE c.case_id IS UNIQUE;
