from pathlib import Path
import pickle
from collections import Counter


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GRAPH_PATH = (
    PROJECT_ROOT
    / "data"
    / "graph"
    / "knowledge_graph_2023.gpickle"
)


print("Loading knowledge graph...")

with GRAPH_PATH.open("rb") as file:
    graph = pickle.load(file)


print("\n--- GRAPH VALIDATION ---")

print(f"Nodes: {graph.number_of_nodes()}")
print(f"Edges: {graph.number_of_edges()}")


# Count relationship types
relationship_counts = Counter(
    data.get("relationship")
    for _, _, data in graph.edges(data=True)
)

print("\nRelationship counts:")

for relationship, count in relationship_counts.items():
    print(f"{relationship}: {count}")


# Check cases missing judge relationships
missing_judge = []

for node_id, data in graph.nodes(data=True):

    if data.get("node_type") != "case":
        continue

    has_judge = any(
        edge_data.get("relationship") == "heard_by"
        for _, _, edge_data
        in graph.out_edges(node_id, data=True)
    )

    if not has_judge:
        missing_judge.append(node_id)


# Check cases missing court relationships
missing_court = []

for node_id, data in graph.nodes(data=True):

    if data.get("node_type") != "case":
        continue

    has_court = any(
        edge_data.get("relationship") == "decided_by"
        for _, _, edge_data
        in graph.out_edges(node_id, data=True)
    )

    if not has_court:
        missing_court.append(node_id)


print("\nCases missing judge:", len(missing_judge))
print("Cases missing court:", len(missing_court))


if missing_judge:
    print("\nFirst missing-judge cases:")
    for node_id in missing_judge[:10]:
        print(node_id)


if missing_court:
    print("\nFirst missing-court cases:")
    for node_id in missing_court[:10]:
        print(node_id)


print("\n--- VALIDATION COMPLETE ---")