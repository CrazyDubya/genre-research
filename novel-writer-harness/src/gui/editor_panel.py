"""
Editor panel component for Novel Writer Harness.
"""
import customtkinter as ctk
from typing import Callable, Optional
from ..models import Chapter


class EditorPanel(ctk.CTkFrame):
    """
    Main writing editor panel with chapter header and text editor.
    """

    def __init__(
        self,
        parent,
        on_text_change: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """
        Initialize the editor panel.

        Args:
            parent: Parent widget
            on_text_change: Callback for text changes
        """
        super().__init__(parent, **kwargs)
        
        self.on_text_change = on_text_change
        self.current_chapter: Optional[Chapter] = None
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the editor panel UI."""
        # Chapter header
        self.chapter_header = ctk.CTkFrame(self, height=40)
        self.chapter_header.pack(fill="x", pady=(0, 5))

        self.chapter_title_entry = ctk.CTkEntry(
            self.chapter_header,
            placeholder_text="Chapter Title",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=400
        )
        self.chapter_title_entry.pack(side="left", padx=10, pady=5)

        self.chapter_status = ctk.CTkOptionMenu(
            self.chapter_header,
            values=["Outline", "Draft", "Revision 1", "Revision 2", "Polished", "Final"],
            width=120
        )
        self.chapter_status.pack(side="right", padx=10, pady=5)

        # Main text editor
        self.editor = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Courier", size=14),
            wrap="word"
        )
        self.editor.pack(fill="both", expand=True)

        # Bind text changes
        self.editor.bind("<KeyRelease>", self._on_text_changed)

        # Scene notes below editor
        self.scene_notes_frame = ctk.CTkFrame(self, height=100)
        self.scene_notes_frame.pack(fill="x", pady=(5, 0))

        self.scene_notes_label = ctk.CTkLabel(
            self.scene_notes_frame,
            text="Scene Notes",
            font=ctk.CTkFont(weight="bold")
        )
        self.scene_notes_label.pack(anchor="w", padx=5)

        self.scene_notes = ctk.CTkTextbox(self.scene_notes_frame, height=60)
        self.scene_notes.pack(fill="x", padx=5, pady=5)
    
    def _on_text_changed(self, event=None):
        """Handle text change events."""
        if self.on_text_change:
            self.on_text_change()
    
    def load_chapter(self, chapter: Chapter):
        """
        Load a chapter into the editor.

        Args:
            chapter: Chapter to load
        """
        self.current_chapter = chapter
        
        # Clear and load chapter content
        self.chapter_title_entry.delete(0, "end")
        self.chapter_title_entry.insert(0, chapter.title)
        
        self.editor.delete("1.0", "end")
        if chapter.scenes:
            # Load all scene content
            for scene in chapter.scenes:
                if scene.content:
                    self.editor.insert("end", scene.content + "\n\n")
        
        # Set chapter status
        status_map = {
            "outline": "Outline",
            "draft": "Draft",
            "revision_1": "Revision 1",
            "revision_2": "Revision 2",
            "polished": "Polished",
            "final": "Final"
        }
        self.chapter_status.set(status_map.get(chapter.status.value, "Draft"))
    
    def get_content(self) -> str:
        """Get the current editor content."""
        return self.editor.get("1.0", "end-1c")
    
    def set_content(self, content: str):
        """Set the editor content."""
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", content)
    
    def get_chapter_title(self) -> str:
        """Get the current chapter title."""
        return self.chapter_title_entry.get()
    
    def get_chapter_status(self) -> str:
        """Get the current chapter status."""
        return self.chapter_status.get()
    
    def get_scene_notes(self) -> str:
        """Get the scene notes."""
        return self.scene_notes.get("1.0", "end-1c")
    
    def set_scene_notes(self, notes: str):
        """Set the scene notes."""
        self.scene_notes.delete("1.0", "end")
        self.scene_notes.insert("1.0", notes)
    
    def get_word_count(self) -> int:
        """Calculate word count in editor."""
        content = self.get_content()
        return len(content.split()) if content else 0
    
    def clear(self):
        """Clear all editor fields."""
        self.chapter_title_entry.delete(0, "end")
        self.editor.delete("1.0", "end")
        self.scene_notes.delete("1.0", "end")
        self.chapter_status.set("Draft")
        self.current_chapter = None
