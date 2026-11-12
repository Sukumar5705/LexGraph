"""
rag_pipeline.py

Purpose
-------
Top-level orchestration of the authority-aware legal RAG pipeline.

Pipeline:

    Query
      ↓
    Hybrid Retrieval
      ↓
    Cross-Encoder Reranking
      ↓
    Authority Ranking
      ↓
    Graph Citation Expansion
      ↓
    Temporal Validation
      ↓
    Conflict Detection
      ↓
    Evidence Relevance Filtering
      ↓
    Grounded Context
      ↓
    Local LLM Generation
      ↓
    Citation Verification
      ↓
    Final Result
"""

from datetime import date
from pathlib import Path
import pickle
import re


from retrieval.hybrid.hybrid_retriever import (
    HybridRetriever,
)

from retrieval.reranking.cross_encoder import (
    CrossEncoderReranker,
)

from retrieval.reranking.authority_ranker import (
    AuthorityRanker,
)

from backend.core.temporal_validator import (
    TemporalValidator,
)

from backend.core.conflict_detector import (
    ConflictDetector,
)

from backend.core.citation_verifier import (
    CitationVerifier,
)

from backend.core.llm_service import (
    LLMService,
)


class RAGPipeline:

    def __init__(self):

        print("Initializing RAG pipeline...")

        # -----------------------------------------
        # Hybrid retrieval
        # -----------------------------------------

        self.hybrid_retriever = (
            HybridRetriever()
        )

        # -----------------------------------------
        # Cross encoder
        # -----------------------------------------

        self.cross_encoder = (
            CrossEncoderReranker()
        )

        # -----------------------------------------
        # Authority ranking
        # -----------------------------------------

        self.authority_ranker = (
            AuthorityRanker()
        )

        # -----------------------------------------
        # Knowledge graph
        # -----------------------------------------

        self._load_knowledge_graph()

        # -----------------------------------------
        # Temporal validation
        # -----------------------------------------

        self.temporal_validator = (
            TemporalValidator()
        )

        # -----------------------------------------
        # Conflict detection
        # -----------------------------------------

        self.conflict_detector = (
            ConflictDetector()
        )

        # -----------------------------------------
        # Citation verification
        # -----------------------------------------

        self.citation_verifier = (
            CitationVerifier()
        )

        # -----------------------------------------
        # LLM
        # -----------------------------------------

        self.llm_service = (
            LLMService()
        )

        print("RAG pipeline initialized.")

    # =========================================================
    # KNOWLEDGE GRAPH
    # =========================================================

    def _load_knowledge_graph(self):

        project_root = (
            Path(__file__).resolve().parents[2]
        )

        graph_path = (
            project_root
            / "data"
            / "graph"
            / "knowledge_graph_2023.gpickle"
        )

        print("Loading citation knowledge graph...")

        if not graph_path.exists():

            raise FileNotFoundError(
                f"Knowledge graph not found: "
                f"{graph_path}"
            )

        with graph_path.open(
            "rb"
        ) as file:

            self.knowledge_graph = (
                pickle.load(file)
            )

        print(
            "Citation knowledge graph loaded: "
            f"{self.knowledge_graph.number_of_nodes()} "
            f"nodes, "
            f"{self.knowledge_graph.number_of_edges()} "
            f"edges"
        )

        self.case_id_to_node = {}

        for node_id, data in (
            self.knowledge_graph.nodes(
                data=True
            )
        ):

            if data.get(
                "node_type"
            ) != "case":

                continue

            case_id = data.get(
                "case_id"
            )

            if not case_id:
                continue

            normalized = (
                str(case_id)
                .strip()
                .upper()
            )

            self.case_id_to_node[
                normalized
            ] = node_id

    # =========================================================
    # GRAPH CITATION EXPANSION
    # =========================================================

    def _get_cited_cases(
        self,
        case_id,
    ):

        if not case_id:
            return []

        normalized = (
            str(case_id)
            .strip()
            .upper()
        )

        source_node = (
            self.case_id_to_node.get(
                normalized
            )
        )

        if source_node is None:
            return []

        cited_cases = []

        for _, target_node, edge_data in (
            self.knowledge_graph.out_edges(
                source_node,
                data=True,
            )
        ):

            if edge_data.get(
                "relationship"
            ) != "cites":

                continue

            target_data = (
                self.knowledge_graph.nodes[
                    target_node
                ]
            )

            if target_data.get(
                "node_type"
            ) != "case":

                continue

            cited_cases.append(
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
                    "relationship": "cites",
                    "confidence": edge_data.get(
                        "confidence"
                    ),
                }
            )

        return cited_cases

    def _expand_graph_relationships(
        self,
        results,
    ):

        expanded = []

        for result in results:

            updated = dict(
                result
            )

            updated[
                "graph_citations"
            ] = self._get_cited_cases(
                result.get(
                    "case_id"
                )
            )

            expanded.append(
                updated
            )

        return expanded

    # =========================================================
    # TEXT NORMALIZATION
    # =========================================================

    def _normalize_text(
        self,
        text,
    ):

        if not text:
            return ""

        text = str(text).lower()

        text = re.sub(
            r"\s+",
            " ",
            text,
        )

        return text.strip()

    # =========================================================
    # QUERY TERM EXTRACTION
    # =========================================================

    def _extract_query_terms(
        self,
        query,
    ):

        normalized = (
            self._normalize_text(
                query
            )
        )

        important_phrases = [
            "order vii rule 11",
            "order 7 rule 11",
            "order vii rule 11 cpc",
            "order 7 rule 11 cpc",
            "rejection of plaint",
            "rejection of the plaint",
            "cause of action",
            "partial rejection",
            "code of civil procedure",
        ]

        terms = []

        for phrase in important_phrases:

            if phrase in normalized:

                terms.append(
                    phrase
                )

        words = re.findall(
            r"[a-z0-9]+",
            normalized,
        )

        stop_words = {
            "what",
            "which",
            "who",
            "where",
            "when",
            "why",
            "how",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "and",
            "or",
            "of",
            "in",
            "on",
            "to",
            "for",
            "from",
            "with",
            "under",
            "this",
            "that",
            "cases",
            "case",
            "retrieved",
            "evidence",
            "discuss",
            "discusses",
            "apply",
            "applies",
            "applied",
        }

        for word in words:

            if (
                len(word) >= 4
                and word not in stop_words
                and word not in terms
            ):

                if word not in terms:

                    terms.append(
                        word
                    )

        return terms

    # =========================================================
    # EVIDENCE RELEVANCE
    # =========================================================

    def _calculate_evidence_relevance(
        self,
        query,
        result,
    ):

        terms = (
            self._extract_query_terms(
                query
            )
        )

        text = self._normalize_text(
            result.get(
                "text",
                ""
            )
        )

        title = self._normalize_text(
            result.get(
                "title",
                ""
            )
        )

        combined = (
            text
            + " "
            + title
        )

        strong_phrases = [
            "order vii rule 11",
            "order 7 rule 11",
            "order vii rule 11 cpc",
            "order 7 rule 11 cpc",
            "rejection of the plaint",
            "rejection of plaint",
        ]

        strong_matches = 0

        for phrase in strong_phrases:

            if phrase in combined:

                strong_matches += 1

        term_matches = 0

        matched_terms = []

        for term in terms:

            if term in combined:

                term_matches += 1

                matched_terms.append(
                    term
                )

        graph_bonus = (
            1
            if result.get(
                "graph_citations"
            )
            else 0
        )

        relevance_score = (
            strong_matches * 10
            + term_matches * 2
            + graph_bonus
        )

        return {
            "relevance_score": (
                relevance_score
            ),
            "strong_matches": (
                strong_matches
            ),
            "term_matches": (
                term_matches
            ),
            "matched_terms": (
                matched_terms
            ),
            "graph_bonus": (
                graph_bonus
            ),
        }

    # =========================================================
    # SELECT RELEVANT EVIDENCE
    # =========================================================

    def _select_relevant_evidence(
        self,
        query,
        results,
        max_sources=5,
    ):

        if not results:
            return []

        # ---------------------------------------------------------
        # Preserve the primary retrieved case.
        #
        # `results` is already ordered by the retrieval/reranking
        # pipeline. The first result is therefore the primary
        # retrieved source shown to the user. It must not disappear
        # just because another case receives a higher evidence
        # relevance score.
        # ---------------------------------------------------------
        primary_result = dict(results[0])

        scored = []

        for result in results:

            updated = dict(result)

            relevance = (
                self._calculate_evidence_relevance(
                    query=query,
                    result=result,
                )
            )

            updated[
                "evidence_relevance"
            ] = relevance

            scored.append(updated)

        # Keep the original primary result's calculated relevance
        # metadata as well.
        primary_relevance = self._calculate_evidence_relevance(
            query=query,
            result=primary_result,
        )
        primary_result[
            "evidence_relevance"
        ] = primary_relevance

        # ---------------------------------------------------------
        # Rank the remaining evidence by evidence relevance.
        # The primary result is removed from this list so it cannot
        # be duplicated when we fill the remaining context slots.
        # ---------------------------------------------------------
        primary_case_id = str(
            primary_result.get("case_id", "")
        ).strip().upper()

        supporting = [
            item
            for item in scored
            if str(
                item.get("case_id", "")
            ).strip().upper() != primary_case_id
        ]

        supporting.sort(
            key=lambda item: (
                item[
                    "evidence_relevance"
                ][
                    "relevance_score"
                ],
                item.get(
                    "final_score",
                    0.0,
                ),
            ),
            reverse=True,
        )

        # ---------------------------------------------------------
        # Select supporting evidence.
        # Prefer cases with a direct legal-issue match, then cases
        # with term matches, and finally the strongest remaining
        # candidates.
        # ---------------------------------------------------------
        direct = [
            item
            for item in supporting
            if item[
                "evidence_relevance"
            ][
                "strong_matches"
            ] > 0
        ]

        term_matches = [
            item
            for item in supporting
            if item[
                "evidence_relevance"
            ][
                "term_matches"
            ] > 0
        ]

        selected_supporting = []
        seen_case_ids = {
            primary_case_id
        }

        # First add directly matching supporting cases.
        for item in direct:
            if len(selected_supporting) >= max_sources - 1:
                break

            case_id = str(
                item.get("case_id", "")
            ).strip().upper()

            if case_id in seen_case_ids:
                continue

            selected_supporting.append(item)
            seen_case_ids.add(case_id)

        # Then add term-matching cases if there are still slots.
        for item in term_matches:
            if len(selected_supporting) >= max_sources - 1:
                break

            case_id = str(
                item.get("case_id", "")
            ).strip().upper()

            if case_id in seen_case_ids:
                continue

            selected_supporting.append(item)
            seen_case_ids.add(case_id)

        # Finally fill any remaining slots with the strongest
        # remaining reranked candidates.
        for item in supporting:
            if len(selected_supporting) >= max_sources - 1:
                break

            case_id = str(
                item.get("case_id", "")
            ).strip().upper()

            if case_id in seen_case_ids:
                continue

            selected_supporting.append(item)
            seen_case_ids.add(case_id)

        selected = [
            primary_result
        ] + selected_supporting

        # If max_sources is 1, the primary case is still preserved.
        selected = selected[:max_sources]

        print(
            "\nEvidence relevance filtering:"
        )

        print(
            f"Retrieved/reranked sources: "
            f"{len(results)}"
        )

        print(
            f"Primary retrieved source preserved: "
            f"{primary_result.get('case_id')}"
        )

        print(
            f"Relevant context sources: "
            f"{len(selected)}"
        )

        for index, result in enumerate(
            selected,
            start=1,
        ):

            relevance = result[
                "evidence_relevance"
            ]

            print(
                f"  {index}. "
                f"{result.get('case_id')} | "
                f"relevance="
                f"{relevance.get('relevance_score', 0)} | "
                f"strong_matches="
                f"{relevance.get('strong_matches', 0)}"
            )

        return selected

    # =========================================================
    # BUILD DIRECTLY RETRIEVED CASE LIST
    # =========================================================

    def _build_direct_retrieved_case_summary(
        self,
        results,
    ):
        """
        Build an explicit list of the cases that were
        actually retrieved.

        This is passed separately to the LLM so it cannot
        confuse a case mentioned inside another judgment
        with a directly retrieved source.
        """

        lines = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            case_id = result.get(
                "case_id",
                "Unknown",
            )

            title = result.get(
                "title",
                "Unknown",
            )

            citation = result.get(
                "citation",
                "Unknown",
            )

            relevance = result.get(
                "evidence_relevance",
                {},
            )

            strong_matches = relevance.get(
                "strong_matches",
                0,
            )

            lines.append(
                f"{index}. "
                f"CASE ID: {case_id}\n"
                f"   TITLE: {title}\n"
                f"   CITATION: {citation}\n"
                f"   STRONG LEGAL-ISSUE MATCHES: "
                f"{strong_matches}"
            )

        if not lines:

            return (
                "No directly retrieved cases."
            )

        return "\n".join(
            lines
        )

    # =========================================================
    # BUILD INTERNAL MENTIONED-CASE SUMMARY
    # =========================================================

    def _extract_mentioned_case_citations(
        self,
        results,
    ):
        """
        Identify citation-like case references appearing
        inside retrieved text.

        This is diagnostic information only.

        It is deliberately NOT used as evidence that the
        mentioned case was independently retrieved.
        """

        mentioned = []

        # Indian SCC citation pattern.
        scc_pattern = re.compile(
            r"\(\d{4}\)\s+\d+\s+SCC\s+\d+",
            re.IGNORECASE,
        )

        # INSC case ID pattern.
        insc_pattern = re.compile(
            r"\b\d{4}\s+INSC\s+\d+\b",
            re.IGNORECASE,
        )

        directly_retrieved_ids = set()

        for result in results:

            case_id = result.get(
                "case_id"
            )

            if case_id:

                directly_retrieved_ids.add(
                    " ".join(
                        str(case_id)
                        .upper()
                        .split()
                    )
                )

        for result in results:

            text = result.get(
                "text",
                "",
            )

            if not text:
                continue

            citations = (
                scc_pattern.findall(
                    text
                )
            )

            insc_ids = (
                insc_pattern.findall(
                    text
                )
            )

            for citation in citations:

                normalized = (
                    " ".join(
                        citation.split()
                    )
                )

                mentioned.append(
                    {
                        "source_case_id": result.get(
                            "case_id"
                        ),
                        "citation": normalized,
                        "directly_retrieved": False,
                    }
                )

            for case_id in insc_ids:

                normalized = (
                    " ".join(
                        case_id.upper().split()
                    )
                )

                if normalized in (
                    directly_retrieved_ids
                ):
                    continue

                mentioned.append(
                    {
                        "source_case_id": result.get(
                            "case_id"
                        ),
                        "citation": normalized,
                        "directly_retrieved": False,
                    }
                )

        # Remove duplicates.

        unique = []

        seen = set()

        for item in mentioned:

            key = (
                item["source_case_id"],
                item["citation"],
            )

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                item
            )

        return unique

    # =========================================================
    # CONTEXT BUILDING
    # =========================================================

    def _build_context(
        self,
        results,
    ):

        if not results:

            return (
                "NO RELEVANT RETRIEVED "
                "EVIDENCE IS AVAILABLE."
            )

        parts = []

        MAX_TEXT_LENGTH = 3500

        for index, result in enumerate(
            results,
            start=1,
        ):

            text = result.get(
                "text",
                "",
            )

            if len(text) > MAX_TEXT_LENGTH:

                text = (
                    text[:MAX_TEXT_LENGTH]
                    + "\n[Source text truncated.]"
                )

            temporal = result.get(
                "temporal_validation",
                {},
            )

            graph_citations = result.get(
                "graph_citations",
                [],
            )

            if graph_citations:

                graph_lines = []

                for cited in graph_citations:

                    graph_lines.append(
                        f"- "
                        f"{result.get('case_id')} "
                        f"cites "
                        f"{cited.get('case_id')} "
                        f"("
                        f"{cited.get('title')}; "
                        f"{cited.get('citation')}"
                        f")"
                    )

                graph_text = (
                    "\n".join(
                        graph_lines
                    )
                )

            else:

                graph_text = "None"

            relevance = result.get(
                "evidence_relevance",
                {},
            )

            parts.append(
                f"""
==================================================
DIRECTLY RETRIEVED SOURCE {index}
==================================================

IMPORTANT:
This case is DIRECTLY RETRIEVED by the RAG system.

CASE ID:
{result.get('case_id', 'Unknown')}

TITLE:
{result.get('title', 'Unknown')}

CITATION:
{result.get('citation', 'Unknown')}

DECISION DATE:
{result.get('decision_date', 'Unknown')}

FINAL SCORE:
{result.get('final_score', 0.0):.6f}

AUTHORITY SCORE:
{result.get('authority_score', 0.0):.2f}

EVIDENCE RELEVANCE:
{relevance.get('relevance_score', 0)}

STRONG LEGAL-ISSUE MATCHES:
{relevance.get('strong_matches', 0)}

MATCHED TERMS:
{", ".join(relevance.get('matched_terms', []))}

TEMPORAL STATUS:
{temporal.get('status', 'unknown')}

TEMPORALLY VALID:
{temporal.get('temporally_valid', None)}

VERIFIED GRAPH CITATIONS:
{graph_text}

CASE TEXT:
{text}
""".strip()
            )

        return "\n\n".join(
            parts
        )

    # =========================================================
    # PROMPT
    # =========================================================

    def _build_prompt(
        self,
        query,
        conflict_report,
        relevant_results,
    ):

        # -----------------------------------------
        # Conflict information
        # -----------------------------------------

        if conflict_report[
            "conflict_detected"
        ]:

            conflict_lines = []

            for conflict in (
                conflict_report[
                    "conflicts"
                ]
            ):

                conflict_lines.append(
                    f"- "
                    f"{conflict['case_a']} "
                    f"conflicts with "
                    f"{conflict['case_b']}"
                )

            conflict_text = (
                "\n".join(
                    conflict_lines
                )
            )

        else:

            conflict_text = (
                "No explicit conflicts were detected."
            )

        # -----------------------------------------
        # Directly retrieved cases
        # -----------------------------------------

        direct_cases = (
            self._build_direct_retrieved_case_summary(
                relevant_results
            )
        )

        # -----------------------------------------
        # Mentioned authorities
        # -----------------------------------------

        mentioned = (
            self._extract_mentioned_case_citations(
                relevant_results
            )
        )

        if mentioned:

            mentioned_lines = []

            for item in mentioned:

                mentioned_lines.append(
                    f"- "
                    f"{item['citation']} "
                    f"is mentioned inside "
                    f"{item['source_case_id']}"
                )

            mentioned_text = (
                "\n".join(
                    mentioned_lines
                )
            )

        else:

            mentioned_text = (
                "No separately identified "
                "internal case citations."
            )

        return f"""
You are an authority-aware legal research assistant
for Indian Supreme Court case law.

Answer the user's question using ONLY the retrieved
evidence supplied in the context.

==================================================
USER QUESTION
==================================================

{query}

==================================================
DIRECTLY RETRIEVED CASES
==================================================

The following cases were ACTUALLY retrieved by the
RAG system:

{direct_cases}

==================================================
IMPORTANT DISTINCTION
==================================================

A case can appear in the supplied evidence in two
different ways:

A. DIRECTLY RETRIEVED CASE
   Its CASE ID appears in the "DIRECTLY RETRIEVED CASES"
   section above.

B. INTERNALLY MENTIONED AUTHORITY
   A different case may be mentioned or cited inside
   the text of a directly retrieved case.

An internally mentioned authority is NOT automatically
a directly retrieved case.

For example, if the text of 2023 INSC 1043 mentions
"(2008) 12 SCC 661", that does NOT mean that the
2008 case was independently retrieved.

Potential internally mentioned citations include:

{mentioned_text}

==================================================
MANDATORY EVIDENCE CHECK BEFORE ANSWERING
==================================================

Before writing the final answer, inspect the CASE TEXT
for EVERY directly retrieved source listed above.

For each source, determine whether its actual CASE TEXT
contains a substantive discussion, explanation, application,
or statement of the legal issue asked about.

If a directly retrieved case's CASE TEXT explicitly states
or explains the requested legal principle, that case MUST be
classified as a directly retrieved relevant case.

Do NOT conclude that "none of the directly retrieved cases"
discuss an issue unless you have checked the actual CASE TEXT
of every directly retrieved source and none contains such a
discussion.

Do NOT use ranking score, retrieval order, case title, or the
existence of an internally cited older authority as a reason
to exclude a directly retrieved case whose CASE TEXT contains
the requested legal issue.

When the CASE TEXT contains the answer, prefer that direct
evidence over any inference about what the case is "mainly"
about.

==================================================
STRICT RULES
==================================================

1. Use ONLY the supplied retrieved evidence.

2. Do not use outside legal knowledge to fill gaps.

3. Do not invent cases, citations, facts, dates,
   holdings, or legal principles.

4. Consider ALL directly retrieved sources.

5. If the question asks "which Supreme Court cases in
   the retrieved evidence discuss or apply" a principle,
   first identify the DIRECTLY RETRIEVED cases whose
   actual CASE TEXT contains substantive discussion
   of that principle.

6. Do NOT omit a directly retrieved case merely because
   another retrieved case has a higher ranking score.

7. If two or more directly retrieved cases contain
   substantive discussion of the requested legal issue,
   identify all of them when the evidence supports it.

8. If a case is only mentioned inside another retrieved
   judgment, describe it as an authority/case mentioned
   or cited in that judgment. Do NOT describe it as a
   directly retrieved case.

9. Do not claim that an internally mentioned authority
   was independently retrieved.

10. A graph relationship saying Case A cites Case B
    establishes a citation relationship only.

11. Do not turn "cites" into:
    - follows
    - approves
    - overrules
    - distinguishes
    - affirms
    unless the supplied text explicitly supports that
    stronger relationship.

12. If the question concerns Order VII Rule 11 CPC,
    prioritize retrieved passages containing:
    - Order VII Rule 11
    - Order 7 Rule 11
    - rejection of plaint
    - rejection of the plaint
    - cause of action
    - plaint
    - CPC
    - Code of Civil Procedure.

13. If a directly retrieved case has a strong legal-issue
    match, it should normally be mentioned in the answer.

14. When identifying directly retrieved cases, use their
    CASE IDs exactly as supplied.

15. If an earlier authority is only mentioned inside a
    retrieved case, it may be discussed as an internally
    cited authority, but it must be clearly labeled as such.

16. Do not claim that temporal status "unknown" means
    the case is good law.

17. If the evidence is genuinely insufficient, say so.

18. If the evidence directly answers the question, do not
    incorrectly claim that it is insufficient.

19. If the user's question asks for a legal principle and
    multiple retrieved CASE TEXT sections explicitly discuss
    that principle, report those retrieved cases rather than
    saying that no retrieved case discusses it.

20. Do not make a negative statement such as "none of the
    directly retrieved cases" unless the supplied CASE TEXT
    supports that negative conclusion after checking all
    directly retrieved sources.

21. Keep the answer concise but complete.

22. Never return an empty answer.

==================================================
CONFLICT INFORMATION
==================================================

{conflict_text}

==================================================
ANSWER FORMAT
==================================================

For questions asking which retrieved cases discuss a
legal principle, prefer this structure:

1. Legal principle
   - State the principle supported by the retrieved text.

2. Directly retrieved cases
   - List every directly retrieved case whose text
     substantively discusses/applies the principle.
   - Include the case ID.

3. Internally mentioned authorities
   - Only mention these separately if useful.
   - Clearly say they were mentioned/cited inside a
     retrieved case and were not independently retrieved.

Do not call an internally mentioned authority a
"retrieved case."

Now answer the user's question strictly from the
retrieved evidence.
""".strip()

    # =========================================================
    # CITATION VERIFICATION SOURCES
    # =========================================================

    def _build_citation_verification_sources(
        self,
        retrieved_cases,
    ):

        verification_sources = []

        for case in retrieved_cases:

            verification_sources.append(
                {
                    "case_id": case.get(
                        "case_id"
                    ),
                    "title": case.get(
                        "title"
                    ),
                    "citation": case.get(
                        "citation"
                    ),
                    "decision_date": case.get(
                        "decision_date"
                    ),
                }
            )

        return verification_sources

    # =========================================================
    # EMPTY CITATION REPORT
    # =========================================================

    def _empty_citation_report(
        self,
        reason,
    ):

        return {
            "verified": False,

            "mentioned_case_ids": [],
            "verified_case_ids": [],
            "unverified_case_ids": [],

            "mentioned_scc_citations": [],
            "verified_scc_citations": [],
            "unverified_scc_citations": [],

            "mentioned_scr_citations": [],
            "verified_scr_citations": [],
            "unverified_scr_citations": [],

            "mentioned_air_citations": [],
            "verified_air_citations": [],
            "unverified_air_citations": [],

            "total_citations": 0,

            "answer_generated": False,

            "verification_reason": reason,
        }

    # =========================================================
    # MAIN PIPELINE
    # =========================================================

    def run(
        self,
        query,
        top_k=10,
        retrieval_k=20,
        reference_date=None,
    ):

        if not query or not query.strip():

            raise ValueError(
                "Query cannot be empty."
            )

        query = query.strip()

        # -----------------------------------------
        # Reference date
        # -----------------------------------------

        if reference_date is None:

            reference_date = date.today()

        else:

            reference_date = (
                self.temporal_validator._parse_date(
                    reference_date
                )
            )

            if reference_date is None:

                raise ValueError(
                    "Invalid reference_date."
                )

        print(
            "\n========================================"
        )

        print(
            "RAG PIPELINE"
        )

        print(
            "========================================"
        )

        # =========================================
        # 1. HYBRID RETRIEVAL
        # =========================================

        print(
            "\n1. Running hybrid retrieval..."
        )

        hybrid_results = (
            self.hybrid_retriever.query(
                query=query,
                top_k=top_k,
                retrieval_k=retrieval_k,
            )
        )

        print(
            f"Hybrid candidates: "
            f"{len(hybrid_results)}"
        )

        if not hybrid_results:

            return {
                "query": query,

                "answer": (
                    "No relevant cases were retrieved."
                ),

                "sources": [],

                "relevant_sources": [],

                "context": "",

                "citation_verification": (
                    self._empty_citation_report(
                        "No cases were retrieved."
                    )
                ),

                "conflict_report": {
                    "conflict_detected": False,
                    "conflicts": [],
                    "conflict_count": 0,
                },

                "reference_date": (
                    reference_date.isoformat()
                ),
            }

        # =========================================
        # 2. CROSS ENCODER
        # =========================================

        print(
            "\n2. Running cross-encoder reranking..."
        )

        reranked_results = (
            self.cross_encoder.rerank(
                query=query,
                results=hybrid_results,
                top_k=top_k,
            )
        )

        print(
            f"Cross-encoder candidates: "
            f"{len(reranked_results)}"
        )

        # =========================================
        # 3. AUTHORITY RANKING
        # =========================================

        print(
            "\n3. Applying authority ranking..."
        )

        ranked_results = (
            self.authority_ranker.rerank(
                results=reranked_results,
                authority_weight=0.10,
                cross_encoder_weight=0.30,
            )
        )

        # =========================================
        # 4. GRAPH EXPANSION
        # =========================================

        print(
            "\n4. Expanding verified graph "
            "citation relationships..."
        )

        graph_expanded_results = (
            self._expand_graph_relationships(
                ranked_results
            )
        )

        total_graph_citations = sum(
            len(
                result.get(
                    "graph_citations",
                    [],
                )
            )
            for result in graph_expanded_results
        )

        print(
            f"Verified graph citation "
            f"relationships found: "
            f"{total_graph_citations}"
        )

        # =========================================
        # 5. TEMPORAL VALIDATION
        # =========================================

        print(
            "\n5. Applying temporal validation..."
        )

        temporally_validated = []

        for result in (
            graph_expanded_results
        ):

            temporal_result = (
                self.temporal_validator.validate(
                    case=result,
                    reference_date=reference_date,
                )
            )

            updated = dict(
                result
            )

            updated[
                "temporal_validation"
            ] = temporal_result

            temporally_validated.append(
                updated
            )

        # =========================================
        # 6. CONFLICT DETECTION
        # =========================================

        print(
            "\n6. Detecting conflicts..."
        )

        conflict_report = (
            self.conflict_detector.detect(
                temporally_validated
            )
        )

        print(
            f"Conflicts detected: "
            f"{conflict_report['conflict_count']}"
        )

        # =========================================
        # 7. EVIDENCE FILTERING
        # =========================================

        print(
            "\n7. Filtering relevant legal evidence..."
        )

        relevant_results = (
            self._select_relevant_evidence(
                query=query,
                results=temporally_validated,
                max_sources=5,
            )
        )

        # =========================================
        # 8. GROUNDED CONTEXT
        # =========================================

        print(
            "\n8. Building grounded context..."
        )

        context = self._build_context(
            relevant_results
        )

        # =========================================
        # 9. LLM GENERATION
        # =========================================

        print(
            "\n9. Generating answer with local LLM..."
        )

        prompt = self._build_prompt(
            query=query,
            conflict_report=conflict_report,
            relevant_results=relevant_results,
        )

        answer = self.llm_service.generate(
            prompt=prompt,
            context=context,
        )

        # =========================================
        # LLM DIAGNOSTIC
        # =========================================

        print(
            "\n========================================"
        )

        print(
            "LLM GENERATION DIAGNOSTIC"
        )

        print(
            "========================================"
        )

        print(
            f"Prompt length: "
            f"{len(prompt)} characters"
        )

        print(
            f"Context length: "
            f"{len(context)} characters"
        )

        print(
            f"Answer type: "
            f"{type(answer).__name__}"
        )

        print(
            f"Answer length: "
            f"{len(answer) if answer else 0} characters"
        )

        print(
            "Answer repr:"
        )

        print(
            repr(answer)
        )

        # =========================================
        # EMPTY ANSWER
        # =========================================

        if not answer or not answer.strip():

            answer = (
                "The local LLM did not return an answer. "
                "The retrieved evidence was available, "
                "but answer generation failed."
            )

            return {
                "query": query,

                "answer": answer,

                "sources": temporally_validated,

                "relevant_sources": relevant_results,

                "context": context,

                "conflict_report": conflict_report,

                "citation_verification": (
                    self._empty_citation_report(
                        "The LLM returned an empty response."
                    )
                ),

                "reference_date": (
                    reference_date.isoformat()
                ),
            }

        # =========================================
        # 10. CITATION VERIFICATION
        # =========================================

        print(
            "\n10. Verifying citations..."
        )

        citation_sources = (
            self._build_citation_verification_sources(
                temporally_validated
            )
        )

        citation_report = (
            self.citation_verifier.verify(
                answer=answer,
                retrieved_cases=citation_sources,
            )
        )

        # -----------------------------------------
        # Ensure expected fields exist
        # -----------------------------------------

        defaults = {
            "mentioned_case_ids": [],
            "verified_case_ids": [],
            "unverified_case_ids": [],

            "mentioned_scc_citations": [],
            "verified_scc_citations": [],
            "unverified_scc_citations": [],

            "mentioned_scr_citations": [],
            "verified_scr_citations": [],
            "unverified_scr_citations": [],

            "mentioned_air_citations": [],
            "verified_air_citations": [],
            "unverified_air_citations": [],
        }

        for key, default in (
            defaults.items()
        ):

            if key not in citation_report:

                citation_report[key] = (
                    list(default)
                )

        has_unverified = any(
            citation_report.get(
                key,
                [],
            )
            for key in [
                "unverified_case_ids",
                "unverified_scc_citations",
                "unverified_scr_citations",
                "unverified_air_citations",
            ]
        )

        citation_report[
            "verified"
        ] = not has_unverified

        citation_report[
            "answer_generated"
        ] = True

        citation_report[
            "verification_reason"
        ] = (
            "Generated answer citations were checked "
            "against retrieved source metadata."
        )

        citation_report[
            "total_citations"
        ] = (
            len(
                citation_report[
                    "mentioned_case_ids"
                ]
            )
            + len(
                citation_report[
                    "mentioned_scc_citations"
                ]
            )
            + len(
                citation_report[
                    "mentioned_scr_citations"
                ]
            )
            + len(
                citation_report[
                    "mentioned_air_citations"
                ]
            )
        )

        # =========================================
        # CITATION DIAGNOSTIC
        # =========================================

        print(
            "\n========================================"
        )

        print(
            "CITATION VERIFICATION DIAGNOSTIC"
        )

        print(
            "========================================"
        )

        print(
            "Mentioned case IDs:"
        )

        print(
            citation_report[
                "mentioned_case_ids"
            ]
        )

        print(
            "Verified case IDs:"
        )

        print(
            citation_report[
                "verified_case_ids"
            ]
        )

        print(
            "Unverified case IDs:"
        )

        print(
            citation_report[
                "unverified_case_ids"
            ]
        )

        print(
            "Mentioned SCC citations:"
        )

        print(
            citation_report[
                "mentioned_scc_citations"
            ]
        )

        print(
            "Verified SCC citations:"
        )

        print(
            citation_report[
                "verified_scc_citations"
            ]
        )

        print(
            "Unverified SCC citations:"
        )

        print(
            citation_report[
                "unverified_scc_citations"
            ]
        )

        print(
            "Mentioned SCR citations:"
        )

        print(
            citation_report[
                "mentioned_scr_citations"
            ]
        )

        print(
            "Verified SCR citations:"
        )

        print(
            citation_report[
                "verified_scr_citations"
            ]
        )

        print(
            "Unverified SCR citations:"
        )

        print(
            citation_report[
                "unverified_scr_citations"
            ]
        )

        print(
            f"Overall verified: "
            f"{citation_report['verified']}"
        )

        # =========================================
        # COMPLETE
        # =========================================

        print(
            "\n========================================"
        )

        print(
            "RAG PIPELINE COMPLETE"
        )

        print(
            "========================================"
        )

        return {
            "query": query,

            "answer": answer,

            "sources": temporally_validated,

            "relevant_sources": relevant_results,

            "context": context,

            "conflict_report": conflict_report,

            "citation_verification": (
                citation_report
            ),

            "reference_date": (
                reference_date.isoformat()
            ),
        }


# =========================================================
# CONVENIENCE FUNCTION
# =========================================================

def run_rag_pipeline(
    query,
    top_k=10,
    retrieval_k=20,
    reference_date=None,
):

    pipeline = RAGPipeline()

    return pipeline.run(
        query=query,
        top_k=top_k,
        retrieval_k=retrieval_k,
        reference_date=reference_date,
    )