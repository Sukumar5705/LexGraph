from pathlib import Path
import json
import re


CITATION_PATTERN = re.compile(
    r"\b20\d{2}\s+INSC\s+\d+\b",
    re.IGNORECASE,
)


def load_cases(path):
    cases = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            cases.append(json.loads(line))

    return cases


def extract_citation_section(text):
    upper = text.upper()

    start = upper.find("LIST OF CITATIONS")
    if start == -1:
        return ""

    end = upper.find("OTHER CASE DETAILS", start)

    if end == -1:
        end = len(text)

    return text[start:end]


def clean_entry(entry):
    entry = re.sub(r"\s+", " ", entry).strip()

    # Remove section heading from first entry
    entry = re.sub(
        r"^.*?AND OTHER REFERENCES\s+",
        "",
        entry,
        flags=re.IGNORECASE,
    )

    return entry.strip(" ,")


def extract_citations_from_case(case):
    section = extract_citation_section(
        case.get("judgment_text", "")
    )

    if not section:
        return []

    entries = re.split(
    r";|–\s*(?:relied on|referred to)\.?",
    section,
    flags=re.IGNORECASE,
)

    results = []

    for entry in entries:
        entry = clean_entry(entry)

        if " v. " not in entry.lower():
            continue

        citation_match = CITATION_PATTERN.search(entry)

        citation = (
            citation_match.group(0)
            if citation_match
            else None
        )

        # Keep the case-name/reference text.
        case_name = entry

        if citation_match:
            case_name = entry[:citation_match.start()].strip()

        # Remove common trailing reference labels
        case_name = re.sub(
            r"\s*[–-]\s*(relied on|referred to)\.?$",
            "",
            case_name,
            flags=re.IGNORECASE,
        ).strip()

        if case_name:
            results.append(
                {
                    "source_case_id": case["case_id"],
                    "source_title": case["title"],
                    "cited_case_name": case_name,
                    "cited_citation": citation,
                    "relationship": "cites",
                }
            )

    return results


def main():
    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "processed"
        / "cases_2023.jsonl"
    )

    output_dir = project_root / "data" / "graph"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = (
        output_dir
        / "citation_records_2023.jsonl"
    )

    cases = load_cases(input_path)

    all_records = []

    cases_with_citations = 0

    for case in cases:
        records = extract_citations_from_case(case)

        if records:
            cases_with_citations += 1

        all_records.extend(records)

    with output_path.open("w", encoding="utf-8") as file:
        for record in all_records:
            file.write(
                json.dumps(record, ensure_ascii=False)
                + "\n"
            )

    print("\n--- COMPLETE ---")
    print(f"Cases: {len(cases)}")
    print(
        f"Cases with extracted citations: "
        f"{cases_with_citations}"
    )
    print(f"Citation records: {len(all_records)}")
    print(f"Output: {output_path}")

    print("\n--- FIRST 10 RECORDS ---")

    for record in all_records[:10]:
        print(record)


if __name__ == "__main__":
    main()