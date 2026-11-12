from backend.core.conflict_detector import ConflictDetector


def main():

    print("=" * 40)
    print("CONFLICT DETECTOR TEST")
    print("=" * 40)

    detector = ConflictDetector()

    # --------------------------------------------------
    # TEST 1: Explicit conflict exists
    # --------------------------------------------------

    print("\n========================================")
    print("TEST 1: EXPLICIT CONFLICT")
    print("========================================")

    cases = [
        {
            "case_id": "2023 INSC 100",
            "conflicts_with": [
                "2023 INSC 200"
            ],
        },
        {
            "case_id": "2023 INSC 200",
            "conflicts_with": [],
        },
        {
            "case_id": "2023 INSC 300",
            "conflicts_with": [],
        },
    ]

    result = detector.detect(cases)

    print(f"Conflict detected: {result['conflict_detected']}")
    print(f"Conflict count: {result['conflict_count']}")
    print(f"Conflicts: {result['conflicts']}")

    # --------------------------------------------------
    # TEST 2: Conflict target is NOT retrieved
    # --------------------------------------------------

    print("\n========================================")
    print("TEST 2: CONFLICTING CASE NOT RETRIEVED")
    print("========================================")

    cases = [
        {
            "case_id": "2023 INSC 100",
            "conflicts_with": [
                "2023 INSC 200"
            ],
        },
        {
            "case_id": "2023 INSC 300",
            "conflicts_with": [],
        },
    ]

    result = detector.detect(cases)

    print(f"Conflict detected: {result['conflict_detected']}")
    print(f"Conflict count: {result['conflict_count']}")
    print(f"Conflicts: {result['conflicts']}")

    # --------------------------------------------------
    # TEST 3: No conflicts
    # --------------------------------------------------

    print("\n========================================")
    print("TEST 3: NO CONFLICT")
    print("========================================")

    cases = [
        {
            "case_id": "2023 INSC 100",
            "conflicts_with": [],
        },
        {
            "case_id": "2023 INSC 200",
            "conflicts_with": [],
        },
    ]

    result = detector.detect(cases)

    print(f"Conflict detected: {result['conflict_detected']}")
    print(f"Conflict count: {result['conflict_count']}")
    print(f"Conflicts: {result['conflicts']}")

    # --------------------------------------------------
    # TEST 4: Duplicate A-B / B-A conflict
    # --------------------------------------------------

    print("\n========================================")
    print("TEST 4: DUPLICATE CONFLICT CHECK")
    print("========================================")

    cases = [
        {
            "case_id": "2023 INSC 100",
            "conflicts_with": [
                "2023 INSC 200"
            ],
        },
        {
            "case_id": "2023 INSC 200",
            "conflicts_with": [
                "2023 INSC 100"
            ],
        },
    ]

    result = detector.detect(cases)

    print(f"Conflict detected: {result['conflict_detected']}")
    print(f"Conflict count: {result['conflict_count']}")
    print(f"Conflicts: {result['conflicts']}")

    print("\n========================================")
    print("TEST COMPLETE")
    print("========================================")


if __name__ == "__main__":
    main()