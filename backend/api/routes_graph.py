"""
Knowledge graph API routes.

Exposes the existing citation knowledge graph stored in
data/graph/knowledge_graph_2023.gpickle.

This reuses the same graph already loaded by the RAG pipeline.
"""

from pathlib import Path
import pickle

from fastapi import APIRouter, HTTPException


router = APIRouter()


# ---------------------------------------------------------
# Knowledge graph loading
# ---------------------------------------------------------

_graph = None
_case_id_to_node = {}


def get_graph():
    """
    Lazily load the existing citation knowledge graph.

    The graph is loaded only when the graph API is actually
    requested, so normal application startup remains lightweight.
    """

    global _graph
    global _case_id_to_node

    if _graph is not None:
        return _graph

    project_root = Path(__file__).resolve().parents[2]

    graph_path = (
        project_root
        / "data"
        / "graph"
        / "knowledge_graph_2023.gpickle"
    )

    if not graph_path.exists():
        raise FileNotFoundError(
            f"Knowledge graph not found: {graph_path}"
        )

    print("[GRAPH API] Loading knowledge graph...", flush=True)

    with graph_path.open("rb") as file:
        _graph = pickle.load(file)

    print(
        "[GRAPH API] Knowledge graph loaded: "
        f"{_graph.number_of_nodes()} nodes, "
        f"{_graph.number_of_edges()} edges",
        flush=True,
    )

    # Build case ID → node ID mapping.
    for node_id, data in _graph.nodes(data=True):

        if data.get("node_type") != "case":
            continue

        case_id = data.get("case_id")

        if not case_id:
            continue

        normalized = (
            str(case_id)
            .strip()
            .upper()
        )

        _case_id_to_node[normalized] = node_id

    return _graph


# ---------------------------------------------------------
# Subgraph endpoint
# ---------------------------------------------------------

@router.get("/subgraph")
def get_subgraph(case_id: str):

    if not case_id or not case_id.strip():
        raise HTTPException(
            status_code=400,
            detail="case_id is required.",
        )

    graph = get_graph()

    normalized_case_id = (
        case_id.strip().upper()
    )

    source_node = _case_id_to_node.get(
        normalized_case_id
    )

    if source_node is None:
        raise HTTPException(
            status_code=404,
            detail=f"Case not found in knowledge graph: {case_id}",
        )

    nodes = []
    edges = []

    included_nodes = set()

    # -----------------------------------------------------
    # Add the selected case
    # -----------------------------------------------------

    included_nodes.add(source_node)

    source_data = graph.nodes[source_node]

    nodes.append(
        {
            "id": str(source_node),
            "case_id": source_data.get("case_id"),
            "title": source_data.get("title"),
            "citation": source_data.get("citation"),
            "decision_date": source_data.get(
                "decision_date"
            ),
            "node_type": source_data.get(
                "node_type"
            ),
            "role": "selected_case",
        }
    )

    # -----------------------------------------------------
    # Add one-hop citation relationships
    # -----------------------------------------------------

    # Cases cited BY the selected case.
    for _, target_node, edge_data in graph.out_edges(
        source_node,
        data=True,
    ):

        if edge_data.get("relationship") != "cites":
            continue

        target_data = graph.nodes[target_node]

        if target_data.get("node_type") != "case":
            continue

        included_nodes.add(target_node)

        nodes.append(
            {
                "id": str(target_node),
                "case_id": target_data.get("case_id"),
                "title": target_data.get("title"),
                "citation": target_data.get("citation"),
                "decision_date": target_data.get(
                    "decision_date"
                ),
                "node_type": target_data.get(
                    "node_type"
                ),
                "role": "cited_case",
            }
        )

        edges.append(
            {
                "source": str(source_node),
                "target": str(target_node),
                "relationship": "cites",
                "confidence": edge_data.get(
                    "confidence"
                ),
            }
        )

    # Cases that CITE the selected case.
    for source_node_2, _, edge_data in graph.in_edges(
        source_node,
        data=True,
    ):

        if edge_data.get("relationship") != "cites":
            continue

        source_data_2 = graph.nodes[source_node_2]

        if source_data_2.get("node_type") != "case":
            continue

        included_nodes.add(source_node_2)

        nodes.append(
            {
                "id": str(source_node_2),
                "case_id": source_data_2.get(
                    "case_id"
                ),
                "title": source_data_2.get(
                    "title"
                ),
                "citation": source_data_2.get(
                    "citation"
                ),
                "decision_date": source_data_2.get(
                    "decision_date"
                ),
                "node_type": source_data_2.get(
                    "node_type"
                ),
                "role": "citing_case",
            }
        )

        edges.append(
            {
                "source": str(source_node_2),
                "target": str(source_node),
                "relationship": "cites",
                "confidence": edge_data.get(
                    "confidence"
                ),
            }
        )

    # -----------------------------------------------------
    # Remove duplicate nodes
    # -----------------------------------------------------

    unique_nodes = {}

    for node in nodes:
        unique_nodes[node["id"]] = node

    nodes = list(unique_nodes.values())

    return {
        "success": True,
        "case_id": case_id,
        "nodes": nodes,
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }