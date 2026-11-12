"""
citation_verifier.py

Purpose
-------
Verifies citations mentioned in a generated answer
against the retrieved source set.

Supported citation formats include:

- Indian Supreme Court INSC case IDs
- SCC citations
- SCR citations
- AIR citations

This is an anti-hallucination check for the final RAG answer.

A citation is considered verified only when the same
citation is present in the retrieved evidence.
"""

import re


# ---------------------------------------------------------
# CASE ID PATTERN
# ---------------------------------------------------------

CASE_ID_PATTERN = re.compile(
    r"\b\d{4}\s+INSC\s+\d+\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------
# SCC CITATION PATTERN
# ---------------------------------------------------------

SCC_PATTERN = re.compile(
    r"\(\s*\d{4}\s*\)\s*\d+\s*SCC\s+\d+\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------
# SCR CITATION PATTERN
# ---------------------------------------------------------

SCR_PATTERN = re.compile(
    r"\[\s*\d{4}\s*\]\s*\d+\s*S\.?\s*C\.?\s*R\.?\s+\d+\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------
# AIR CITATION PATTERN
# ---------------------------------------------------------

AIR_PATTERN = re.compile(
    r"\bAIR\s+\d{4}\s+(?:SC|SCC|[A-Za-z]{2,})\s+\d+\b",
    re.IGNORECASE,
)


class CitationVerifier:
    """
    Verifies legal citations mentioned in an answer
    against citations available in the retrieved evidence.
    """

    def __init__(self):
        pass

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def _normalize(self, value):
        """
        Normalize whitespace and case for comparison.
        """

        if not value:
            return ""

        return " ".join(
            str(value)
            .upper()
            .strip()
            .split()
        )

    # =====================================================
    # EXTRACT INSC CASE IDS
    # =====================================================

    def extract_case_ids(self, answer):
        """
        Extract INSC case IDs from the generated answer.

        Example:
            2023 INSC 1043
        """

        if not answer:
            return []

        matches = CASE_ID_PATTERN.findall(
            answer
        )

        case_ids = []

        for case_id in matches:

            normalized = self._normalize(
                case_id
            )

            if normalized not in case_ids:
                case_ids.append(
                    normalized
                )

        return case_ids

    # =====================================================
    # EXTRACT SCC CITATIONS
    # =====================================================

    def extract_scc_citations(self, answer):
        """
        Extract SCC citations.

        Example:
            (2008) 12 SCC 661
        """

        if not answer:
            return []

        matches = SCC_PATTERN.findall(
            answer
        )

        citations = []

        for citation in matches:

            normalized = self._normalize(
                citation
            )

            if normalized not in citations:
                citations.append(
                    normalized
                )

        return citations

    # =====================================================
    # EXTRACT SCR CITATIONS
    # =====================================================

    def extract_scr_citations(self, answer):
        """
        Extract SCR citations.

        Example:
            [2023] 16 SCR 872
        """

        if not answer:
            return []

        matches = SCR_PATTERN.findall(
            answer
        )

        citations = []

        for citation in matches:

            normalized = self._normalize(
                citation
            )

            if normalized not in citations:
                citations.append(
                    normalized
                )

        return citations

    # =====================================================
    # EXTRACT AIR CITATIONS
    # =====================================================

    def extract_air_citations(self, answer):
        """
        Extract AIR citations.

        Example:
            AIR 1962 SC 941
        """

        if not answer:
            return []

        matches = AIR_PATTERN.findall(
            answer
        )

        citations = []

        for citation in matches:

            normalized = self._normalize(
                citation
            )

            if normalized not in citations:
                citations.append(
                    normalized
                )

        return citations

    # =====================================================
    # EXTRACT ALL LEGAL CITATIONS
    # =====================================================

    def extract_all_citations(self, answer):
        """
        Extract all supported citation types.
        """

        return {
            "case_ids": self.extract_case_ids(
                answer
            ),
            "scc_citations": (
                self.extract_scc_citations(
                    answer
                )
            ),
            "scr_citations": (
                self.extract_scr_citations(
                    answer
                )
            ),
            "air_citations": (
                self.extract_air_citations(
                    answer
                )
            ),
        }

    # =====================================================
    # BUILD RETRIEVED CITATION SETS
    # =====================================================

    def _get_retrieved_citations(
        self,
        retrieved_cases,
    ):
        """
        Extract all citations available in
        the retrieved source set.

        Citations can come from:

        1. case_id
        2. citation metadata
        3. title/text content
        """

        retrieved_case_ids = set()

        retrieved_scc = set()
        retrieved_scr = set()
        retrieved_air = set()

        for case in retrieved_cases:

            # ---------------------------------------------
            # Case ID
            # ---------------------------------------------

            case_id = case.get(
                "case_id"
            )

            if case_id:

                retrieved_case_ids.add(
                    self._normalize(
                        case_id
                    )
                )

            # ---------------------------------------------
            # Explicit citation metadata
            # ---------------------------------------------

            citation = case.get(
                "citation"
            )

            if citation:

                citation_text = str(
                    citation
                )

                for value in SCC_PATTERN.findall(
                    citation_text
                ):

                    retrieved_scc.add(
                        self._normalize(
                            value
                        )
                    )

                for value in SCR_PATTERN.findall(
                    citation_text
                ):

                    retrieved_scr.add(
                        self._normalize(
                            value
                        )
                    )

                for value in AIR_PATTERN.findall(
                    citation_text
                ):

                    retrieved_air.add(
                        self._normalize(
                            value
                        )
                    )

            # ---------------------------------------------
            # Full retrieved text
            # ---------------------------------------------

            text = case.get(
                "text",
                ""
            )

            if text:

                text = str(text)

                # SCC
                for value in SCC_PATTERN.findall(
                    text
                ):

                    retrieved_scc.add(
                        self._normalize(
                            value
                        )
                    )

                # SCR
                for value in SCR_PATTERN.findall(
                    text
                ):

                    retrieved_scr.add(
                        self._normalize(
                            value
                        )
                    )

                # AIR
                for value in AIR_PATTERN.findall(
                    text
                ):

                    retrieved_air.add(
                        self._normalize(
                            value
                        )
                    )

        return {
            "case_ids": retrieved_case_ids,
            "scc_citations": retrieved_scc,
            "scr_citations": retrieved_scr,
            "air_citations": retrieved_air,
        }

    # =====================================================
    # VERIFY
    # =====================================================

    def verify(
        self,
        answer,
        retrieved_cases,
    ):
        """
        Verify all supported legal citations in an answer.

        A citation is verified only if it is present
        in the retrieved source evidence.
        """

        mentioned = self.extract_all_citations(
            answer
        )

        retrieved = self._get_retrieved_citations(
            retrieved_cases
        )

        # ---------------------------------------------
        # Case IDs
        # ---------------------------------------------

        verified_case_ids = []
        unverified_case_ids = []

        for case_id in mentioned[
            "case_ids"
        ]:

            if case_id in retrieved[
                "case_ids"
            ]:

                verified_case_ids.append(
                    case_id
                )

            else:

                unverified_case_ids.append(
                    case_id
                )

        # ---------------------------------------------
        # SCC
        # ---------------------------------------------

        verified_scc = []
        unverified_scc = []

        for citation in mentioned[
            "scc_citations"
        ]:

            if citation in retrieved[
                "scc_citations"
            ]:

                verified_scc.append(
                    citation
                )

            else:

                unverified_scc.append(
                    citation
                )

        # ---------------------------------------------
        # SCR
        # ---------------------------------------------

        verified_scr = []
        unverified_scr = []

        for citation in mentioned[
            "scr_citations"
        ]:

            if citation in retrieved[
                "scr_citations"
            ]:

                verified_scr.append(
                    citation
                )

            else:

                unverified_scr.append(
                    citation
                )

        # ---------------------------------------------
        # AIR
        # ---------------------------------------------

        verified_air = []
        unverified_air = []

        for citation in mentioned[
            "air_citations"
        ]:

            if citation in retrieved[
                "air_citations"
            ]:

                verified_air.append(
                    citation
                )

            else:

                unverified_air.append(
                    citation
                )

        # ---------------------------------------------
        # Combine all unverified citations
        # ---------------------------------------------

        total_unverified = (
            len(unverified_case_ids)
            + len(unverified_scc)
            + len(unverified_scr)
            + len(unverified_air)
        )

        total_citations = (
            len(mentioned["case_ids"])
            + len(mentioned["scc_citations"])
            + len(mentioned["scr_citations"])
            + len(mentioned["air_citations"])
        )

        return {
            "verified": (
                total_unverified == 0
            ),

            # -----------------------------------------
            # Existing fields - preserved for compatibility
            # -----------------------------------------

            "mentioned_case_ids": (
                mentioned["case_ids"]
            ),

            "verified_case_ids": (
                verified_case_ids
            ),

            "unverified_case_ids": (
                unverified_case_ids
            ),

            # -----------------------------------------
            # New citation fields
            # -----------------------------------------

            "mentioned_scc_citations": (
                mentioned["scc_citations"]
            ),

            "verified_scc_citations": (
                verified_scc
            ),

            "unverified_scc_citations": (
                unverified_scc
            ),

            "mentioned_scr_citations": (
                mentioned["scr_citations"]
            ),

            "verified_scr_citations": (
                verified_scr
            ),

            "unverified_scr_citations": (
                unverified_scr
            ),

            "mentioned_air_citations": (
                mentioned["air_citations"]
            ),

            "verified_air_citations": (
                verified_air
            ),

            "unverified_air_citations": (
                unverified_air
            ),

            "total_citations": (
                total_citations
            ),

            "total_unverified": (
                total_unverified
            ),
        }


# =========================================================
# CONVENIENCE FUNCTION
# =========================================================

def verify_citations(
    answer,
    retrieved_cases,
):
    """
    Convenience function for citation verification.
    """

    verifier = CitationVerifier()

    return verifier.verify(
        answer=answer,
        retrieved_cases=retrieved_cases,
    )