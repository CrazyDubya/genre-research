"""
Configuration management for the Novel Writer Harness.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import json
import os


@dataclass
class EditorConfig:
    """Editor appearance settings."""
    font_family: str = "Courier"
    font_size: int = 14
    line_spacing: float = 1.5
    theme: str = "dark"
    wrap_mode: str = "word"
    show_line_numbers: bool = False
    autosave_interval: int = 60  # seconds


@dataclass
class LLMSettings:
    """LLM provider settings."""
    provider: str = "anthropic"
    model: str = "claude-sonnet-4-20250514"
    temperature: float = 0.7
    max_tokens: int = 4096
    api_key_env: str = "ANTHROPIC_API_KEY"

    # Ollama-specific
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # OpenRouter-specific
    openrouter_api_key_env: str = "OPENROUTER_API_KEY"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "anthropic/claude-sonnet-4"


@dataclass
class WritingGoals:
    """Writing goal settings."""
    daily_word_count: int = 1000
    session_word_count: int = 500
    default_project_target: int = 80000
    track_time: bool = True


@dataclass
class Config:
    """Main application configuration."""
    # Paths
    projects_dir: str = "projects"
    research_dir: str = ""  # Auto-detected

    # Settings
    editor: EditorConfig = field(default_factory=EditorConfig)
    llm: LLMSettings = field(default_factory=LLMSettings)
    goals: WritingGoals = field(default_factory=WritingGoals)

    # Window state
    window_width: int = 1600
    window_height: int = 900
    window_x: Optional[int] = None
    window_y: Optional[int] = None

    # Recent projects
    recent_projects: list[str] = field(default_factory=list)
    max_recent: int = 10

    def add_recent_project(self, project_path: str) -> None:
        """Add a project to recent projects list."""
        if project_path in self.recent_projects:
            self.recent_projects.remove(project_path)
        self.recent_projects.insert(0, project_path)
        self.recent_projects = self.recent_projects[:self.max_recent]

    def to_dict(self) -> dict:
        """Serialize configuration to dictionary."""
        return {
            "projects_dir": self.projects_dir,
            "research_dir": self.research_dir,
            "editor": {
                "font_family": self.editor.font_family,
                "font_size": self.editor.font_size,
                "line_spacing": self.editor.line_spacing,
                "theme": self.editor.theme,
                "wrap_mode": self.editor.wrap_mode,
                "show_line_numbers": self.editor.show_line_numbers,
                "autosave_interval": self.editor.autosave_interval,
            },
            "llm": {
                "provider": self.llm.provider,
                "model": self.llm.model,
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens,
                "api_key_env": self.llm.api_key_env,
                "ollama_url": self.llm.ollama_url,
                "ollama_model": self.llm.ollama_model,
                "openrouter_api_key_env": self.llm.openrouter_api_key_env,
                "openrouter_base_url": self.llm.openrouter_base_url,
                "openrouter_model": self.llm.openrouter_model,
            },
            "goals": {
                "daily_word_count": self.goals.daily_word_count,
                "session_word_count": self.goals.session_word_count,
                "default_project_target": self.goals.default_project_target,
                "track_time": self.goals.track_time,
            },
            "window": {
                "width": self.window_width,
                "height": self.window_height,
                "x": self.window_x,
                "y": self.window_y,
            },
            "recent_projects": self.recent_projects,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Deserialize configuration from dictionary."""
        editor_data = data.get("editor", {})
        llm_data = data.get("llm", {})
        goals_data = data.get("goals", {})
        window_data = data.get("window", {})

        return cls(
            projects_dir=data.get("projects_dir", "projects"),
            research_dir=data.get("research_dir", ""),
            editor=EditorConfig(
                font_family=editor_data.get("font_family", "Courier"),
                font_size=editor_data.get("font_size", 14),
                line_spacing=editor_data.get("line_spacing", 1.5),
                theme=editor_data.get("theme", "dark"),
                wrap_mode=editor_data.get("wrap_mode", "word"),
                show_line_numbers=editor_data.get("show_line_numbers", False),
                autosave_interval=editor_data.get("autosave_interval", 60),
            ),
            llm=LLMSettings(
                provider=llm_data.get("provider", "anthropic"),
                model=llm_data.get("model", "claude-sonnet-4-20250514"),
                temperature=llm_data.get("temperature", 0.7),
                max_tokens=llm_data.get("max_tokens", 4096),
                api_key_env=llm_data.get("api_key_env", "ANTHROPIC_API_KEY"),
                ollama_url=llm_data.get("ollama_url", "http://localhost:11434"),
                ollama_model=llm_data.get("ollama_model", "llama3.2"),
                openrouter_api_key_env=llm_data.get("openrouter_api_key_env", "OPENROUTER_API_KEY"),
                openrouter_base_url=llm_data.get("openrouter_base_url", "https://openrouter.ai/api/v1"),
                openrouter_model=llm_data.get("openrouter_model", "anthropic/claude-sonnet-4"),
            ),
            goals=WritingGoals(
                daily_word_count=goals_data.get("daily_word_count", 1000),
                session_word_count=goals_data.get("session_word_count", 500),
                default_project_target=goals_data.get("default_project_target", 80000),
                track_time=goals_data.get("track_time", True),
            ),
            window_width=window_data.get("width", 1600),
            window_height=window_data.get("height", 900),
            window_x=window_data.get("x"),
            window_y=window_data.get("y"),
            recent_projects=data.get("recent_projects", []),
        )


def get_config_path() -> Path:
    """Get the configuration file path."""
    # Use XDG config directory on Linux, AppData on Windows, etc.
    if os.name == "nt":
        config_dir = Path(os.environ.get("APPDATA", "")) / "NovelWriterHarness"
    else:
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "novel-writer-harness"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "settings.json"


def load_config() -> Config:
    """Load configuration from disk."""
    config_path = get_config_path()

    if config_path.exists():
        try:
            with open(config_path) as f:
                data = json.load(f)
            return Config.from_dict(data)
        except Exception:
            pass

    return Config()


def save_config(config: Config) -> None:
    """Save configuration to disk."""
    config_path = get_config_path()

    with open(config_path, "w") as f:
        json.dump(config.to_dict(), f, indent=2)
