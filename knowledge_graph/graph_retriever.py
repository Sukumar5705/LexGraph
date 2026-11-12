from pathlib import Path
import pickle


class GraphRetriever:
    """
    Retrieves graph relationships for legal cases.

    Currently supports:
    - cases cited by a case
    - cases citing a case
    - judge associated with a case
    - court associated with a case
    """

    def __init__(self):

        project_root = Path(__file__).resolve().parents[1]

        graph_path = (
            project_root
            / "data"
            / "graph"
            / "knowledge_graph_2023.gpickle"
        )

        print("Loading knowledge graph...")

        with graph_path.open("rb") as file:
            self.graph = pickle.load(file)

        print(
            f"Knowledge graph loaded: "
            f"{self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges"
        )

    def get_case_node(self, case_id):
        """
        Find the graph node corresponding to a case ID.
        """

        for node_id, data in self.graph.nodes(
            data=True
        ):

            if (
                data.get("node_type") == "case"
                and data.get("case_id") == case_id
            ):
                return node_id

        return None

    def get_cited_cases(self, case_id):
        """
        Return cases directly cited by the given case.
        """

        node_id = self.get_case_node(case_id)

        if node_id is None:
            return []

        results = []

        for _, target, edge_data in self.graph.out_edges(
            node_id,
            data=True
        ):

            if edge_data.get("relationship") != "cites":
                continue

            target_data = self.graph.nodes[target]

            if target_data.get("node_type") != "case":
                continue

            results.append(
                {
                    "case_id": target_data.get(
                        "case_id"
                    ),
                    "title": target_data.get(
                        "title"
                    ),
                    "citation": target_data.get(
                        "citation"
                    ),
                    "decision_date": target_data.get(
                        "decision_date"
                    ),
                    "relationship": "cited_by_case",
                }
            )

        return results

    def get_citing_cases(self, case_id):
        """
        Return cases that cite the given case.
        """

        node_id = self.get_case_node(case_id)

        if node_id is None:
            return []

        results = []

        for source, _, edge_data in self.graph.in_edges(
            node_id,
            data=True
        ):

            if edge_data.get("relationship") != "cites":
                continue

            source_data = self.graph.nodes[source]

            if source_data.get("node_type") != "case":
                continue

            results.append(
                {
                    "case_id": source_data.get(
                        "case_id"
                    ),
                    "title": source_data.get(
                        "title"
                    ),
                    "citation": source_data.get(
                        "citation"
                    ),
                    "decision_date": source_data.get(
                        "decision_date"
                    ),
                    "relationship": "cites_case",
                }
            )

        return results

    def get_judge(self, case_id):
        """
        Return the judge associated with a case.
        """

        node_id = self.get_case_node(case_id)

        if node_id is None:
            return None

        for _, target, edge_data in self.graph.out_edges(
            node_id,
            data=True
        ):

            if edge_data.get("relationship") != "heard_by":
                continue

            target_data = self.graph.nodes[target]

            if target_data.get("node_type") == "judge":
                return target_data.get("name")

        return None

    def get_court(self, case_id):
        """
        Return the court associated with a case.
        """

        node_id = self.get_case_node(case_id)

        if node_id is None:
            return None

        for _, target, edge_data in self.graph.out_edges(
            node_id,
            data=True
        ):

            if edge_data.get("relationship") != "decided_by":
                continue

            target_data = self.graph.nodes[target]

            if target_data.get("node_type") == "court":
                return target_data.get("name")

        return None

    def expand_case(self, case_id):
        """
        Return all currently supported graph information
        for a case.
        """

        return {
            "case_id": case_id,
            "cited_cases": self.get_cited_cases(
                case_id
            ),
            "citing_cases": self.get_citing_cases(
                case_id
            ),
            "judge": self.get_judge(
                case_id
            ),
            "court": self.get_court(
                case_id
            ),
        }