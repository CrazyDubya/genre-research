"""
Data models for the Novel Writer Harness.
"""
from .project import Project, ProjectMetadata, ProjectStatus, Genre
from .chapter import Chapter, Scene, ChapterOutline, ChapterStatus, POVType
from .story_bible import (
    StoryBible,
    CharacterProfile,
    CharacterRole,
    Relationship,
    RelationshipType,
    Setting,
    PlotThread,
    TimelineEvent,
    WorldRule,
)
from .context import (
    ContextBuilder,
    ContextConfig,
    ContextMode,
    AssembledContext,
    WritingTask,
    create_writing_prompt,
)

__all__ = [
    # Project
    "Project",
    "ProjectMetadata",
    "ProjectStatus",
    "Genre",
    # Chapter
    "Chapter",
    "Scene",
    "ChapterOutline",
    "ChapterStatus",
    "POVType",
    # Story Bible
    "StoryBible",
    "CharacterProfile",
    "CharacterRole",
    "Relationship",
    "RelationshipType",
    "Setting",
    "PlotThread",
    "TimelineEvent",
    "WorldRule",
    # Context
    "ContextBuilder",
    "ContextConfig",
    "ContextMode",
    "AssembledContext",
    "WritingTask",
    "create_writing_prompt",
]
