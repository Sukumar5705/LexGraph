from knowledge_graph.graph_retriever import GraphRetriever


class AuthorityRanker:
    """
    Graph-aware authority reranker.

    Combines:
    - hybrid RRF retrieval score
    - graph authority score
    - optional cross-encoder relevance score
    """

    def __init__(self):

        print("Initializing authority ranker...")

        self.graph_retriever = GraphRetriever()

    def calculate_authority_score(
        self,
        case_id
    ):
        """
        Calculate a graph-based authority score.

        Citing cases receive a stronger weight than
        cases cited by the candidate.
        """

        graph_data = (
            self.graph_retriever.expand_case(
                case_id
            )
        )

        citing_count = len(
            graph_data["citing_cases"]
        )

        cited_count = len(
            graph_data["cited_cases"]
        )

        authority_score = (
            2.0 * citing_count
            + 1.0 * cited_count
        )

        return {
            "authority_score": authority_score,
            "citing_count": citing_count,
            "cited_count": cited_count,
        }

    def _normalize_cross_encoder_scores(
        self,
        results
    ):
        """
        Min-max normalize cross-encoder scores
        to the range 0-1.
        """

        scores = [
            result.get(
                "cross_encoder_score"
            )
            for result in results
        ]

        scores = [
            score
            for score in scores
            if score is not None
        ]

        if not scores:
            return {}

        minimum = min(scores)
        maximum = max(scores)

        if maximum == minimum:

            return {
                id(result): 1.0
                for result in results
            }

        normalized = {}

        for result in results:

            score = result.get(
                "cross_encoder_score"
            )

            if score is None:
                normalized[
                    id(result)
                ] = 0.0

            else:

                normalized[
                    id(result)
                ] = (
                    (score - minimum)
                    / (maximum - minimum)
                )

        return normalized

    def rerank(
        self,
        results,
        authority_weight=0.10,
        cross_encoder_weight=0.30
    ):
        """
        Apply graph authority and optional
        cross-encoder relevance.

        The current weights are intentionally
        conservative:

            RRF                 = main retrieval signal
            Cross encoder       = 0.30
            Authority           = 0.10
        """

        if not results:
            return []

        normalized_cross_scores = (
            self._normalize_cross_encoder_scores(
                results
            )
        )

        reranked = []

        for result in results:

            case_id = result.get(
                "case_id"
            )

            authority = (
                self.calculate_authority_score(
                    case_id
                )
            )

            rrf_score = result.get(
                "rrf_score",
                0.0
            )

            authority_score = authority[
                "authority_score"
            ]

            normalized_cross_score = (
                normalized_cross_scores.get(
                    id(result),
                    0.0
                )
            )

            final_score = (
                rrf_score
                + (
                    authority_weight
                    * authority_score
                )
                + (
                    cross_encoder_weight
                    * normalized_cross_score
                )
            )

            updated_result = dict(result)

            updated_result[
                "authority_score"
            ] = authority_score

            updated_result[
                "citing_count"
            ] = authority[
                "citing_count"
            ]

            updated_result[
                "cited_count"
            ] = authority[
                "cited_count"
            ]

            updated_result[
                "normalized_cross_encoder_score"
            ] = normalized_cross_score

            updated_result[
                "final_score"
            ] = final_score

            reranked.append(
                updated_result
            )

        reranked.sort(
            key=lambda x: x[
                "final_score"
            ],
            reverse=True
        )

        return reranked