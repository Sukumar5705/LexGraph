from pathlib import Path
import json


def load_cases(path):
    cases = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            cases.append(json.loads(line))

    return cases


def build_case_nodes():

    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "processed"
        / "cases_2023.jsonl"
    )

    output_dir = project_root / "data" / "graph"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = (
        output_dir
        / "case_nodes_2023.jsonl"
    )

    print("Loading cases...")

    cases = load_cases(input_path)

    nodes = []

    for case in cases:

        source_path = case.get("source_path", "")

        node_id = Path(source_path).stem

        node = {
            "node_id": node_id,
            "case_id": case.get("case_id"),
            "title": case.get("title"),
            "citation": case.get("citation"),
            "decision_date": case.get("decision_date"),
            "judge": case.get("judge"),
            "court": case.get("court"),
            "disposal_nature": case.get("disposal_nature"),
            "source_path": source_path,
            "node_type": "case",
        }

        nodes.append(node)

    print("Saving case nodes...")

    with output_path.open("w", encoding="utf-8") as file:

        for node in nodes:
            file.write(
                json.dumps(
                    node,
                    ensure_ascii=False
                )
                + "\n"
            )

    print("\n--- COMPLETE ---")
    print(f"Cases: {len(cases)}")
    print(f"Nodes created: {len(nodes)}")
    print(f"Output: {output_path}")

    print("\n--- FIRST NODE ---")
    print(nodes[0])


if __name__ == "__main__":
    build_case_nodes()