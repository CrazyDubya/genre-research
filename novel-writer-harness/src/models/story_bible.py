"""
Story Bible data models for maintaining story consistency.

The story bible tracks all canonical information about the novel:
- Characters and their relationships
- World-building and settings
- Plot threads and timeline
- Themes and motifs
- Genre-specific elements
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import json
from pathlib import Path
import uuid


class CharacterRole(Enum):
    """Character importance levels."""
    PROTAGONIST = "protagonist"
    ANTAGONIST = "antagonist"
    DEUTERAGONIST = "deuteragonist"  # Secondary protagonist
    SUPPORTING = "supporting"
    MINOR = "minor"
    MENTIONED = "mentioned"  # Referenced but doesn't appear


class RelationshipType(Enum):
    """Types of character relationships."""
    FAMILY = "family"
    ROMANTIC = "romantic"
    FRIEND = "friend"
    ENEMY = "enemy"
    RIVAL = "rival"
    MENTOR = "mentor"
    STUDENT = "student"
    COLLEAGUE = "colleague"
    ACQUAINTANCE = "acquaintance"
    COMPLICATED = "complicated"


@dataclass
class CharacterProfile:
    """
    Complete character profile for story bible.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    aliases: list[str] = field(default_factory=list)
    role: CharacterRole = CharacterRole.SUPPORTING

    # Physical description
    age: str = ""
    appearance: str = ""
    distinguishing_features: str = ""
    mannerisms: str = ""
    voice_description: str = ""

    # Background
    backstory: str = ""
    occupation: str = ""
    skills: list[str] = field(default_factory=list)
    secrets: str = ""

    # Psychology
    personality: str = ""
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    fears: list[str] = field(default_factory=list)
    desires: list[str] = field(default_factory=list)

    # Character arc
    arc_type: str = ""  # e.g., "redemption", "fall", "coming of age"
    starting_state: str = ""
    ending_state: str = ""
    key_moments: list[str] = field(default_factory=list)

    # Dialogue patterns
    speech_patterns: str = ""
    vocabulary_level: str = ""
    catchphrases: list[str] = field(default_factory=list)

    # Notes
    notes: str = ""
    first_appearance: str = ""  # Chapter/scene reference

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "aliases": self.aliases,
            "role": self.role.value,
            "age": self.age,
            "appearance": self.appearance,
            "distinguishing_features": self.distinguishing_features,
            "mannerisms": self.mannerisms,
            "voice_description": self.voice_description,
            "backstory": self.backstory,
            "occupation": self.occupation,
            "skills": self.skills,
            "secrets": self.secrets,
            "personality": self.personality,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "fears": self.fears,
            "desires": self.desires,
            "arc_type": self.arc_type,
            "starting_state": self.starting_state,
            "ending_state": self.ending_state,
            "key_moments": self.key_moments,
            "speech_patterns": self.speech_patterns,
            "vocabulary_level": self.vocabulary_level,
            "catchphrases": self.catchphrases,
            "notes": self.notes,
            "first_appearance": self.first_appearance,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CharacterProfile":
        """Deserialize from dictionary."""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            aliases=data.get("aliases", []),
            role=CharacterRole(data.get("role", "supporting")),
            age=data.get("age", ""),
            appearance=data.get("appearance", ""),
            distinguishing_features=data.get("distinguishing_features", ""),
            mannerisms=data.get("mannerisms", ""),
            voice_description=data.get("voice_description", ""),
            backstory=data.get("backstory", ""),
            occupation=data.get("occupation", ""),
            skills=data.get("skills", []),
            secrets=data.get("secrets", ""),
            personality=data.get("personality", ""),
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            fears=data.get("fears", []),
            desires=data.get("desires", []),
            arc_type=data.get("arc_type", ""),
            starting_state=data.get("starting_state", ""),
            ending_state=data.get("ending_state", ""),
            key_moments=data.get("key_moments", []),
            speech_patterns=data.get("speech_patterns", ""),
            vocabulary_level=data.get("vocabulary_level", ""),
            catchphrases=data.get("catchphrases", []),
            notes=data.get("notes", ""),
            first_appearance=data.get("first_appearance", ""),
        )

    def get_llm_summary(self) -> str:
        """Generate a concise summary for LLM context."""
        parts = [f"**{self.name}** ({self.role.value})"]
        if self.age:
            parts.append(f"Age: {self.age}")
        if self.appearance:
            parts.append(f"Appearance: {self.appearance}")
        if self.personality:
            parts.append(f"Personality: {self.personality}")
        if self.occupation:
            parts.append(f"Occupation: {self.occupation}")
        if self.speech_patterns:
            parts.append(f"Speech: {self.speech_patterns}")
        return "\n".join(parts)


