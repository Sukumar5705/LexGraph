from pathlib import Path
import json

from legal_chunker import create_chunks


def build_chunks():
    project_root = Path(__file__).resolve().parents[2]

    input_path = project_root / "data" / "processed" / "cases_2023.jsonl"
    output_path = project_root / "data" / "processed" / "chunks_2023.jsonl"

    total_cases = 0
    total_chunks = 0

    with input_path.open("r", encoding="utf-8") as input_file, \
            output_path.open("w", encoding="utf-8") as output_file:

        for line in input_file:
            case = json.loads(line)

            chunks = create_chunks(
                text=case["judgment_text"],
                case_id=case["case_id"],
            )

            for chunk in chunks:

                # Add useful case-level metadata to every chunk
                chunk["title"] = case["title"]
                chunk["citation"] = case["citation"]
                chunk["decision_date"] = case["decision_date"]
                chunk["judge"] = case["judge"]
                chunk["court"] = case["court"]
                chunk["disposal_nature"] = case["disposal_nature"]
                chunk["source_path"] = case["source_path"]

                output_file.write(
                    json.dumps(chunk, ensure_ascii=False) + "\n"
                )

                total_chunks += 1

            total_cases += 1

            if total_cases % 50 == 0:
                print(
                    f"Processed cases: {total_cases} | "
                    f"Chunks created: {total_chunks}"
                )

    print("\n--- COMPLETE ---")
    print(f"Cases processed: {total_cases}")
    print(f"Total chunks: {total_chunks}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    build_chunks()