"""
temporal_validator.py

Purpose
-------
Validates the temporal relevance of retrieved cases.

This first implementation uses information that is actually
available in the current dataset:

- decision date
- reference date
- explicit temporal status, if supplied

It does NOT assume that a case is good law merely because
no overruling relationship is present.
"""

from datetime import date, datetime


class TemporalValidator:
    """
    Conservative temporal validator for retrieved cases.
    """

    VALID_STATUSES = {
        "good_law",
        "overruled",
        "distinguished",
        "unknown",
    }

    def __init__(self):
        pass

    def _parse_date(self, value):
        """
        Convert common date representations into a date object.
        """

        if value is None:
            return None

        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        if isinstance(value, str):

            value = value.strip()

            formats = [
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%d/%m/%Y",
                "%Y/%m/%d",
            ]

            for fmt in formats:

                try:
                    return datetime.strptime(
                        value,
                        fmt
                    ).date()

                except ValueError:
                    continue

        return None

    def validate(
        self,
        case,
        reference_date=None,
    ):
        """
        Validate the temporal status of one case.

        Parameters
        ----------
        case:
            Case dictionary.

        reference_date:
            Date against which temporal relevance is checked.
            Defaults to today's date.

        Returns
        -------
        dict
            Temporal validation report.
        """

        if reference_date is None:
            reference_date = date.today()

        else:
            reference_date = self._parse_date(
                reference_date
            )

            if reference_date is None:
                raise ValueError(
                    "Invalid reference_date."
                )

        decision_date = self._parse_date(
            case.get("decision_date")
        )

        explicit_status = case.get(
            "temporal_status"
        )

        if explicit_status:

            explicit_status = (
                str(explicit_status)
                .strip()
                .lower()
            )

            if explicit_status not in (
                self.VALID_STATUSES
            ):

                explicit_status = "unknown"

        else:
            explicit_status = "unknown"

        # -------------------------------------------------
        # No decision date available
        # -------------------------------------------------

        if decision_date is None:

            return {
                "case_id": case.get("case_id"),
                "decision_date": None,
                "reference_date": reference_date.isoformat(),
                "status": explicit_status,
                "temporally_valid": None,
                "reason": (
                    "Decision date is unavailable."
                ),
            }

        # -------------------------------------------------
        # Case decided after reference date
        # -------------------------------------------------

        if decision_date > reference_date:

            return {
                "case_id": case.get("case_id"),
                "decision_date": decision_date.isoformat(),
                "reference_date": reference_date.isoformat(),
                "status": explicit_status,
                "temporally_valid": False,
                "reason": (
                    "Case was decided after "
                    "the reference date."
                ),
            }

        # -------------------------------------------------
        # Explicit overruled status
        # -------------------------------------------------

        if explicit_status == "overruled":

            return {
                "case_id": case.get("case_id"),
                "decision_date": decision_date.isoformat(),
                "reference_date": reference_date.isoformat(),
                "status": "overruled",
                "temporally_valid": False,
                "reason": (
                    "Case has an explicit "
                    "overruled status."
                ),
            }

        # -------------------------------------------------
        # Explicit distinguished status
        # -------------------------------------------------

        if explicit_status == "distinguished":

            return {
                "case_id": case.get("case_id"),
                "decision_date": decision_date.isoformat(),
                "reference_date": reference_date.isoformat(),
                "status": "distinguished",
                "temporally_valid": True,
                "reason": (
                    "Case has an explicit "
                    "distinguished status."
                ),
            }

        # -------------------------------------------------
        # Explicit good-law status
        # -------------------------------------------------

        if explicit_status == "good_law":

            return {
                "case_id": case.get("case_id"),
                "decision_date": decision_date.isoformat(),
                "reference_date": reference_date.isoformat(),
                "status": "good_law",
                "temporally_valid": True,
                "reason": (
                    "Case has an explicit "
                    "good-law status."
                ),
            }

        # -------------------------------------------------
        # Date is valid, but legal status is unknown
        # -------------------------------------------------

        return {
            "case_id": case.get("case_id"),
            "decision_date": decision_date.isoformat(),
            "reference_date": reference_date.isoformat(),
            "status": "unknown",
            "temporally_valid": True,
            "reason": (
                "Case predates the reference date, "
                "but no explicit overruling or "
                "good-law status is available."
            ),
        }


def validate_temporal(
    case,
    reference_date=None,
):
    """
    Convenience function for temporal validation.
    """

    validator = TemporalValidator()

    return validator.validate(
        case=case,
        reference_date=reference_date,
    )