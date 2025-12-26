"""Revision history utilities for scene drafts."""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from difflib import unified_diff
from typing import Iterable, List, Optional

from scene_system.models import SceneDraft, SceneRevision


def generate_unified_diff(old_text: str, new_text: str) -> str:
    diff_lines = unified_diff(
        old_text.splitlines(),
        new_text.splitlines(),
        fromfile="previous",
        tofile="current",
        lineterm="",
    )
    return "\n".join(diff_lines)


class RevisionHistory:
    def __init__(self, draft: SceneDraft) -> None:
        self._draft = draft

    @property
    def draft(self) -> SceneDraft:
        return self._draft

    def add_revision(self, new_text: str, note: Optional[str] = None) -> SceneRevision:
        if not self._draft.can_edit():
            raise ValueError("Scene is locked and cannot be revised.")

        diff = generate_unified_diff(self._draft.text, new_text)
        revision = SceneRevision(
            revision_id=len(self._draft.revisions) + 1,
            created_at=datetime.utcnow(),
            note=note,
            text=new_text,
            diff=diff,
        )
        self._draft.revisions.append(revision)
        self._draft.text = new_text
        return revision

    def list_revisions(self) -> List[SceneRevision]:
        return list(self._draft.revisions)

    def get_revision(self, revision_id: int) -> Optional[SceneRevision]:
        for revision in self._draft.revisions:
            if revision.revision_id == revision_id:
                return revision
        return None

    def restore_revision(self, revision_id: int) -> SceneDraft:
        revision = self.get_revision(revision_id)
        if revision is None:
            raise ValueError(f"Revision {revision_id} not found.")
        if not self._draft.can_edit():
            raise ValueError("Scene is locked and cannot be restored.")
        self._draft.text = revision.text
        return self._draft
