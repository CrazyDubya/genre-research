"""
Research Service for accessing the genre research library.

Provides structured access to genre-specific writing guidance,
templates, checklists, and examples from the research library.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import re


@dataclass
class ResearchDocument:
    """A document from the research library."""
    path: Path
    title: str
    content: str
    genre: str
    category: str  # "guide", "template", "checklist", "examples", "quickstart"

    @property
    def word_count(self) -> int:
        return len(self.content.split())

    def get_section(self, heading: str) -> Optional[str]:
        """Extract a specific section by heading."""
        pattern = rf"^##?\s*{re.escape(heading)}.*?(?=^##?\s|\Z)"
        match = re.search(pattern, self.content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        return match.group(0) if match else None

    def get_summary(self, max_chars: int = 500) -> str:
        """Get a summary of the document."""
        # Try to get the first paragraph after the title
        lines = self.content.split("\n")
        content_lines = []
        in_content = False

        for line in lines:
            if line.startswith("#"):
                if in_content:
                    break
                in_content = True
                continue
            if in_content and line.strip():
                content_lines.append(line)
                if len(" ".join(content_lines)) > max_chars:
                    break

        summary = " ".join(content_lines)[:max_chars]
        return summary + "..." if len(summary) == max_chars else summary


class ResearchService:
    """
    Service for accessing the genre research library.

    The research library contains comprehensive writing guidance for multiple genres:
    - Action
    - Choose Your Own Adventure
    - Comedy
    - Epic Fantasy / Space Opera
    - Horror
    - Interactive Fiction
    - Murder Mystery
    - Romance
    - Slice of Life
    """

    # Genre directory mapping
    GENRE_DIRS = {
        "action": "action-genre-research",
        "cyoa": "choose-your-own-adventure-research",
        "comedy": "comedy-writing-research",
        "epic-fantasy": "epic-space-opera-research",
        "space-opera": "epic-space-opera-research",
        "horror": "horror-genre-research",
        "interactive-fiction": "interactive-fiction-research",
        "murder-mystery": "murder-mystery-research",
        "romance": "romance-story-research",
        "slice-of-life": "slice-of-life-research",
    }

    # Document categories based on filename patterns
    CATEGORY_PATTERNS = {
        "quickstart": r"QUICKSTART\.md$",
        "template": r"-template\.md$|bible.*\.md$",
        "checklist": r"checklist\.md$",
        "worksheet": r"worksheet\.md$",
        "examples": r"examples?\.md$|analysis\.md$",
        "guide": r".*\.md$",  # Default
    }

    def __init__(self, research_root: Optional[Path] = None):
        """
        Initialize the research service.

        Args:
            research_root: Path to the genre-research directory.
                         If None, attempts to find it relative to this file.
        """
        if research_root is None:
            # Navigate from this file to the research root
            self.research_root = Path(__file__).parent.parent.parent.parent
        else:
            self.research_root = Path(research_root)

    def get_genre_path(self, genre: str) -> Optional[Path]:
        """Get the path to a genre's research directory."""
        genre_dir = self.GENRE_DIRS.get(genre.lower())
        if genre_dir:
            path = self.research_root / genre_dir
            return path if path.exists() else None
        return None

    def list_genres(self) -> list[str]:
        """List all available genres."""
        return list(self.GENRE_DIRS.keys())

    def list_documents(self, genre: str) -> list[ResearchDocument]:
        """List all documents for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return []

        documents = []
        for md_file in genre_path.rglob("*.md"):
            doc = self._load_document(md_file, genre)
            if doc:
                documents.append(doc)

        return sorted(documents, key=lambda d: (d.category != "quickstart", d.title))

    def _categorize_file(self, filename: str) -> str:
        """Determine the category of a file based on its name."""
        for category, pattern in self.CATEGORY_PATTERNS.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return category
        return "guide"

    def _load_document(self, path: Path, genre: str) -> Optional[ResearchDocument]:
        """Load a document from disk."""
        try:
            content = path.read_text(encoding="utf-8")

            # Extract title from first heading or filename
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            title = title_match.group(1) if title_match else path.stem.replace("-", " ").title()

            return ResearchDocument(
                path=path,
                title=title,
                content=content,
                genre=genre,
                category=self._categorize_file(path.name),
            )
        except Exception:
            return None

    def get_quickstart(self, genre: str) -> Optional[ResearchDocument]:
        """Get the quickstart guide for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return None

        quickstart_path = genre_path / "QUICKSTART.md"
        if quickstart_path.exists():
            return self._load_document(quickstart_path, genre)
        return None

    def get_readme(self, genre: str) -> Optional[ResearchDocument]:
        """Get the main README for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return None

        readme_path = genre_path / "README.md"
        if readme_path.exists():
            return self._load_document(readme_path, genre)
        return None

    def get_bible_template(self, genre: str) -> Optional[ResearchDocument]:
        """Get the story bible template for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return None

        # Look in story-framework/templates
        templates_dir = genre_path / "story-framework" / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*bible*.md"):
                return self._load_document(template_file, genre)

        return None

    def get_revision_checklist(self, genre: str) -> Optional[ResearchDocument]:
        """Get the revision checklist for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return None

        # Look in story-framework
        framework_dir = genre_path / "story-framework"
        if framework_dir.exists():
            for checklist_file in framework_dir.glob("*checklist*.md"):
                return self._load_document(checklist_file, genre)

        return None

    def get_planning_worksheet(self, genre: str) -> Optional[ResearchDocument]:
        """Get the planning worksheet for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return None

        # Look in story-framework
        framework_dir = genre_path / "story-framework"
        if framework_dir.exists():
            for worksheet_file in framework_dir.glob("*worksheet*.md"):
                return self._load_document(worksheet_file, genre)

        return None

    def get_examples(self, genre: str) -> list[ResearchDocument]:
        """Get all example analyses for a genre."""
        genre_path = self.get_genre_path(genre)
        if not genre_path:
            return []

        examples = []
        examples_dir = genre_path / "examples"
        if examples_dir.exists():
            for example_file in examples_dir.glob("*.md"):
                doc = self._load_document(example_file, genre)
                if doc:
                    examples.append(doc)

        return examples

    def search_documents(
        self,
        query: str,
        genre: Optional[str] = None,
        category: Optional[str] = None,
    ) -> list[ResearchDocument]:
        """
        Search for documents containing the query.

        Args:
            query: Search query (case-insensitive)
            genre: Limit to specific genre
            category: Limit to specific category
        """
        results = []
        query_lower = query.lower()

        genres = [genre] if genre else self.list_genres()

        for g in genres:
            for doc in self.list_documents(g):
                if category and doc.category != category:
                    continue

                if query_lower in doc.content.lower() or query_lower in doc.title.lower():
                    results.append(doc)

        return results

    def get_genre_guidance(self, genre: str, topic: str) -> Optional[str]:
        """
        Get specific guidance on a topic from genre research.

        Topics might include:
        - "pacing"
        - "character"
        - "dialogue"
        - "structure"
        - "tropes"
        - etc.
        """
        documents = self.list_documents(genre)

        for doc in documents:
            section = doc.get_section(topic)
            if section:
                return section

        # Fall back to searching content
        results = self.search_documents(topic, genre=genre)
        if results:
            return results[0].get_summary(2000)

        return None

    def get_context_for_writing(
        self,
        genre: str,
        chapter_number: int = 1,
        scene_type: str = "",
    ) -> str:
        """
        Get relevant context from research for current writing position.

        Provides different guidance based on:
        - Genre conventions
        - Position in story (beginning, middle, end)
        - Scene type (action, dialogue, description, etc.)
        """
        parts = []

        # Get genre overview
        readme = self.get_readme(genre)
        if readme:
            # Get core principles section
            principles = readme.get_section("Core Principles") or readme.get_section("Key Principles")
            if principles:
                parts.append("## Genre Principles\n" + principles[:1000])

        # Get structure guidance based on position
        if chapter_number <= 3:
            topic = "opening" if chapter_number == 1 else "setup"
        elif chapter_number <= 6:
            topic = "rising action"
        elif chapter_number <= 9:
            topic = "midpoint"
        else:
            topic = "climax"

        structure_guidance = self.get_genre_guidance(genre, topic)
        if structure_guidance:
            parts.append(f"## Structure ({topic})\n" + structure_guidance[:800])

        # Get scene-specific guidance
        if scene_type:
            scene_guidance = self.get_genre_guidance(genre, scene_type)
            if scene_guidance:
                parts.append(f"## {scene_type.title()} Guidance\n" + scene_guidance[:800])

        return "\n\n".join(parts)

    def get_character_guidance(self, genre: str, role: str = "protagonist") -> Optional[str]:
        """Get guidance on character creation for the genre."""
        return self.get_genre_guidance(genre, f"{role}") or self.get_genre_guidance(genre, "character")

    def get_dialogue_guidance(self, genre: str) -> Optional[str]:
        """Get dialogue writing guidance for the genre."""
        return self.get_genre_guidance(genre, "dialogue")

    def get_pacing_guidance(self, genre: str) -> Optional[str]:
        """Get pacing guidance for the genre."""
        return self.get_genre_guidance(genre, "pacing")

    def get_tropes(self, genre: str) -> Optional[str]:
        """Get common tropes for the genre."""
        return self.get_genre_guidance(genre, "tropes") or self.get_genre_guidance(genre, "conventions")
