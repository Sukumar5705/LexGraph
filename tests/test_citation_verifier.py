from backend.core.citation_verifier import (
    CitationVerifier,
)


def main():

    print("=" * 40)
    print("CITATION VERIFIER TEST")
    print("=" * 40)

    # ==================================================
    # RETRIEVED CASES
    # ==================================================

    retrieved_cases = [
        {
            "case_id": "2023 INSC 1043",
            "title": (
                "ELDECO HOUSING AND INDUSTRIES LIMITED "
                "versus ASHOK VIDYARTHI AND OTHERS"
            ),
            "citation": "[2023] 16 S.C.R. 872",
            "text": (
                "ELDECO HOUSING AND INDUSTRIES LIMITED "
                "v. ASHOK VIDYARTHI AND OTHERS "
                "[2023] 16 S.C.R. 872. "
                "The case also referred to "
                "(2020) 7 SCC 366."
            ),
        },
        {
            "case_id": "2023 INSC 964",
            "title": (
                "KUM. GEETHA, D/O LATE KRISHNA "
                "versus NANJUNDASWAMY & ORS."
            ),
            "citation": "[2023] 14 S.C.R. 153",
            "text": (
                "KUM. GEETHA v. NANJUNDASWAMY "
                "[2023] 14 S.C.R. 153. "
                "The case relied upon "
                "(2018) 11 SCC 780."
            ),
        },
    ]

    verifier = CitationVerifier()

    # ==================================================
    # TEST 1: VERIFIED CASE IDs
    # ==================================================

    answer_1 = (
        "The relevant decision is 2023 INSC 1043. "
        "The court also considered 2023 INSC 964."
    )

    result_1 = verifier.verify(
        answer=answer_1,
        retrieved_cases=retrieved_cases,
    )

    print("\n========================================")
    print("TEST 1: VERIFIED CASE IDs")
    print("========================================")

    print("\nMentioned case IDs:")
    print(result_1["mentioned_case_ids"])

    print("\nVerified case IDs:")
    print(result_1["verified_case_ids"])

    print("\nUnverified case IDs:")
    print(result_1["unverified_case_ids"])

    print("\nOverall verified:")
    print(result_1["verified"])

    # ==================================================
    # TEST 2: UNVERIFIED CASE ID
    # ==================================================

    answer_2 = (
        "The relevant cases are 2023 INSC 1043, "
        "2023 INSC 964, and 2023 INSC 999."
    )

    result_2 = verifier.verify(
        answer=answer_2,
        retrieved_cases=retrieved_cases,
    )

    print("\n========================================")
    print("TEST 2: UNVERIFIED CASE ID")
    print("========================================")

    print("\nMentioned case IDs:")
    print(result_2["mentioned_case_ids"])

    print("\nVerified case IDs:")
    print(result_2["verified_case_ids"])

    print("\nUnverified case IDs:")
    print(result_2["unverified_case_ids"])

    print("\nOverall verified:")
    print(result_2["verified"])

    # ==================================================
    # TEST 3: VERIFIED SCC AND SCR CITATIONS
    # ==================================================

    answer_3 = (
        "The court relied on "
        "(2020) 7 SCC 366 and "
        "(2018) 11 SCC 780. "
        "The relevant Supreme Court Reports citations are "
        "[2023] 16 S.C.R. 872 and "
        "[2023] 14 S.C.R. 153."
    )

    result_3 = verifier.verify(
        answer=answer_3,
        retrieved_cases=retrieved_cases,
    )

    print("\n========================================")
    print("TEST 3: VERIFIED SCC / SCR CITATIONS")
    print("========================================")

    print("\nMentioned SCC citations:")
    print(result_3["mentioned_scc_citations"])

    print("\nVerified SCC citations:")
    print(result_3["verified_scc_citations"])

    print("\nUnverified SCC citations:")
    print(result_3["unverified_scc_citations"])

    print("\nMentioned SCR citations:")
    print(result_3["mentioned_scr_citations"])

    print("\nVerified SCR citations:")
    print(result_3["verified_scr_citations"])

    print("\nUnverified SCR citations:")
    print(result_3["unverified_scr_citations"])

    print("\nOverall verified:")
    print(result_3["verified"])

    # ==================================================
    # TEST 4: UNVERIFIED SCC / SCR CITATIONS
    # ==================================================

    answer_4 = (
        "The court relied on "
        "(2019) 99 SCC 999 and "
        "[2022] 99 S.C.R. 999."
    )

    result_4 = verifier.verify(
        answer=answer_4,
        retrieved_cases=retrieved_cases,
    )

    print("\n========================================")
    print("TEST 4: UNVERIFIED SCC / SCR CITATIONS")
    print("========================================")

    print("\nMentioned SCC citations:")
    print(result_4["mentioned_scc_citations"])

    print("\nVerified SCC citations:")
    print(result_4["verified_scc_citations"])

    print("\nUnverified SCC citations:")
    print(result_4["unverified_scc_citations"])

    print("\nMentioned SCR citations:")
    print(result_4["mentioned_scr_citations"])

    print("\nVerified SCR citations:")
    print(result_4["verified_scr_citations"])

    print("\nUnverified SCR citations:")
    print(result_4["unverified_scr_citations"])

    print("\nOverall verified:")
    print(result_4["verified"])

    # ==================================================
    # TEST 5: MIXED VERIFIED + UNVERIFIED
    # ==================================================

    answer_5 = (
        "The relevant cases are 2023 INSC 1043 "
        "and 2023 INSC 999. "
        "The court relied on "
        "(2020) 7 SCC 366 and "
        "(2019) 99 SCC 999."
    )

    result_5 = verifier.verify(
        answer=answer_5,
        retrieved_cases=retrieved_cases,
    )

    print("\n========================================")
    print("TEST 5: MIXED VERIFIED / UNVERIFIED")
    print("========================================")

    print("\nMentioned case IDs:")
    print(result_5["mentioned_case_ids"])

    print("\nVerified case IDs:")
    print(result_5["verified_case_ids"])

    print("\nUnverified case IDs:")
    print(result_5["unverified_case_ids"])

    print("\nMentioned SCC citations:")
    print(result_5["mentioned_scc_citations"])

    print("\nVerified SCC citations:")
    print(result_5["verified_scc_citations"])

    print("\nUnverified SCC citations:")
    print(result_5["unverified_scc_citations"])

    print("\nOverall verified:")
    print(result_5["verified"])

    # ==================================================
    # TEST 6: EXACT UNSUPPORTED SCC CITATION
    # ==================================================

    # This is the exact type of citation that appeared
    # in the problematic RAG answer:
    #
    # (2008) 12 SCC 661
    #
    # It is intentionally NOT present in retrieved_cases.
    # Therefore it MUST be detected as unverified.

    answer_6 = (
        "The Supreme Court applied the principle in "
        "Kamala and others v. K. T. Eshwara Sa "
        "(2008) 12 SCC 661."
    )

    result_6 = verifier.verify(
        answer=answer_6,
        retrieved_cases=retrieved_cases,
    )

    print("\n========================================")
    print("TEST 6: EXACT UNSUPPORTED SCC CITATION")
    print("========================================")

    print("\nMentioned SCC citations:")
    print(result_6["mentioned_scc_citations"])

    print("\nVerified SCC citations:")
    print(result_6["verified_scc_citations"])

    print("\nUnverified SCC citations:")
    print(result_6["unverified_scc_citations"])

    print("\nOverall verified:")
    print(result_6["verified"])

    # ==================================================
    # COMPLETE
    # ==================================================

    print("\n========================================")
    print("TEST COMPLETE")
    print("========================================")


if __name__ == "__main__":
    main()