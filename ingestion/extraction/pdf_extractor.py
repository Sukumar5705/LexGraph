from pathlib import Path
import pymupdf


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from a single PDF judgment using PyMuPDF.
    """
    document = pymupdf.open(str(pdf_path))

    pages = []

    for page in document:
        text = page.get_text()
        if text:
            pages.append(text)

    document.close()

    return "\n".join(pages)


def extract_all_pdfs(input_dir: Path, output_dir: Path) -> None:
    """
    Extract text from all English Supreme Court judgment PDFs
    and save each result as a TXT file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*_EN.pdf"))

    print(f"Found {len(pdf_files)} English PDFs.")

    for i, pdf_path in enumerate(pdf_files, start=1):
        try:
            text = extract_text_from_pdf(pdf_path)

            output_path = output_dir / f"{pdf_path.stem}.txt"
            output_path.write_text(text, encoding="utf-8")

            print(f"[{i}/{len(pdf_files)}] Extracted: {pdf_path.name}")

        except Exception as e:
            print(f"[{i}/{len(pdf_files)}] ERROR: {pdf_path.name} -> {e}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    input_dir = project_root / "data" / "raw"
    output_dir = project_root / "data" / "processed"

    extract_all_pdfs(input_dir, output_dir)