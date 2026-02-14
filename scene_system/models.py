"""Data models for scene drafting."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(frozen=True)
class SceneCard:
    goal: str
    conflict: str
    outcome: str
    pov: str
    setting: str
    length_target: str


@dataclass(frozen=True)
class StyleParameters:
    tone: int
    pacing: int
    dialogue_ratio: int

    def to_prompt_fragment(self) -> str:
        return (
            f"Tone: {self.tone}/100\n"
            f"Pacing: {self.pacing}/100\n"
            f"Dialogue ratio: {self.dialogue_ratio}/100"
        )


@dataclass(frozen=True)
class SceneRevision:
    revision_id: int
    created_at: datetime
    note: Optional[str]
    text: str
    diff: str


@dataclass
class SceneDraft:
    scene_id: str
    scene_card: SceneCard
    text: str = ""
    revisions: List[SceneRevision] = field(default_factory=list)
    locked: bool = False

    def lock(self) -> None:
        self.locked = True

    def unlock(self) -> None:
        self.locked = False

    def can_edit(self) -> bool:
        return not self.locked
