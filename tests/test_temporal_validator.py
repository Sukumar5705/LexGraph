from backend.core.temporal_validator import (
    TemporalValidator,
)


def main():

    print("=" * 40)
    print("TEMPORAL VALIDATOR TEST")
    print("=" * 40)

    validator = TemporalValidator()

    test_cases = [

        {
            "case_id": "2023 INSC 1043",
            "decision_date": "2023-12-01",
        },

        {
            "case_id": "2025 INSC 100",
            "decision_date": "2025-05-10",
        },

        {
            "case_id": "2019 INSC 500",
            "decision_date": "2019-06-15",
            "temporal_status": "overruled",
        },

        {
            "case_id": "2020 INSC 200",
            "decision_date": "2020-03-20",
            "temporal_status": "good_law",
        },

        {
            "case_id": "2021 INSC 300",
        },
    ]

    reference_date = "2024-01-01"

    for case in test_cases:

        print("\n----------------------------------------")

        print(
            f"Case: "
            f"{case.get('case_id')}"
        )

        result = validator.validate(
            case,
            reference_date=reference_date,
        )

        print(
            f"Decision Date: "
            f"{result['decision_date']}"
        )

        print(
            f"Reference Date: "
            f"{result['reference_date']}"
        )

        print(
            f"Status: "
            f"{result['status']}"
        )

        print(
            f"Temporally Valid: "
            f"{result['temporally_valid']}"
        )

        print(
            f"Reason: "
            f"{result['reason']}"
        )


if __name__ == "__main__":
    main()