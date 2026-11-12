"""
conflict_detector.py

Purpose
-------
Detects explicitly identified conflicts among retrieved precedents.

The detector is intentionally conservative.

It does NOT assume that two cases conflict merely because
they discuss similar legal subjects. A conflict is reported
only when explicit conflict information is available in the
case metadata.

This avoids generating unsupported legal conclusions.
"""


class ConflictDetector:
    """
    Conservative conflict detector for retrieved cases.
    """

    def __init__(self):
        pass

    def detect(
        self,
        cases,
    ):
        """
        Detect explicitly declared conflicts.

        Parameters
        ----------
        cases:
            List of retrieved case dictionaries.

        Returns
        -------
        dict
            Conflict report.
        """

        case_ids = set()

        for case in cases:

            case_id = case.get("case_id")

            if case_id:
                case_ids.add(
                    self._normalize_case_id(
                        case_id
                    )
                )

        conflicts = []

        for case in cases:

            source_case_id = case.get(
                "case_id"
            )

            if not source_case_id:
                continue

            source_case_id = (
                self._normalize_case_id(
                    source_case_id
                )
            )

            explicit_conflicts = case.get(
                "conflicts_with",
                []
            )

            if isinstance(
                explicit_conflicts,
                str
            ):
                explicit_conflicts = [
                    explicit_conflicts
                ]

            if not isinstance(
                explicit_conflicts,
                list
            ):
                continue

            for target_case_id in (
                explicit_conflicts
            ):

                if not target_case_id:
                    continue

                target_case_id = (
                    self._normalize_case_id(
                        target_case_id
                    )
                )

                # Only report conflicts where the
                # conflicting case is actually present
                # in the retrieved set.
                if target_case_id not in case_ids:
                    continue

                conflict = {
                    "case_a": source_case_id,
                    "case_b": target_case_id,
                    "relationship": "conflict",
                }

                # Avoid duplicate A-B / B-A records.
                if not self._conflict_exists(
                    conflicts,
                    source_case_id,
                    target_case_id,
                ):
                    conflicts.append(
                        conflict
                    )

        return {
            "conflict_detected": (
                len(conflicts) > 0
            ),
            "conflicts": conflicts,
            "conflict_count": len(conflicts),
        }

    def _normalize_case_id(
        self,
        case_id,
    ):
        """
        Normalize a case ID for comparison.
        """

        return " ".join(
            str(case_id)
            .strip()
            .upper()
            .split()
        )

    def _conflict_exists(
        self,
        conflicts,
        case_a,
        case_b,
    ):
        """
        Check whether the same conflict has
        already been recorded in either direction.
        """

        for conflict in conflicts:

            existing_a = conflict["case_a"]
            existing_b = conflict["case_b"]

            if (
                existing_a == case_a
                and existing_b == case_b
            ):
                return True

            if (
                existing_a == case_b
                and existing_b == case_a
            ):
                return True

        return False


def detect_conflicts(cases):
    """
    Convenience function for conflict detection.
    """

    detector = ConflictDetector()

    return detector.detect(cases)