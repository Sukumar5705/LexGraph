from pathlib import Path
import json

import pandas as pd

from clean_text import clean_text


def build_dataset():
    # Project paths
    project_root = Path(__file__).resolve().parents[2]

    metadata_path = project_root / "data" / "metadata" / "metadata-2023.parquet"
    text_dir = project_root / "data" / "processed"
    output_path = project_root / "data" / "processed" / "cases_2023.jsonl"

    # Load metadata
    df = pd.read_parquet(metadata_path)

    processed = 0
    skipped = 0

    with output_path.open("w", encoding="utf-8") as output_file:

        for _, row in df.iterrows():

            # Metadata path, e.g. 2023_10_1001_1009
            case_path = str(row["path"])

            # Extracted text filename
            text_path = text_dir / f"{case_path}_EN.txt"

            # Skip metadata records without a matching English judgment
            if not text_path.exists():
                skipped += 1
                continue

            # Read and clean judgment text
            raw_text = text_path.read_text(encoding="utf-8")
            judgment_text = clean_text(raw_text)

            # Create structured case record
            case = {
                "case_id": row["case_id"],
                "title": row["title"],
                "petitioner": row["petitioner"],
                "respondent": row["respondent"],
                "description": row["description"],
                "judge": row["judge"],
                "author_judge": row["author_judge"],
                "citation": row["citation"],
                "cnr": row["cnr"],
                "decision_date": row["decision_date"],
                "disposal_nature": row["disposal_nature"],
                "court": row["court"],
                "available_languages": row["available_languages"],
                "nc_display": row["nc_display"],
                "year": row["year"],
                "source_path": case_path,
                "judgment_text": judgment_text,
            }

            # Write one JSON object per line
            output_file.write(
                json.dumps(case, ensure_ascii=False) + "\n"
            )

            processed += 1

    print(f"Metadata records: {len(df)}")
    print(f"Cases processed: {processed}")
    print(f"Cases skipped: {skipped}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    build_dataset()