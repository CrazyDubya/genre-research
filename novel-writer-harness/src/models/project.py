"""
Project data model for novel writing projects.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from pathlib import Path
import json
import uuid


class ProjectStatus(Enum):
    """Project lifecycle status."""
    PLANNING = "planning"
    DRAFTING = "drafting"
    REVISING = "revising"
    EDITING = "editing"
    COMPLETE = "complete"


class Genre(Enum):
    """Supported genres matching research library."""
    ACTION = "action"
    CHOOSE_YOUR_OWN_ADVENTURE = "cyoa"
    COMEDY = "comedy"
    EPIC_FANTASY = "epic-fantasy"
    SPACE_OPERA = "space-opera"
    HORROR = "horror"
    INTERACTIVE_FICTION = "interactive-fiction"
    MURDER_MYSTERY = "murder-mystery"
    ROMANCE = "romance"
    SLICE_OF_LIFE = "slice-of-life"


@dataclass
class ProjectMetadata:
    """Project metadata and settings."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = "Untitled Novel"
    author: str = ""
    genre: Genre = Genre.ACTION
    subgenre: str = ""
    logline: str = ""
    target_word_count: int = 80000
    status: ProjectStatus = ProjectStatus.PLANNING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # LLM settings
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.7

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre.value,
            "subgenre": self.subgenre,
            "logline": self.logline,
            "target_word_count": self.target_word_count,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "temperature": self.temperature,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ProjectMetadata":
        """Deserialize from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", "Untitled Novel"),
            author=data.get("author", ""),
            genre=Genre(data.get("genre", "action")),
            subgenre=data.get("subgenre", ""),
            logline=data.get("logline", ""),
            target_word_count=data.get("target_word_count", 80000),
            status=ProjectStatus(data.get("status", "planning")),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
            llm_provider=data.get("llm_provider", "anthropic"),
            llm_model=data.get("llm_model", "claude-sonnet-4-20250514"),
            temperature=data.get("temperature", 0.7),
        )


@dataclass
class Project:
    """
    Main project container for a novel.

    A project contains:
    - Metadata (title, genre, settings)
    - Chapters and scenes
    - Story bible (characters, settings, plot)
    - Notes and research
    - Revision history
    """
    metadata: ProjectMetadata = field(default_factory=ProjectMetadata)
    project_path: Optional[Path] = None

    # Content references (loaded separately)
    chapter_ids: list[str] = field(default_factory=list)

    # Statistics
    current_word_count: int = 0

    def __post_init__(self):
        """Initialize project path if not set."""
        if self.project_path is None and self.metadata.id:
            self.project_path = Path(f"projects/{self.metadata.id}")

    @property
    def progress_percent(self) -> float:
        """Calculate progress towards target word count."""
        if self.metadata.target_word_count == 0:
            return 0.0
        return min(100.0, (self.current_word_count / self.metadata.target_word_count) * 100)

    @property
    def genre_research_path(self) -> Path:
        """Get path to genre research directory."""
        genre_dirs = {
            Genre.ACTION: "action-genre-research",
            Genre.CHOOSE_YOUR_OWN_ADVENTURE: "choose-your-own-adventure-research",
            Genre.COMEDY: "comedy-writing-research",
            Genre.EPIC_FANTASY: "epic-space-opera-research",
            Genre.SPACE_OPERA: "epic-space-opera-research",
            Genre.HORROR: "horror-genre-research",
            Genre.INTERACTIVE_FICTION: "interactive-fiction-research",
            Genre.MURDER_MYSTERY: "murder-mystery-research",
            Genre.ROMANCE: "romance-story-research",
            Genre.SLICE_OF_LIFE: "slice-of-life-research",
        }
        return Path(genre_dirs.get(self.metadata.genre, "action-genre-research"))

    def save(self) -> None:
        """Save project metadata to disk."""
        if self.project_path is None:
            raise ValueError("Project path not set")

        self.project_path.mkdir(parents=True, exist_ok=True)

        # Save metadata
        metadata_file = self.project_path / "project.json"
        data = {
            "metadata": self.metadata.to_dict(),
            "chapter_ids": self.chapter_ids,
            "current_word_count": self.current_word_count,
        }
        with open(metadata_file, "w") as f:
            json.dump(data, f, indent=2)

        # Update timestamp
        self.metadata.updated_at = datetime.now()

    @classmethod
    def load(cls, project_path: Path) -> "Project":
        """Load project from disk."""
        metadata_file = project_path / "project.json"
        if not metadata_file.exists():
            raise FileNotFoundError(f"Project not found: {project_path}")

        with open(metadata_file) as f:
            data = json.load(f)

        return cls(
            metadata=ProjectMetadata.from_dict(data["metadata"]),
            project_path=project_path,
            chapter_ids=data.get("chapter_ids", []),
            current_word_count=data.get("current_word_count", 0),
        )

    @classmethod
    def create_new(cls, title: str, genre: Genre, author: str = "") -> "Project":
        """Create a new project with default structure."""
        metadata = ProjectMetadata(
            title=title,
            author=author,
            genre=genre,
        )
        project = cls(metadata=metadata)
        project.project_path = Path(f"projects/{metadata.id}")

        # Create directory structure
        project.project_path.mkdir(parents=True, exist_ok=True)
        (project.project_path / "chapters").mkdir(exist_ok=True)
        (project.project_path / "notes").mkdir(exist_ok=True)
        (project.project_path / "exports").mkdir(exist_ok=True)

        # Save initial state
        project.save()

        return project