@dataclass
class Relationship:
    """Relationship between two characters."""
    character1_id: str = ""
    character2_id: str = ""
    relationship_type: RelationshipType = RelationshipType.ACQUAINTANCE
    description: str = ""
    dynamic: str = ""  # How they interact
    history: str = ""  # How relationship developed
    tension_points: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "character1_id": self.character1_id,
            "character2_id": self.character2_id,
            "relationship_type": self.relationship_type.value,
            "description": self.description,
            "dynamic": self.dynamic,
            "history": self.history,
            "tension_points": self.tension_points,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Relationship":
        return cls(
            character1_id=data.get("character1_id", ""),
            character2_id=data.get("character2_id", ""),
            relationship_type=RelationshipType(data.get("relationship_type", "acquaintance")),
            description=data.get("description", ""),
            dynamic=data.get("dynamic", ""),
            history=data.get("history", ""),
            tension_points=data.get("tension_points", []),
        )


@dataclass
class Setting:
    """A location or setting in the story."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: str = ""  # e.g., "city", "building", "natural", "vehicle"

    # Description
    description: str = ""
    atmosphere: str = ""
    sensory_details: str = ""  # Sights, sounds, smells, etc.

    # Details
    history: str = ""
    significance: str = ""  # Why this place matters to the story
    secrets: str = ""

    # Connections
    parent_location: str = ""  # ID of containing location
    connected_locations: list[str] = field(default_factory=list)

    # Visual reference
    map_notes: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "atmosphere": self.atmosphere,
            "sensory_details": self.sensory_details,
            "history": self.history,
            "significance": self.significance,
            "secrets": self.secrets,
            "parent_location": self.parent_location,
            "connected_locations": self.connected_locations,
            "map_notes": self.map_notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Setting":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            type=data.get("type", ""),
            description=data.get("description", ""),
            atmosphere=data.get("atmosphere", ""),
            sensory_details=data.get("sensory_details", ""),
            history=data.get("history", ""),
            significance=data.get("significance", ""),
            secrets=data.get("secrets", ""),
            parent_location=data.get("parent_location", ""),
            connected_locations=data.get("connected_locations", []),
            map_notes=data.get("map_notes", ""),
        )


@dataclass
class PlotThread:
    """A plot thread or story arc."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    type: str = ""  # "main", "subplot", "backstory", "mystery"

    # Structure
    setup: str = ""
    rising_action: list[str] = field(default_factory=list)
    climax: str = ""
    resolution: str = ""

    # Status
    introduced_chapter: int = 0
    resolved_chapter: Optional[int] = None
    is_active: bool = True

    # Connections
    related_characters: list[str] = field(default_factory=list)
    related_settings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "setup": self.setup,
            "rising_action": self.rising_action,
            "climax": self.climax,
            "resolution": self.resolution,
            "introduced_chapter": self.introduced_chapter,
            "resolved_chapter": self.resolved_chapter,
            "is_active": self.is_active,
            "related_characters": self.related_characters,
            "related_settings": self.related_settings,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PlotThread":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            type=data.get("type", ""),
            setup=data.get("setup", ""),
            rising_action=data.get("rising_action", []),
            climax=data.get("climax", ""),
            resolution=data.get("resolution", ""),
            introduced_chapter=data.get("introduced_chapter", 0),
            resolved_chapter=data.get("resolved_chapter"),
            is_active=data.get("is_active", True),
            related_characters=data.get("related_characters", []),
            related_settings=data.get("related_settings", []),
        )


@dataclass
class TimelineEvent:
    """An event in the story timeline."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""

    # Timing
    story_time: str = ""  # When in story time
    chapter_reference: int = 0  # When it appears in narrative

    # Connections
    characters_involved: list[str] = field(default_factory=list)
    location: str = ""
    plot_threads: list[str] = field(default_factory=list)

    # Type
    event_type: str = ""  # "backstory", "present", "flashback", "foreshadowing"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "story_time": self.story_time,
            "chapter_reference": self.chapter_reference,
            "characters_involved": self.characters_involved,
            "location": self.location,
            "plot_threads": self.plot_threads,
            "event_type": self.event_type,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TimelineEvent":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            description=data.get("description", ""),
            story_time=data.get("story_time", ""),
            chapter_reference=data.get("chapter_reference", 0),
            characters_involved=data.get("characters_involved", []),
            location=data.get("location", ""),
            plot_threads=data.get("plot_threads", []),
            event_type=data.get("event_type", ""),
        )


@dataclass
class WorldRule:
    """A world-building rule or constraint."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    category: str = ""  # "magic", "technology", "society", "physics", etc.
    description: str = ""
    limitations: str = ""
    exceptions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "limitations": self.limitations,
            "exceptions": self.exceptions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorldRule":
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            name=data.get("name", ""),
            category=data.get("category", ""),
            description=data.get("description", ""),
            limitations=data.get("limitations", ""),
            exceptions=data.get("exceptions", []),
        )


