"""
Chapter and scene data models.
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import json
import uuid
from pathlib import Path


class ChapterStatus(Enum):
    """Chapter completion status."""
    OUTLINE = "outline"
    DRAFT = "draft"
    REVISION_1 = "revision_1"
    REVISION_2 = "revision_2"
    POLISHED = "polished"
    FINAL = "final"


class POVType(Enum):
    """Point of view types."""
    FIRST_PERSON = "first_person"
    SECOND_PERSON = "second_person"
    THIRD_LIMITED = "third_limited"
    THIRD_OMNISCIENT = "third_omniscient"
    MULTIPLE = "multiple"


@dataclass
class Scene:
    """
    A scene within a chapter.

    Scenes are the atomic units of narrative action.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    summary: str = ""

    # Scene metadata
    pov_character: str = ""
    location: str = ""
    time_in_story: str = ""

    # Scene purpose (for planning)
    goal: str = ""  # What character wants
    conflict: str = ""  # What opposes them
    disaster_or_resolution: str = ""  # Scene outcome

    # Writing metadata
    word_count: int = 0
    status: ChapterStatus = ChapterStatus.OUTLINE
    notes: str = ""

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_word_count(self) -> int:
        """Calculate and update word count from content."""
        self.word_count = len(self.content.split()) if self.content else 0
        return self.word_count

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "pov_character": self.pov_character,
            "location": self.location,
            "time_in_story": self.time_in_story,
            "goal": self.goal,
            "conflict": self.conflict,
            "disaster_or_resolution": self.disaster_or_resolution,
            "word_count": self.word_count,
            "status": self.status.value,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Scene":
        """Deserialize from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            content=data.get("content", ""),
            summary=data.get("summary", ""),
            pov_character=data.get("pov_character", ""),
            location=data.get("location", ""),
            time_in_story=data.get("time_in_story", ""),
            goal=data.get("goal", ""),
            conflict=data.get("conflict", ""),
            disaster_or_resolution=data.get("disaster_or_resolution", ""),
            word_count=data.get("word_count", 0),
            status=ChapterStatus(data.get("status", "outline")),
            notes=data.get("notes", ""),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
        )


@dataclass
class Chapter:
    """
    A chapter containing one or more scenes.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    number: int = 1
    title: str = ""
    epigraph: str = ""  # Optional chapter opening quote/poem

    # Chapter content
    scenes: list[Scene] = field(default_factory=list)
    chapter_notes: str = ""

    # Chapter-level metadata
    pov: POVType = POVType.THIRD_LIMITED
    primary_pov_character: str = ""

    # Purpose and structure
    chapter_goal: str = ""  # What this chapter accomplishes
    opening_hook: str = ""  # How chapter begins
    closing_hook: str = ""  # How chapter ends (pull to next)

    # Status tracking
    status: ChapterStatus = ChapterStatus.OUTLINE

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @property
    def word_count(self) -> int:
        """Total word count of all scenes."""
        return sum(scene.word_count for scene in self.scenes)

    @property
    def scene_count(self) -> int:
        """Number of scenes in chapter."""
        return len(self.scenes)

    @property
    def full_content(self) -> str:
        """Concatenate all scene content."""
        return "\n\n---\n\n".join(
            scene.content for scene in self.scenes if scene.content
        )

    def add_scene(self, scene: Optional[Scene] = None) -> Scene:
        """Add a new scene to the chapter."""
        if scene is None:
            scene = Scene(title=f"Scene {len(self.scenes) + 1}")
        self.scenes.append(scene)
        self.updated_at = datetime.now()
        return scene

    def remove_scene(self, scene_id: str) -> bool:
        """Remove a scene by ID."""
        for i, scene in enumerate(self.scenes):
            if scene.id == scene_id:
                self.scenes.pop(i)
                self.updated_at = datetime.now()
                return True
        return False

    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """Get a scene by ID."""
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        return None

    def update_all_word_counts(self) -> int:
        """Update word counts for all scenes and return total."""
        for scene in self.scenes:
            scene.update_word_count()
        return self.word_count

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "epigraph": self.epigraph,
            "scenes": [scene.to_dict() for scene in self.scenes],
            "chapter_notes": self.chapter_notes,
            "pov": self.pov.value,
            "primary_pov_character": self.primary_pov_character,
            "chapter_goal": self.chapter_goal,
            "opening_hook": self.opening_hook,
            "closing_hook": self.closing_hook,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Chapter":
        """Deserialize from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            number=data.get("number", 1),
            title=data.get("title", ""),
            epigraph=data.get("epigraph", ""),
            scenes=[Scene.from_dict(s) for s in data.get("scenes", [])],
            chapter_notes=data.get("chapter_notes", ""),
            pov=POVType(data.get("pov", "third_limited")),
            primary_pov_character=data.get("primary_pov_character", ""),
            chapter_goal=data.get("chapter_goal", ""),
            opening_hook=data.get("opening_hook", ""),
            closing_hook=data.get("closing_hook", ""),
            status=ChapterStatus(data.get("status", "outline")),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
        )

    def save(self, project_path: Path) -> None:
        """Save chapter to disk."""
        chapters_dir = project_path / "chapters"
        chapters_dir.mkdir(parents=True, exist_ok=True)

        chapter_file = chapters_dir / f"chapter_{self.number:03d}.json"
        with open(chapter_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, project_path: Path, chapter_number: int) -> "Chapter":
        """Load chapter from disk."""
        chapter_file = project_path / "chapters" / f"chapter_{chapter_number:03d}.json"
        if not chapter_file.exists():
            raise FileNotFoundError(f"Chapter not found: {chapter_file}")

        with open(chapter_file) as f:
            data = json.load(f)

        return cls.from_dict(data)


@dataclass
class ChapterOutline:
    """
    Lightweight chapter outline for planning view.
    """
    number: int
    title: str
    summary: str = ""
    scene_count: int = 0
    target_word_count: int = 3000
    actual_word_count: int = 0
    status: ChapterStatus = ChapterStatus.OUTLINE
    key_events: list[str] = field(default_factory=list)
    characters_present: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "number": self.number,
            "title": self.title,
            "summary": self.summary,
            "scene_count": self.scene_count,
            "target_word_count": self.target_word_count,
            "actual_word_count": self.actual_word_count,
            "status": self.status.value,
            "key_events": self.key_events,
            "characters_present": self.characters_present,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ChapterOutline":
        """Deserialize from dictionary."""
        return cls(
            number=data.get("number", 1),
            title=data.get("title", ""),
            summary=data.get("summary", ""),
            scene_count=data.get("scene_count", 0),
            target_word_count=data.get("target_word_count", 3000),
            actual_word_count=data.get("actual_word_count", 0),
            status=ChapterStatus(data.get("status", "outline")),
            key_events=data.get("key_events", []),
            characters_present=data.get("characters_present", []),
        )

    @classmethod
    def from_chapter(cls, chapter: Chapter) -> "ChapterOutline":
        """Create outline from full chapter."""
        return cls(
            number=chapter.number,
            title=chapter.title,
            scene_count=chapter.scene_count,
            actual_word_count=chapter.word_count,
            status=chapter.status,
        )
