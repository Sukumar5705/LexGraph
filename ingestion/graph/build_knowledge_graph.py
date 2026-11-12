from pathlib import Path
import json

import networkx as nx


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            records.append(json.loads(line))

    return records


def build_knowledge_graph():

    project_root = Path(__file__).resolve().parents[2]

    nodes_path = (
        project_root
        / "data"
        / "graph"
        / "case_nodes_2023.jsonl"
    )

    edges_path = (
        project_root
        / "data"
        / "graph"
        / "citation_edges_2023.jsonl"
    )

    output_dir = project_root / "data" / "graph"
    output_dir.mkdir(parents=True, exist_ok=True)

    graph_path = (
        output_dir
        / "knowledge_graph_2023.gpickle"
    )

    print("Loading case nodes...")
    case_nodes = load_jsonl(nodes_path)

    print("Loading citation edges...")
    citation_edges = load_jsonl(edges_path)

    graph = nx.MultiDiGraph()

    # --------------------------------------------------
    # 1. Add CASE nodes
    # --------------------------------------------------

    print("Adding case nodes...")

    for case in case_nodes:

        node_id = case["node_id"]

        graph.add_node(
            node_id,
            node_type="case",
            case_id=case.get("case_id"),
            title=case.get("title"),
            citation=case.get("citation"),
            decision_date=case.get("decision_date"),
            judge=case.get("judge"),
            court=case.get("court"),
            disposal_nature=case.get(
                "disposal_nature"
            ),
            source_path=case.get(
                "source_path"
            ),
        )

    # --------------------------------------------------
    # 2. Add JUDGE nodes
    # --------------------------------------------------

    print("Adding judge nodes...")

    for case in case_nodes:

        judge_value = case.get("judge")

        if not judge_value:
            continue

        judge_name = judge_value.strip()

        judge_id = f"judge::{judge_name}"

        graph.add_node(
            judge_id,
            node_type="judge",
            name=judge_name,
        )

        graph.add_edge(
            case["node_id"],
            judge_id,
            relationship="heard_by",
        )

    # --------------------------------------------------
    # 3. Add COURT nodes
    # --------------------------------------------------

    print("Adding court nodes...")

    for case in case_nodes:

        court_value = case.get("court")

        if not court_value:
            continue

        court_name = court_value.strip()

        court_id = f"court::{court_name}"

        graph.add_node(
            court_id,
            node_type="court",
            name=court_name,
        )

        graph.add_edge(
            case["node_id"],
            court_id,
            relationship="decided_by",
        )

    # --------------------------------------------------
    # 4. Add CITATION edges
    # --------------------------------------------------

    print("Adding citation edges...")

    for edge in citation_edges:

        source = edge["source"]
        target = edge["target"]

        if source not in graph:
            continue

        if target not in graph:
            continue

        graph.add_edge(
            source,
            target,
            relationship="cites",
            confidence=edge.get(
                "confidence"
            ),
        )

    # --------------------------------------------------
    # 5. Print graph statistics
    # --------------------------------------------------

    case_count = sum(
        1
        for _, data in graph.nodes(data=True)
        if data.get("node_type") == "case"
    )

    judge_count = sum(
        1
        for _, data in graph.nodes(data=True)
        if data.get("node_type") == "judge"
    )

    court_count = sum(
        1
        for _, data in graph.nodes(data=True)
        if data.get("node_type") == "court"
    )

    citation_count = sum(
        1
        for _, _, data in graph.edges(data=True)
        if data.get("relationship") == "cites"
    )

    print("\n--- GRAPH COMPLETE ---")

    print(f"Total nodes: {graph.number_of_nodes()}")
    print(f"Total edges: {graph.number_of_edges()}")

    print(f"Case nodes: {case_count}")
    print(f"Judge nodes: {judge_count}")
    print(f"Court nodes: {court_count}")
    print(f"Citation edges: {citation_count}")

    print("\nSaving graph...")

    # NetworkX 3.x no longer provides nx.write_gpickle,
    # so we use Python's pickle module directly.
    import pickle

    with graph_path.open("wb") as file:
        pickle.dump(
            graph,
            file,
            protocol=pickle.HIGHEST_PROTOCOL,
        )

    print(f"Graph saved to: {graph_path}")


if __name__ == "__main__":
    build_knowledge_graph()