@dataclass
class StoryBible:
    """
    Complete story bible containing all canonical story information.
    """
    # Core elements
    characters: list[CharacterProfile] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    settings: list[Setting] = field(default_factory=list)
    plot_threads: list[PlotThread] = field(default_factory=list)
    timeline: list[TimelineEvent] = field(default_factory=list)
    world_rules: list[WorldRule] = field(default_factory=list)

    # Thematic elements
    themes: list[str] = field(default_factory=list)
    motifs: list[str] = field(default_factory=list)
    symbols: dict[str, str] = field(default_factory=dict)  # symbol -> meaning

    # Genre-specific notes
    genre_elements: dict[str, str] = field(default_factory=dict)

    # Style guide
    tone: str = ""
    style_notes: str = ""
    dos: list[str] = field(default_factory=list)
    donts: list[str] = field(default_factory=list)

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def get_character_by_id(self, char_id: str) -> Optional[CharacterProfile]:
        """Find character by ID."""
        for char in self.characters:
            if char.id == char_id:
                return char
        return None

    def get_character_by_name(self, name: str) -> Optional[CharacterProfile]:
        """Find character by name (case-insensitive)."""
        name_lower = name.lower()
        for char in self.characters:
            if char.name.lower() == name_lower:
                return char
            if name_lower in [a.lower() for a in char.aliases]:
                return char
        return None

    def get_setting_by_id(self, setting_id: str) -> Optional[Setting]:
        """Find setting by ID."""
        for setting in self.settings:
            if setting.id == setting_id:
                return setting
        return None

    def get_active_plot_threads(self) -> list[PlotThread]:
        """Get all unresolved plot threads."""
        return [pt for pt in self.plot_threads if pt.is_active]

    def generate_llm_context(self, include_all: bool = False) -> str:
        """
        Generate a context summary for LLM consumption.

        Args:
            include_all: If True, include all details. If False, include summaries.
        """
        sections = []

        # Characters
        if self.characters:
            sections.append("## Characters\n")
            for char in self.characters:
                if include_all:
                    sections.append(char.get_llm_summary())
                else:
                    if char.role in [CharacterRole.PROTAGONIST, CharacterRole.ANTAGONIST, CharacterRole.DEUTERAGONIST]:
                        sections.append(char.get_llm_summary())
                sections.append("")

        # Active plot threads
        active_plots = self.get_active_plot_threads()
        if active_plots:
            sections.append("## Active Plot Threads\n")
            for plot in active_plots:
                sections.append(f"- **{plot.name}**: {plot.setup}")

        # Settings (major ones)
        if self.settings:
            sections.append("\n## Key Settings\n")
            for setting in self.settings[:5]:  # Top 5
                sections.append(f"- **{setting.name}**: {setting.description[:100]}...")

        # World rules
        if self.world_rules:
            sections.append("\n## World Rules\n")
            for rule in self.world_rules:
                sections.append(f"- **{rule.name}**: {rule.description}")

        # Style guide
        if self.tone or self.style_notes:
            sections.append("\n## Style Guide\n")
            if self.tone:
                sections.append(f"Tone: {self.tone}")
            if self.dos:
                sections.append(f"Do: {', '.join(self.dos)}")
            if self.donts:
                sections.append(f"Don't: {', '.join(self.donts)}")

        return "\n".join(sections)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "characters": [c.to_dict() for c in self.characters],
            "relationships": [r.to_dict() for r in self.relationships],
            "settings": [s.to_dict() for s in self.settings],
            "plot_threads": [p.to_dict() for p in self.plot_threads],
            "timeline": [t.to_dict() for t in self.timeline],
            "world_rules": [w.to_dict() for w in self.world_rules],
            "themes": self.themes,
            "motifs": self.motifs,
            "symbols": self.symbols,
            "genre_elements": self.genre_elements,
            "tone": self.tone,
            "style_notes": self.style_notes,
            "dos": self.dos,
            "donts": self.donts,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StoryBible":
        """Deserialize from dictionary."""
        return cls(
            characters=[CharacterProfile.from_dict(c) for c in data.get("characters", [])],
            relationships=[Relationship.from_dict(r) for r in data.get("relationships", [])],
            settings=[Setting.from_dict(s) for s in data.get("settings", [])],
            plot_threads=[PlotThread.from_dict(p) for p in data.get("plot_threads", [])],
            timeline=[TimelineEvent.from_dict(t) for t in data.get("timeline", [])],
            world_rules=[WorldRule.from_dict(w) for w in data.get("world_rules", [])],
            themes=data.get("themes", []),
            motifs=data.get("motifs", []),
            symbols=data.get("symbols", {}),
            genre_elements=data.get("genre_elements", {}),
            tone=data.get("tone", ""),
            style_notes=data.get("style_notes", ""),
            dos=data.get("dos", []),
            donts=data.get("donts", []),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else datetime.now(),
        )

    def save(self, project_path: Path) -> None:
        """Save story bible to disk."""
        bible_file = project_path / "story_bible.json"
        self.updated_at = datetime.now()
        with open(bible_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, project_path: Path) -> "StoryBible":
        """Load story bible from disk."""
        bible_file = project_path / "story_bible.json"
        if not bible_file.exists():
            return cls()  # Return empty bible if not found

        with open(bible_file) as f:
            data = json.load(f)

        return cls.from_dict(data)
