from pathlib import Path
import json
import re


def load_jsonl(path):
    records = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            records.append(json.loads(line))

    return records


def normalize_case_id(case_id):
    """
    Normalize different INSC formats.

    Examples:
        2023 INSC 766
        2023:INSC:766
        2023:INSC: 766

    All become:

        2023 INSC 766
    """

    if not case_id:
        return None

    text = str(case_id).strip().upper()

    match = re.search(
        r"\b(\d{4})\s*:?\s*INSC\s*:?\s*(\d+)\b",
        text,
        re.IGNORECASE,
    )

    if not match:
        return None

    year = match.group(1)
    number = match.group(2)

    return f"{year} INSC {number}"


def normalize_title(title):
    """
    Normalize case titles for fallback matching.
    """

    if not title:
        return ""

    text = str(title).upper()

    # Make common separators equivalent
    text = text.replace("VERSUS", " V ")
    text = text.replace(" VS. ", " V ")
    text = text.replace(" VS ", " V ")
    text = text.replace(" V. ", " V ")

    # Remove punctuation
    text = re.sub(
        r"[^A-Z0-9\s]",
        " ",
        text
    )

    # Collapse whitespace
    text = " ".join(
        text.split()
    )

    return text


def extract_case_id_from_text(text):
    """
    Extract an INSC case ID from arbitrary text.

    Examples:

        2023 INSC 766
        2023:INSC:766
        2023:INSC: 766

    Returns normalized case ID or None.
    """

    if not text:
        return None

    match = re.search(
        r"\b(\d{4})\s*:?\s*INSC\s*:?\s*(\d+)\b",
        str(text),
        re.IGNORECASE,
    )

    if not match:
        return None

    return (
        f"{match.group(1)} "
        f"INSC "
        f"{match.group(2)}"
    )


