"""
LLM Context Management for novel writing.

Manages what information is sent to the LLM for each interaction,
including story bible excerpts, recent chapters, and genre guidance.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pathlib import Path


class ContextMode(Enum):
    """How much context to include."""
    MINIMAL = "minimal"  # Just current scene + essential characters
    STANDARD = "standard"  # Current chapter + main story bible
    COMPREHENSIVE = "comprehensive"  # Multiple chapters + full bible
    CUSTOM = "custom"  # User-defined selection


class WritingTask(Enum):
    """Types of writing tasks for context optimization."""
    CONTINUE = "continue"  # Continue writing from current point
    SUGGEST = "suggest"  # Generate multiple options
    REWRITE = "rewrite"  # Rewrite selected text
    EXPAND = "expand"  # Expand sparse passages
    CONDENSE = "condense"  # Tighten verbose sections
    DIALOGUE = "dialogue"  # Generate character dialogue
    DESCRIBE = "describe"  # Add description/sensory details
    OUTLINE = "outline"  # Create chapter/scene outline
    BRAINSTORM = "brainstorm"  # Generate ideas
    ANALYZE = "analyze"  # Analyze text for issues
    EDIT = "edit"  # Line editing suggestions


@dataclass
class ContextConfig:
    """Configuration for context assembly."""
    mode: ContextMode = ContextMode.STANDARD

    # Token budget management
    max_tokens: int = 100000  # Max context tokens
    reserve_output_tokens: int = 4000  # Reserve for response

    # Content inclusion settings
    include_story_bible: bool = True
    include_genre_guidance: bool = True
    include_recent_chapters: int = 2  # Number of previous chapters
    include_chapter_outlines: bool = True

    # Specific inclusions (for CUSTOM mode)
    included_character_ids: list[str] = field(default_factory=list)
    included_setting_ids: list[str] = field(default_factory=list)
    included_chapter_numbers: list[int] = field(default_factory=list)
    custom_context: str = ""


@dataclass
class ContextBlock:
    """A block of context with metadata."""
    content: str
    source: str  # Where this content came from
    priority: int  # Higher = more important to include
    token_estimate: int = 0
    category: str = ""  # "bible", "chapter", "genre", "instruction", etc.

    def estimate_tokens(self) -> int:
        """Rough token estimate (4 chars per token)."""
        self.token_estimate = len(self.content) // 4
        return self.token_estimate


@dataclass
class AssembledContext:
    """
    Fully assembled context ready for LLM.
    """
    system_prompt: str = ""
    context_blocks: list[ContextBlock] = field(default_factory=list)
    user_prompt: str = ""

    # Metadata
    total_tokens_estimate: int = 0
    truncated: bool = False
    included_sources: list[str] = field(default_factory=list)

    def get_full_context(self) -> str:
        """Assemble all context blocks into single string."""
        parts = []
        for block in sorted(self.context_blocks, key=lambda b: -b.priority):
            if block.content:
                parts.append(f"## {block.source}\n{block.content}")
        return "\n\n".join(parts)

    def estimate_total_tokens(self) -> int:
        """Calculate total token estimate."""
        system_tokens = len(self.system_prompt) // 4
        context_tokens = sum(b.estimate_tokens() for b in self.context_blocks)
        user_tokens = len(self.user_prompt) // 4
        self.total_tokens_estimate = system_tokens + context_tokens + user_tokens
        return self.total_tokens_estimate


class ContextBuilder:
    """
    Builds context for LLM interactions.

    Assembles relevant information from:
    - Story bible (characters, settings, plot)
    - Recent chapter content
    - Genre research guidance
    - Current scene/chapter
    - User instructions
    """

    def __init__(self, config: Optional[ContextConfig] = None):
        self.config = config or ContextConfig()
        self.blocks: list[ContextBlock] = []

    def add_system_prompt(self, genre: str, task: WritingTask) -> str:
        """Generate system prompt based on genre and task."""
        base_prompt = """You are a skilled novelist collaborating on writing a novel.
Your role is to assist with creative writing while maintaining consistency with
the established story elements, character voices, and narrative style.

