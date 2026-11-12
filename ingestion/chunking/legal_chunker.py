from typing import List, Dict
import re


MAX_CHARS = 3000
OVERLAP_CHARS = 300


def split_into_paragraphs(text: str) -> List[str]:
    """Split judgment text into readable paragraph-like sections."""
    paragraphs = []

    # First try blank-line separation
    raw_paragraphs = re.split(r"\n\s*\n", text)

    for paragraph in raw_paragraphs:
        paragraph = " ".join(paragraph.split())

        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs


def split_long_text(text: str, max_chars: int) -> List[str]:
    """
    Split an oversized paragraph into smaller pieces.
    Prefer sentence boundaries where possible.
    """
    if len(text) <= max_chars:
        return [text]

    sentences = re.split(r"(?<=[.!?])\s+", text)

    pieces = []
    current = ""

    for sentence in sentences:
        if not sentence:
            continue

        if len(sentence) > max_chars:
            if current:
                pieces.append(current)
                current = ""

            # Hard split only when a single sentence is too long
            for start in range(0, len(sentence), max_chars):
                pieces.append(sentence[start:start + max_chars])

        elif len(current) + len(sentence) + 1 <= max_chars:
            current = f"{current} {sentence}".strip()

        else:
            if current:
                pieces.append(current)

            current = sentence

    if current:
        pieces.append(current)

    return pieces


def create_chunks(
    text: str,
    case_id: str,
    max_chars: int = MAX_CHARS,
    overlap_chars: int = OVERLAP_CHARS,
) -> List[Dict]:
    """
    Create retrieval-friendly legal chunks.

    Chunks respect paragraph/sentence boundaries where possible
    and never exceed max_chars.
    """

    paragraphs = split_into_paragraphs(text)

    # Break oversized paragraphs first
    units = []

    for paragraph in paragraphs:
        units.extend(split_long_text(paragraph, max_chars))

    chunks = []
    current = ""

    for unit in units:

        if not current:
            current = unit
            continue

        candidate = f"{current} {unit}"

        if len(candidate) <= max_chars:
            current = candidate

        else:
            chunks.append(current)

            # Add a small overlap from the previous chunk
            overlap = current[-overlap_chars:]

            # Ensure overlap itself doesn't cause the next chunk
            # to exceed max_chars.
            current = f"{overlap} {unit}".strip()

            if len(current) > max_chars:
                current = current[:max_chars]

    if current:
        chunks.append(current)

    results = []

    for index, chunk in enumerate(chunks):
        results.append(
            {
                "case_id": case_id,
                "chunk_index": index,
                "section_type": "judgment",
                "text": chunk,
            }
        )

    return results