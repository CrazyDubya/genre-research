"""
Helper utility functions.
"""
import re
from typing import Optional


def word_count(text: str) -> int:
    """
    Count words in text.

    Args:
        text: The text to count words in.

    Returns:
        Number of words.
    """
    if not text or not text.strip():
        return 0
    return len(text.split())


def character_count(text: str, include_spaces: bool = True) -> int:
    """
    Count characters in text.

    Args:
        text: The text to count characters in.
        include_spaces: Whether to include spaces in the count.

    Returns:
        Number of characters.
    """
    if not text:
        return 0
    if include_spaces:
        return len(text)
    return len(text.replace(" ", "").replace("\n", "").replace("\t", ""))


def estimate_reading_time(text: str, wpm: int = 250) -> int:
    """
    Estimate reading time in minutes.

    Args:
        text: The text to estimate reading time for.
        wpm: Words per minute reading speed.

    Returns:
        Estimated reading time in minutes.
    """
    words = word_count(text)
    return max(1, round(words / wpm))


def estimate_page_count(text: str, words_per_page: int = 250) -> int:
    """
    Estimate page count.

    Args:
        text: The text to estimate pages for.
        words_per_page: Average words per printed page.

    Returns:
        Estimated page count.
    """
    words = word_count(text)
    return max(1, round(words / words_per_page))


def slugify(text: str, max_length: int = 50) -> str:
    """
    Convert text to a URL/filename-safe slug.

    Args:
        text: The text to slugify.
        max_length: Maximum length of the slug.

    Returns:
        Slugified text.
    """
    # Convert to lowercase
    slug = text.lower()

    # Replace spaces and underscores with hyphens
    slug = re.sub(r"[\s_]+", "-", slug)

    # Remove non-alphanumeric characters (except hyphens)
    slug = re.sub(r"[^a-z0-9\-]", "", slug)

    # Remove multiple consecutive hyphens
    slug = re.sub(r"-+", "-", slug)

    # Remove leading/trailing hyphens
    slug = slug.strip("-")

    # Truncate to max length
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")

    return slug or "untitled"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: The text to truncate.
        max_length: Maximum length (including suffix).
        suffix: Suffix to add if truncated.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)].rstrip() + suffix


def extract_first_paragraph(text: str, max_chars: int = 500) -> str:
    """
    Extract the first paragraph from text.

    Args:
        text: The text to extract from.
        max_chars: Maximum characters to return.

    Returns:
        First paragraph or truncated text.
    """
    if not text:
        return ""

    # Split by double newlines (paragraph breaks)
    paragraphs = re.split(r"\n\s*\n", text.strip())

    first_para = paragraphs[0] if paragraphs else text

    return truncate_text(first_para, max_chars)


def count_sentences(text: str) -> int:
    """
    Count sentences in text.

    Args:
        text: The text to count sentences in.

    Returns:
        Number of sentences.
    """
    if not text:
        return 0

    # Simple sentence detection (end punctuation followed by space or end)
    sentences = re.split(r"[.!?]+\s*", text.strip())
    return len([s for s in sentences if s.strip()])


def calculate_readability(text: str) -> dict:
    """
    Calculate basic readability metrics.

    Args:
        text: The text to analyze.

    Returns:
        Dictionary with readability metrics.
    """
    words = word_count(text)
    sentences = count_sentences(text)
    chars = character_count(text, include_spaces=False)

    if words == 0:
        return {
            "words": 0,
            "sentences": 0,
            "avg_word_length": 0,
            "avg_sentence_length": 0,
        }

    avg_word_length = chars / words if words > 0 else 0
    avg_sentence_length = words / sentences if sentences > 0 else words

    return {
        "words": words,
        "sentences": sentences,
        "avg_word_length": round(avg_word_length, 1),
        "avg_sentence_length": round(avg_sentence_length, 1),
    }


def highlight_search(text: str, query: str, max_context: int = 50) -> list[str]:
    """
    Find and highlight search query in text.

    Args:
        text: The text to search in.
        query: The search query.
        max_context: Characters of context around each match.

    Returns:
        List of matching excerpts with context.
    """
    if not text or not query:
        return []

    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for match in pattern.finditer(text):
        start = max(0, match.start() - max_context)
        end = min(len(text), match.end() + max_context)

        excerpt = text[start:end]

        # Add ellipsis if truncated
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(text):
            excerpt = excerpt + "..."

        results.append(excerpt)

    return results


def format_word_count(count: int) -> str:
    """
    Format word count for display.

    Args:
        count: Word count.

    Returns:
        Formatted string (e.g., "1,234 words").
    """
    return f"{count:,} word{'s' if count != 1 else ''}"


def format_duration(minutes: int) -> str:
    """
    Format duration for display.

    Args:
        minutes: Duration in minutes.

    Returns:
        Formatted string (e.g., "1h 30m").
    """
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    mins = minutes % 60

    if mins == 0:
        return f"{hours}h"

    return f"{hours}h {mins}m"


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and normalizing.

    Args:
        text: The text to clean.

    Returns:
        Cleaned text.
    """
    if not text:
        return ""

    # Replace multiple spaces with single space
    text = re.sub(r" +", " ", text)

    # Replace multiple newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split("\n")]

    return "\n".join(lines).strip()


def split_into_paragraphs(text: str) -> list[str]:
    """
    Split text into paragraphs.

    Args:
        text: The text to split.

    Returns:
        List of paragraphs.
    """
    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


def merge_paragraphs(paragraphs: list[str]) -> str:
    """
    Merge paragraphs into text.

    Args:
        paragraphs: List of paragraphs.

    Returns:
        Merged text with proper paragraph breaks.
    """
    return "\n\n".join(p.strip() for p in paragraphs if p.strip())
