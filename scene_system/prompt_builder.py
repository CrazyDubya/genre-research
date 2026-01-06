"""Prompt builder for LLM scene drafting."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from scene_system.models import SceneCard, StyleParameters


class PromptBuilder:
    def __init__(self, story_bible: Dict[str, str]) -> None:
        self._story_bible = story_bible

    def build_prompt(
        self,
        scene_card: SceneCard,
        style: Optional[StyleParameters] = None,
        bible_sections: Optional[Iterable[str]] = None,
    ) -> str:
        bible_sections = list(bible_sections or self._story_bible.keys())
        bible_content = self._format_story_bible(bible_sections)
        style_content = style.to_prompt_fragment() if style else "Style: default"
        return (
            "You are drafting a narrative scene. Use the following inputs.\n\n"
            "Scene Card\n"
            f"Goal: {scene_card.goal}\n"
            f"Conflict: {scene_card.conflict}\n"
            f"Outcome: {scene_card.outcome}\n"
            f"POV: {scene_card.pov}\n"
            f"Setting: {scene_card.setting}\n"
            f"Length target: {scene_card.length_target}\n\n"
            "Story Bible\n"
            f"{bible_content}\n\n"
            "Style Controls\n"
            f"{style_content}\n\n"
            "Draft the scene with clear beats, honoring the story bible details."
        )

    def _format_story_bible(self, sections: Iterable[str]) -> str:
        formatted_sections: List[str] = []
        for section in sections:
            content = self._story_bible.get(section)
            if not content:
                continue
            formatted_sections.append(f"{section}: {content}")
        if not formatted_sections:
            return "No story bible sections provided."
        return "\n".join(formatted_sections)
