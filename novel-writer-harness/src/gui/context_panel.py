"""
Context/reference panel component for Novel Writer Harness.
"""
import customtkinter as ctk
from typing import Callable, Optional, List
from ..models import Genre, StoryBible


class ContextPanel(ctk.CTkFrame):
    """
    Context panel for Story Bible, Research, and LLM Chat.
    """

    def __init__(
        self,
        parent,
        on_bible_section_change: Optional[Callable[[str], None]] = None,
        on_bible_edit: Optional[Callable[[], None]] = None,
        on_genre_change: Optional[Callable[[str], None]] = None,
        on_research_doc_selected: Optional[Callable[[str], None]] = None,
        on_chat_send: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        """
        Initialize the context panel.

        Args:
            parent: Parent widget
            on_bible_section_change: Callback when bible section changes
            on_bible_edit: Callback when Edit Bible is clicked
            on_genre_change: Callback when genre changes
            on_research_doc_selected: Callback when research document is selected
            on_chat_send: Callback when chat message is sent
        """
        super().__init__(parent, width=350, **kwargs)
        self.grid_propagate(False)
        
        self.on_bible_section_change = on_bible_section_change
        self.on_bible_edit = on_bible_edit
        self.on_genre_change = on_genre_change
        self.on_research_doc_selected = on_research_doc_selected
        self.on_chat_send = on_chat_send
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the context panel UI."""
        # Tab view for different context types
        self.context_tabs = ctk.CTkTabview(self)
        self.context_tabs.pack(fill="both", expand=True, padx=5, pady=5)

        # Story Bible tab
        self.bible_tab = self.context_tabs.add("Story Bible")
        self._create_bible_view()

        # Research tab
        self.research_tab = self.context_tabs.add("Research")
        self._create_research_view()

        # LLM tab
        self.llm_tab = self.context_tabs.add("LLM Chat")
        self._create_llm_chat_view()
    
    def _create_bible_view(self):
        """Create the story bible quick view."""
        # Quick access buttons
        self.bible_buttons = ctk.CTkFrame(self.bible_tab)
        self.bible_buttons.pack(fill="x", pady=5)

        ctk.CTkButton(
            self.bible_buttons,
            text="Characters",
            width=80,
            command=lambda: self._handle_bible_section("characters")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            self.bible_buttons,
            text="Settings",
            width=80,
            command=lambda: self._handle_bible_section("settings")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            self.bible_buttons,
            text="Plot",
            width=60,
            command=lambda: self._handle_bible_section("plot")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            self.bible_buttons,
            text="Edit",
            width=50,
            command=self._handle_bible_edit
        ).pack(side="right", padx=2)

        # Bible content display
        self.bible_content = ctk.CTkTextbox(self.bible_tab)
        self.bible_content.pack(fill="both", expand=True, pady=5)
    
    def _create_research_view(self):
        """Create the research browser view."""
        # Genre selector
        self.genre_frame = ctk.CTkFrame(self.research_tab)
        self.genre_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(self.genre_frame, text="Genre:").pack(side="left", padx=5)

        self.genre_selector = ctk.CTkOptionMenu(
            self.genre_frame,
            values=[g.value for g in Genre],
            command=self._handle_genre_change
        )
        self.genre_selector.pack(side="left", padx=5)

        # Document list
        self.research_list = ctk.CTkScrollableFrame(self.research_tab, height=200)
        self.research_list.pack(fill="x", pady=5)

        # Document content
        self.research_content = ctk.CTkTextbox(self.research_tab)
        self.research_content.pack(fill="both", expand=True, pady=5)
    
    def _create_llm_chat_view(self):
        """Create the LLM chat interface."""
        # Chat history
        self.chat_history = ctk.CTkTextbox(self.llm_tab, state="disabled")
        self.chat_history.pack(fill="both", expand=True, pady=5)

        # Input area
        self.chat_input_frame = ctk.CTkFrame(self.llm_tab)
        self.chat_input_frame.pack(fill="x", pady=5)

        self.chat_input = ctk.CTkEntry(
            self.chat_input_frame,
            placeholder_text="Ask the LLM for help..."
        )
        self.chat_input.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.chat_send = ctk.CTkButton(
            self.chat_input_frame,
            text="Send",
            width=60,
            command=self._handle_chat_send
        )
        self.chat_send.pack(side="right")

        # Bind Enter key
        self.chat_input.bind("<Return>", lambda e: self._handle_chat_send())
    
    def _handle_bible_section(self, section: str):
        """Handle bible section button click."""
        if self.on_bible_section_change:
            self.on_bible_section_change(section)
    
    def _handle_bible_edit(self):
        """Handle Edit Bible button click."""
        if self.on_bible_edit:
            self.on_bible_edit()
    
    def _handle_genre_change(self, genre: str):
        """Handle genre selector change."""
        if self.on_genre_change:
            self.on_genre_change(genre)
    
    def _handle_chat_send(self):
        """Handle chat send button click."""
        message = self.chat_input.get().strip()
        if message and self.on_chat_send:
            self.on_chat_send(message)
            self.chat_input.delete(0, "end")
    
    def set_bible_content(self, content: str):
        """
        Set the story bible content display.

        Args:
            content: Content to display
        """
        self.bible_content.configure(state="normal")
        self.bible_content.delete("1.0", "end")
        self.bible_content.insert("1.0", content)
        self.bible_content.configure(state="disabled")
    
    def set_research_content(self, content: str):
        """
        Set the research content display.

        Args:
            content: Content to display
        """
        self.research_content.delete("1.0", "end")
        self.research_content.insert("1.0", content)
    
    def add_research_document(self, title: str, callback: Callable[[], None]):
        """
        Add a research document button.

        Args:
            title: Document title
            callback: Function to call when clicked
        """
        doc_btn = ctk.CTkButton(
            self.research_list,
            text=title,
            anchor="w",
            command=callback
        )
        doc_btn.pack(fill="x", pady=2, padx=5)
    
    def clear_research_documents(self):
        """Clear all research document buttons."""
        for widget in self.research_list.winfo_children():
            widget.destroy()
    
    def add_chat_message(self, role: str, message: str):
        """
        Add a message to the chat history.

        Args:
            role: "User" or "Assistant"
            message: Message text
        """
        self.chat_history.configure(state="normal")
        self.chat_history.insert("end", f"{role}: {message}\n\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.see("end")
    
    def clear_chat_history(self):
        """Clear the chat history."""
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", "end")
        self.chat_history.configure(state="disabled")
    
    def select_tab(self, tab_name: str):
        """
        Select a specific tab.

        Args:
            tab_name: Name of tab ("Story Bible", "Research", or "LLM Chat")
        """
        self.context_tabs.set(tab_name)
