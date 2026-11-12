import re


def clean_text(text: str) -> str:
    """
    Clean extracted judgment text while preserving legal content.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove common PDF extraction control characters
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", " ", text)

    # Fix words broken across lines with a hyphen
    # Example: "appel-\nlants" -> "appellants"
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)

    # Replace remaining line breaks with spaces
    # while keeping paragraph separation
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Normalize spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()