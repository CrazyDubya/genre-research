"""
Toolbar component for Novel Writer Harness.
"""
import customtkinter as ctk
from typing import Callable, Optional


class Toolbar(ctk.CTkFrame):
    """
    Application toolbar with writing modes and quick actions.
    """

    def __init__(
        self,
        parent,
        on_mode_change: Optional[Callable[[str], None]] = None,
        on_llm_continue: Optional[Callable[[], None]] = None,
        on_llm_suggest: Optional[Callable[[], None]] = None,
        on_llm_rewrite: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """
        Initialize the toolbar.

        Args:
            parent: Parent widget
            on_mode_change: Callback for writing mode changes
            on_llm_continue: Callback for Continue button
            on_llm_suggest: Callback for Suggest button
            on_llm_rewrite: Callback for Rewrite button
        """
        super().__init__(parent, height=40, **kwargs)
        
        self.on_mode_change = on_mode_change
        self.on_llm_continue = on_llm_continue
        self.on_llm_suggest = on_llm_suggest
        self.on_llm_rewrite = on_llm_rewrite
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the toolbar UI."""
        # Writing mode selector
        self.mode_label = ctk.CTkLabel(self, text="Mode:")
        self.mode_label.pack(side="left", padx=5)

        self.mode_selector = ctk.CTkSegmentedButton(
            self,
            values=["Draft", "Collaborate", "Revise", "Outline"],
            command=self._on_mode_changed
        )
        self.mode_selector.set("Draft")
        self.mode_selector.pack(side="left", padx=5)

        # Separator
        ctk.CTkFrame(self, width=2, height=30).pack(side="left", padx=10)

        # LLM quick actions
        self.llm_continue = ctk.CTkButton(
            self,
            text="Continue",
            width=80,
            command=self._handle_llm_continue
        )
        self.llm_continue.pack(side="left", padx=2)

        self.llm_suggest = ctk.CTkButton(
            self,
            text="Suggest",
            width=70,
            command=self._handle_llm_suggest
        )
        self.llm_suggest.pack(side="left", padx=2)

        self.llm_rewrite = ctk.CTkButton(
            self,
            text="Rewrite",
            width=70,
            command=self._handle_llm_rewrite
        )
        self.llm_rewrite.pack(side="left", padx=2)

        # Right side - word count goal
        self.goal_frame = ctk.CTkFrame(self)
        self.goal_frame.pack(side="right", padx=5)

        self.word_count_label = ctk.CTkLabel(
            self.goal_frame,
            text="Words: 0 / 80,000"
        )
        self.word_count_label.pack(side="left", padx=5)

        self.progress_bar = ctk.CTkProgressBar(self.goal_frame, width=150)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", padx=5)
    
    def _on_mode_changed(self, mode: str):
        """Handle mode change."""
        if self.on_mode_change:
            self.on_mode_change(mode)
    
    def _handle_llm_continue(self):
        """Handle Continue button."""
        if self.on_llm_continue:
            self.on_llm_continue()
    
    def _handle_llm_suggest(self):
        """Handle Suggest button."""
        if self.on_llm_suggest:
            self.on_llm_suggest()
    
    def _handle_llm_rewrite(self):
        """Handle Rewrite button."""
        if self.on_llm_rewrite:
            self.on_llm_rewrite()
    
    def update_word_count(self, current: int, goal: int = 80000):
        """
        Update the word count display.

        Args:
            current: Current word count
            goal: Goal word count
        """
        self.word_count_label.configure(text=f"Words: {current:,} / {goal:,}")
        progress = min(current / goal, 1.0) if goal > 0 else 0
        self.progress_bar.set(progress)
    
    def get_current_mode(self) -> str:
        """Get the currently selected writing mode."""
        return self.mode_selector.get()
    
    def set_mode(self, mode: str):
        """Set the writing mode."""
        self.mode_selector.set(mode)
