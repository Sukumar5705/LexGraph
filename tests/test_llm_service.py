from backend.core.llm_service import LLMService


def main():

    print("=" * 40)
    print("LOCAL LLM TEST")
    print("=" * 40)

    print("\nLoading LLM service...")

    llm = LLMService()

    # ==================================================
    # TEST 1: PROMPT ONLY
    # ==================================================

    print("\n========================================")
    print("TEST 1: PROMPT ONLY")
    print("========================================")

    answer_1 = llm.generate(
        prompt=(
            "Explain the doctrine of precedent "
            "in Indian law in three simple sentences."
        )
    )

    print("\nLLM RESPONSE:")
    print(repr(answer_1))

    print("\nResponse length:")
    print(len(answer_1))

    if answer_1 and answer_1.strip():
        print("\nTEST 1: PASS")
    else:
        print("\nTEST 1: FAIL")

    # ==================================================
    # TEST 2: PROMPT + CONTEXT
    # ==================================================

    print("\n========================================")
    print("TEST 2: PROMPT + CONTEXT")
    print("========================================")

    context = """
    Order VII Rule 11 CPC provides for rejection of a plaint
    in specified circumstances.

    The Supreme Court has held that the court should read the
    plaint meaningfully and as a whole. If the plaint does not
    disclose a cause of action, the plaint may be rejected
    under Order VII Rule 11 CPC.
    """

    answer_2 = llm.generate(
        prompt=(
            "What is the legal principle under "
            "Order VII Rule 11 CPC? "
            "Answer in three simple sentences."
        ),
        context=context,
    )

    print("\nLLM RESPONSE:")
    print(repr(answer_2))

    print("\nResponse length:")
    print(len(answer_2))

    if answer_2 and answer_2.strip():
        print("\nTEST 2: PASS")
    else:
        print("\nTEST 2: FAIL")

    # ==================================================
    # FINAL RESULT
    # ==================================================

    print("\n========================================")
    print("FINAL RESULT")
    print("========================================")

    test_1_passed = bool(
        answer_1 and answer_1.strip()
    )

    test_2_passed = bool(
        answer_2 and answer_2.strip()
    )

    print(
        f"Prompt-only test: "
        f"{'PASS' if test_1_passed else 'FAIL'}"
    )

    print(
        f"Context test: "
        f"{'PASS' if test_2_passed else 'FAIL'}"
    )

    if test_1_passed and test_2_passed:
        print("\nLLM SERVICE TEST: PASS")
    else:
        print("\nLLM SERVICE TEST: FAIL")


if __name__ == "__main__":
    main()