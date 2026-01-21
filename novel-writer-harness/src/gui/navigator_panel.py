"""
Project navigator panel component for Novel Writer Harness.
"""
import customtkinter as ctk
from typing import Callable, Optional, List
from ..models import Chapter, Project


class NavigatorPanel(ctk.CTkFrame):
    """
    Project navigator panel for browsing chapters, notes, and outline.
    """

    def __init__(
        self,
        parent,
        on_chapter_selected: Optional[Callable[[Chapter], None]] = None,
        on_add_chapter: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """
        Initialize the navigator panel.

        Args:
            parent: Parent widget
            on_chapter_selected: Callback when a chapter is selected
            on_add_chapter: Callback when Add Chapter is clicked
        """
        super().__init__(parent, width=250, **kwargs)
        self.grid_propagate(False)
        
        self.on_chapter_selected = on_chapter_selected
        self.on_add_chapter = on_add_chapter
        self.chapters: List[Chapter] = []
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the navigator panel UI."""
        # Project title
        self.project_title = ctk.CTkLabel(
            self,
            text="No Project",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.project_title.pack(pady=10)

        # Tab view for chapters/notes/outline
        self.nav_tabs = ctk.CTkTabview(self)
        self.nav_tabs.pack(fill="both", expand=True, padx=5, pady=5)

        # Chapters tab
        self.chapters_tab = self.nav_tabs.add("Chapters")
        self.chapters_list = ctk.CTkScrollableFrame(self.chapters_tab)
        self.chapters_list.pack(fill="both", expand=True)

        # Add chapter button
        self.add_chapter_btn = ctk.CTkButton(
            self.chapters_tab,
            text="+ Add Chapter",
            command=self._handle_add_chapter
        )
        self.add_chapter_btn.pack(pady=5)

        # Notes tab
        self.notes_tab = self.nav_tabs.add("Notes")
        self.notes_list = ctk.CTkScrollableFrame(self.notes_tab)
        self.notes_list.pack(fill="both", expand=True)

        # Outline tab
        self.outline_tab = self.nav_tabs.add("Outline")
        self.outline_view = ctk.CTkTextbox(self.outline_tab)
        self.outline_view.pack(fill="both", expand=True)
    
    def set_project(self, project: Optional[Project]):
        """
        Set the current project.

        Args:
            project: Project to display, or None to clear
        """
        if project:
            self.project_title.configure(text=project.title)
            self.chapters = project.chapters if hasattr(project, 'chapters') else []
            self.refresh_chapters()
        else:
            self.project_title.configure(text="No Project")
            self.chapters = []
            self.refresh_chapters()
    
    def refresh_chapters(self):
        """Refresh the chapters list display."""
        # Clear existing chapters
        for widget in self.chapters_list.winfo_children():
            widget.destroy()
        
        # Add chapter buttons
        for i, chapter in enumerate(self.chapters):
            chapter_btn = ctk.CTkButton(
                self.chapters_list,
                text=f"Ch {chapter.number}: {chapter.title}",
                anchor="w",
                command=lambda c=chapter: self._handle_chapter_click(c)
            )
            chapter_btn.pack(fill="x", pady=2, padx=5)
            
            # Show word count
            word_count_label = ctk.CTkLabel(
                self.chapters_list,
                text=f"  {chapter.word_count:,} words",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            )
            word_count_label.pack(anchor="w", padx=15)
    
    def _handle_chapter_click(self, chapter: Chapter):
        """Handle chapter button click."""
        if self.on_chapter_selected:
            self.on_chapter_selected(chapter)
    
    def _handle_add_chapter(self):
        """Handle Add Chapter button click."""
        if self.on_add_chapter:
            self.on_add_chapter()
    
    def add_note(self, title: str, content: str = ""):
        """
        Add a note to the notes tab.

        Args:
            title: Note title
            content: Note content
        """
        note_frame = ctk.CTkFrame(self.notes_list)
        note_frame.pack(fill="x", pady=2, padx=5)
        
        note_label = ctk.CTkLabel(
            note_frame,
            text=title,
            font=ctk.CTkFont(weight="bold"),
            anchor="w"
        )
        note_label.pack(fill="x", padx=5, pady=2)
    
    def set_outline(self, outline_text: str):
        """
        Set the outline text.

        Args:
            outline_text: Outline content
        """
        self.outline_view.delete("1.0", "end")
        self.outline_view.insert("1.0", outline_text)
    
    def get_outline(self) -> str:
        """Get the current outline text."""
        return self.outline_view.get("1.0", "end-1c")
    
    def select_tab(self, tab_name: str):
        """
        Select a specific tab.

        Args:
            tab_name: Name of tab ("Chapters", "Notes", or "Outline")
        """
        self.nav_tabs.set(tab_name)