def build_citation_graph():

    project_root = Path(__file__).resolve().parents[2]

    nodes_path = (
        project_root
        / "data"
        / "graph"
        / "case_nodes_2023.jsonl"
    )

    citation_path = (
        project_root
        / "data"
        / "graph"
        / "citation_records_2023.jsonl"
    )

    output_dir = (
        project_root
        / "data"
        / "graph"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        output_dir
        / "citation_edges_2023.jsonl"
    )

    print("Loading case nodes...")
    nodes = load_jsonl(
        nodes_path
    )

    print("Loading citation records...")
    citation_records = load_jsonl(
        citation_path
    )

    # -------------------------------------------------
    # Build case ID -> node ID mapping
    # -------------------------------------------------

    case_id_to_nodes = {}

    for node in nodes:

        case_id = node.get(
            "case_id"
        )

        node_id = node.get(
            "node_id"
        )

        if not case_id or not node_id:
            continue

        normalized_id = normalize_case_id(
            case_id
        )

        if not normalized_id:
            continue

        case_id_to_nodes.setdefault(
            normalized_id,
            []
        ).append(node_id)

    # -------------------------------------------------
    # Build normalized title -> node ID mapping
    # -------------------------------------------------

    title_to_nodes = {}

    for node in nodes:

        node_id = node.get(
            "node_id"
        )

        title = node.get(
            "title"
        )

        if not node_id or not title:
            continue

        normalized_title = normalize_title(
            title
        )

        if not normalized_title:
            continue

        title_to_nodes.setdefault(
            normalized_title,
            []
        ).append(node_id)

    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------

    edges = []
    seen = set()

    verified_internal = 0
    citation_id_matches = 0
    title_matches = 0
    ambiguous = 0
    external = 0
    unresolved = 0

    # -------------------------------------------------
    # Process citation records
    # -------------------------------------------------

    for record in citation_records:

        source_case_id = normalize_case_id(
            record.get(
                "source_case_id"
            )
        )

        if not source_case_id:
            continue

        source_nodes = case_id_to_nodes.get(
            source_case_id,
            []
        )

        # Source must identify exactly one document.
        if len(source_nodes) != 1:
            continue

        source_node_id = source_nodes[0]

        cited_citation = record.get(
            "cited_citation"
        )

        cited_case_name = record.get(
            "cited_case_name"
        )

        target_case_id = None
        target_nodes = []

        # -------------------------------------------------
        # METHOD 1:
        # Use explicit cited_citation
        # -------------------------------------------------

        if cited_citation:

            target_case_id = extract_case_id_from_text(
                cited_citation
            )

            if target_case_id:

                target_nodes = case_id_to_nodes.get(
                    target_case_id,
                    []
                )

                if len(target_nodes) == 1:

                    citation_id_matches += 1

        # -------------------------------------------------
        # METHOD 2:
        # Extract INSC ID from cited_case_name
        # -------------------------------------------------

        if not target_nodes:

            target_case_id = extract_case_id_from_text(
                cited_case_name
            )

            if target_case_id:

                target_nodes = case_id_to_nodes.get(
                    target_case_id,
                    []
                )

                if len(target_nodes) == 1:

                    citation_id_matches += 1

        # -------------------------------------------------
        # METHOD 3:
        # Match case title as fallback
        # -------------------------------------------------

        if not target_nodes and cited_case_name:

            normalized_cited_title = normalize_title(
                cited_case_name
            )

            matching_nodes = title_to_nodes.get(
                normalized_cited_title,
                []
            )

            if len(matching_nodes) == 1:

                target_nodes = matching_nodes

                target_case_id = (
                    nodes[
                        next(
                            i
                            for i, node in enumerate(nodes)
                            if node.get("node_id")
                            == matching_nodes[0]
                        )
                    ].get("case_id")
                )

                target_case_id = normalize_case_id(
                    target_case_id
                )

                title_matches += 1

        # -------------------------------------------------
        # No target found
        # -------------------------------------------------

        if not target_nodes:

            # If the cited case is an older/external case,
            # it simply isn't represented in the 2023 graph.
            external += 1
            continue

        # -------------------------------------------------
        # Ambiguous target
        # -------------------------------------------------

        if len(target_nodes) > 1:

            ambiguous += 1
            continue

        target_node_id = target_nodes[0]

        # -------------------------------------------------
        # Never create self-citation
        # -------------------------------------------------

        if source_node_id == target_node_id:
            continue

        edge_key = (
            source_node_id,
            target_node_id
        )

        if edge_key in seen:
            continue

        seen.add(
            edge_key
        )

        edges.append(
            {
                "source": source_node_id,
                "target": target_node_id,
                "source_case_id": source_case_id,
                "target_case_id": target_case_id,
                "relationship": "cites",
                "confidence": "verified_id",
            }
        )

        verified_internal += 1

    # -------------------------------------------------
    # Save edges
    # -------------------------------------------------

    print("\nSaving citation edges...")

    with output_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        for edge in edges:

            file.write(
                json.dumps(
                    edge,
                    ensure_ascii=False
                )
                + "\n"
            )

    # -------------------------------------------------
    # Final statistics
    # -------------------------------------------------

    print("\n--- COMPLETE ---")

    print(
        f"Nodes: {len(nodes)}"
    )

    print(
        f"Citation records: "
        f"{len(citation_records)}"
    )

    print(
        f"Verified internal edges: "
        f"{verified_internal}"
    )

    print(
        f"Resolved through INSC ID: "
        f"{citation_id_matches}"
    )

    print(
        f"Resolved through title: "
        f"{title_matches}"
    )

    print(
        f"Ambiguous citations skipped: "
        f"{ambiguous}"
    )

    print(
        f"External/unresolved records: "
        f"{external}"
    )

    print(
        f"Unique graph edges: "
        f"{len(edges)}"
    )

    print(
        f"Output: {output_path}"
    )


if __name__ == "__main__":
    build_citation_graph()