Key principles:
- Maintain character voice consistency
- Follow established world rules
- Match the tone and style of the existing content
- Advance plot threads naturally
- Create vivid, engaging prose
"""
        task_instructions = {
            WritingTask.CONTINUE: "Continue the story naturally from where it left off. Match the pacing and style.",
            WritingTask.SUGGEST: "Provide 3 distinct options for continuing the story, each with a different approach.",
            WritingTask.REWRITE: "Rewrite the selected text while preserving the core meaning but improving the prose.",
            WritingTask.EXPAND: "Expand this passage with more detail, sensory description, and emotional depth.",
            WritingTask.CONDENSE: "Tighten this passage, removing unnecessary words while keeping the essential content.",
            WritingTask.DIALOGUE: "Write natural dialogue for the characters involved, reflecting their unique voices.",
            WritingTask.DESCRIBE: "Add vivid sensory details and environmental description to enhance the scene.",
            WritingTask.OUTLINE: "Create a structured outline with scene goals, conflicts, and resolutions.",
            WritingTask.BRAINSTORM: "Generate creative ideas and possibilities for the story direction.",
            WritingTask.ANALYZE: "Analyze this text for pacing, character consistency, and areas for improvement.",
            WritingTask.EDIT: "Provide line-by-line editing suggestions for clarity, flow, and impact.",
        }

        genre_notes = f"\nGenre: {genre}. Adhere to genre conventions and reader expectations."

        return base_prompt + task_instructions.get(task, "") + genre_notes

    def add_story_bible_context(self, bible_summary: str, priority: int = 90) -> None:
        """Add story bible summary to context."""
        if bible_summary:
            self.blocks.append(ContextBlock(
                content=bible_summary,
                source="Story Bible",
                priority=priority,
                category="bible"
            ))

    def add_character_context(self, character_summaries: list[str], priority: int = 85) -> None:
        """Add character information to context."""
        if character_summaries:
            content = "\n\n".join(character_summaries)
            self.blocks.append(ContextBlock(
                content=content,
                source="Characters",
                priority=priority,
                category="bible"
            ))

    def add_chapter_content(self, chapter_content: str, chapter_num: int, priority: int = 70) -> None:
        """Add chapter content to context."""
        if chapter_content:
            self.blocks.append(ContextBlock(
                content=chapter_content,
                source=f"Chapter {chapter_num}",
                priority=priority,
                category="chapter"
            ))

    def add_current_scene(self, scene_content: str, priority: int = 100) -> None:
        """Add current scene content (highest priority)."""
        if scene_content:
            self.blocks.append(ContextBlock(
                content=scene_content,
                source="Current Scene",
                priority=priority,
                category="current"
            ))

    def add_genre_guidance(self, guidance: str, priority: int = 50) -> None:
        """Add genre-specific writing guidance."""
        if guidance:
            self.blocks.append(ContextBlock(
                content=guidance,
                source="Genre Guidance",
                priority=priority,
                category="genre"
            ))

    def add_custom_context(self, content: str, source: str, priority: int = 60) -> None:
        """Add custom context block."""
        if content:
            self.blocks.append(ContextBlock(
                content=content,
                source=source,
                priority=priority,
                category="custom"
            ))

    def add_previous_output(self, content: str, priority: int = 80) -> None:
        """Add previous writing for continuity."""
        if content:
            # Truncate if too long
            max_chars = 8000
            if len(content) > max_chars:
                content = "...\n" + content[-max_chars:]

            self.blocks.append(ContextBlock(
                content=content,
                source="Previous Content",
                priority=priority,
                category="previous"
            ))

    def build(self, user_prompt: str, genre: str, task: WritingTask) -> AssembledContext:
        """
        Build the final assembled context.

        Prioritizes blocks and truncates if necessary to fit token budget.
        """
        # Generate system prompt
        system_prompt = self.add_system_prompt(genre, task)

        # Sort blocks by priority
        sorted_blocks = sorted(self.blocks, key=lambda b: -b.priority)

        # Calculate available tokens
        system_tokens = len(system_prompt) // 4
        user_tokens = len(user_prompt) // 4
        available_tokens = self.config.max_tokens - self.config.reserve_output_tokens - system_tokens - user_tokens

        # Add blocks until we hit the limit
        included_blocks = []
        current_tokens = 0
        truncated = False

        for block in sorted_blocks:
            block.estimate_tokens()
            if current_tokens + block.token_estimate <= available_tokens:
                included_blocks.append(block)
                current_tokens += block.token_estimate
            else:
                truncated = True

        # Build result
        result = AssembledContext(
            system_prompt=system_prompt,
            context_blocks=included_blocks,
            user_prompt=user_prompt,
            truncated=truncated,
            included_sources=[b.source for b in included_blocks]
        )
        result.estimate_total_tokens()

        return result

    def clear(self) -> None:
        """Clear all context blocks."""
        self.blocks = []


def create_writing_prompt(
    task: WritingTask,
    selection: str = "",
    instructions: str = "",
    character_focus: list[str] = None,
) -> str:
    """
    Create a user prompt for a specific writing task.

    Args:
        task: The type of writing task
        selection: Selected text to work with (for rewrite, expand, etc.)
        instructions: Additional user instructions
        character_focus: Characters to focus on (for dialogue)
    """
    prompts = {
        WritingTask.CONTINUE: "Continue the story from where it left off.",
        WritingTask.SUGGEST: "Provide 3 different options for what happens next.",
        WritingTask.REWRITE: f"Rewrite the following passage:\n\n{selection}",
        WritingTask.EXPAND: f"Expand this passage with more detail:\n\n{selection}",
        WritingTask.CONDENSE: f"Condense this passage while keeping essential content:\n\n{selection}",
        WritingTask.DIALOGUE: f"Write dialogue for: {', '.join(character_focus or ['the characters'])}",
        WritingTask.DESCRIBE: f"Add sensory details and description to:\n\n{selection}",
        WritingTask.OUTLINE: "Create a detailed outline for the next chapter/scene.",
        WritingTask.BRAINSTORM: "Generate creative ideas for the story direction.",
        WritingTask.ANALYZE: f"Analyze this text for improvements:\n\n{selection}",
        WritingTask.EDIT: f"Provide editing suggestions for:\n\n{selection}",
    }

    prompt = prompts.get(task, "Help with writing.")

    if instructions:
        prompt += f"\n\nAdditional instructions: {instructions}"

    return prompt
