"""
Main application window for the Novel Writer Harness.
"""
import customtkinter as ctk
from pathlib import Path
from typing import Optional, Callable
import asyncio
import threading

from ..models import Project, Genre, Chapter, StoryBible
from ..services import LLMService, ResearchService


class MainWindow(ctk.CTk):
    """
    Main application window.

    Layout:
    ┌─────────────────────────────────────────────────────────────────┐
    │ Toolbar: Project | View | LLM | Help                            │
    ├───────────┬─────────────────────────────────┬───────────────────┤
    │           │                                  │                   │
    │  Project  │       Writing Editor             │   Context Panel   │
    │  Navigator│                                  │                   │
    │           │                                  │   - Story Bible   │
    │  - Chapters│                                 │   - Research      │
    │  - Scenes │                                  │   - LLM Chat      │
    │  - Notes  │                                  │                   │
    │           │                                  │                   │
    ├───────────┴─────────────────────────────────┴───────────────────┤
    │ Status Bar: Word Count | Progress | LLM Status                   │
    └─────────────────────────────────────────────────────────────────┘
    """

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Novel Writer Harness")
        self.geometry("1600x900")
        self.minsize(1200, 700)

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Application state
        self.current_project: Optional[Project] = None
        self.current_chapter: Optional[Chapter] = None
        self.story_bible: Optional[StoryBible] = None

        # Services
        self.llm_service = LLMService()
        self.research_service = ResearchService()

        # Async event loop for LLM calls
        self.loop = asyncio.new_event_loop()
        self.async_thread = threading.Thread(target=self._run_async_loop, daemon=True)
        self.async_thread.start()

        # Build UI
        self._create_menu()
        self._create_toolbar()
        self._create_main_layout()
        self._create_status_bar()

        # Bind shortcuts
        self._bind_shortcuts()

    def _run_async_loop(self):
        """Run async event loop in background thread."""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def run_async(self, coro):
        """Run a coroutine in the async thread."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def _create_menu(self):
        """Create the menu bar."""
        self.menu_bar = ctk.CTkFrame(self, height=30)
        self.menu_bar.pack(fill="x", padx=5, pady=5)

        # File menu button
        self.file_menu = ctk.CTkButton(
            self.menu_bar,
            text="File",
            width=60,
            command=self._show_file_menu
        )
        self.file_menu.pack(side="left", padx=2)

        # Project menu
        self.project_menu = ctk.CTkButton(
            self.menu_bar,
            text="Project",
            width=70,
            command=self._show_project_menu
        )
        self.project_menu.pack(side="left", padx=2)

        # View menu
        self.view_menu = ctk.CTkButton(
            self.menu_bar,
            text="View",
            width=60,
            command=self._show_view_menu
        )
        self.view_menu.pack(side="left", padx=2)

        # LLM menu
        self.llm_menu = ctk.CTkButton(
            self.menu_bar,
            text="LLM",
            width=60,
            command=self._show_llm_menu
        )
        self.llm_menu.pack(side="left", padx=2)

        # Help menu
        self.help_menu = ctk.CTkButton(
            self.menu_bar,
            text="Help",
            width=60,
            command=self._show_help
        )
        self.help_menu.pack(side="left", padx=2)

        # Right side - quick actions
        self.save_btn = ctk.CTkButton(
            self.menu_bar,
            text="Save",
            width=60,
            command=self._save_project
        )
        self.save_btn.pack(side="right", padx=2)

    def _create_toolbar(self):
        """Create the toolbar with quick actions."""
        self.toolbar = ctk.CTkFrame(self, height=40)
        self.toolbar.pack(fill="x", padx=5, pady=2)

        # Writing mode selector
        self.mode_label = ctk.CTkLabel(self.toolbar, text="Mode:")
        self.mode_label.pack(side="left", padx=5)

        self.mode_selector = ctk.CTkSegmentedButton(
            self.toolbar,
            values=["Draft", "Collaborate", "Revise", "Outline"],
            command=self._on_mode_change
        )
        self.mode_selector.set("Draft")
        self.mode_selector.pack(side="left", padx=5)

        # Separator
        ctk.CTkFrame(self.toolbar, width=2, height=30).pack(side="left", padx=10)

        # LLM quick actions
        self.llm_continue = ctk.CTkButton(
            self.toolbar,
            text="Continue",
            width=80,
            command=self._llm_continue
        )
        self.llm_continue.pack(side="left", padx=2)

        self.llm_suggest = ctk.CTkButton(
            self.toolbar,
            text="Suggest",
            width=70,
            command=self._llm_suggest
        )
        self.llm_suggest.pack(side="left", padx=2)

        self.llm_rewrite = ctk.CTkButton(
            self.toolbar,
            text="Rewrite",
            width=70,
            command=self._llm_rewrite
        )
        self.llm_rewrite.pack(side="left", padx=2)

        # Right side - word count goal
        self.goal_frame = ctk.CTkFrame(self.toolbar)
        self.goal_frame.pack(side="right", padx=5)

        self.word_count_label = ctk.CTkLabel(
            self.goal_frame,
            text="Words: 0 / 80,000"
        )
        self.word_count_label.pack(side="left", padx=5)

        self.progress_bar = ctk.CTkProgressBar(self.goal_frame, width=150)
        self.progress_bar.set(0)
        self.progress_bar.pack(side="left", padx=5)

    def _create_main_layout(self):
        """Create the main three-panel layout."""
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure grid
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Left panel - Project Navigator
        self._create_navigator_panel()

        # Center panel - Editor
        self._create_editor_panel()

        # Right panel - Context
        self._create_context_panel()

    def _create_navigator_panel(self):
        """Create the project navigator panel."""
        self.nav_panel = ctk.CTkFrame(self.main_container, width=250)
        self.nav_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.nav_panel.grid_propagate(False)

        # Project title
        self.project_title = ctk.CTkLabel(
            self.nav_panel,
            text="No Project",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.project_title.pack(pady=10)

        # Tab view for chapters/notes
        self.nav_tabs = ctk.CTkTabview(self.nav_panel)
        self.nav_tabs.pack(fill="both", expand=True, padx=5, pady=5)

        # Chapters tab
        self.chapters_tab = self.nav_tabs.add("Chapters")
        self.chapters_list = ctk.CTkScrollableFrame(self.chapters_tab)
        self.chapters_list.pack(fill="both", expand=True)

        # Add chapter button
        self.add_chapter_btn = ctk.CTkButton(
            self.chapters_tab,
            text="+ Add Chapter",
            command=self._add_chapter
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

    def _create_editor_panel(self):
        """Create the main writing editor panel."""
        self.editor_panel = ctk.CTkFrame(self.main_container)
        self.editor_panel.grid(row=0, column=1, sticky="nsew", padx=5)

        # Chapter header
        self.chapter_header = ctk.CTkFrame(self.editor_panel, height=40)
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
            self.editor_panel,
            font=ctk.CTkFont(family="Courier", size=14),
            wrap="word"
        )
        self.editor.pack(fill="both", expand=True)

        # Bind text changes for word count
        self.editor.bind("<KeyRelease>", self._on_text_change)

        # Scene notes below editor
        self.scene_notes_frame = ctk.CTkFrame(self.editor_panel, height=100)
        self.scene_notes_frame.pack(fill="x", pady=(5, 0))

        self.scene_notes_label = ctk.CTkLabel(
            self.scene_notes_frame,
            text="Scene Notes",
            font=ctk.CTkFont(weight="bold")
        )
        self.scene_notes_label.pack(anchor="w", padx=5)

        self.scene_notes = ctk.CTkTextbox(self.scene_notes_frame, height=60)
        self.scene_notes.pack(fill="x", padx=5, pady=5)

    def _create_context_panel(self):
        """Create the context/reference panel."""
        self.context_panel = ctk.CTkFrame(self.main_container, width=350)
        self.context_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        self.context_panel.grid_propagate(False)

        # Tab view for different context types
        self.context_tabs = ctk.CTkTabview(self.context_panel)
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
            command=lambda: self._show_bible_section("characters")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            self.bible_buttons,
            text="Settings",
            width=80,
            command=lambda: self._show_bible_section("settings")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            self.bible_buttons,
            text="Plot",
            width=60,
            command=lambda: self._show_bible_section("plot")
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            self.bible_buttons,
            text="Edit",
            width=50,
            command=self._open_bible_editor
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
            command=self._on_genre_change
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
            command=self._send_chat
        )
        self.chat_send.pack(side="right")

        # Bind Enter key
        self.chat_input.bind("<Return>", lambda e: self._send_chat())

    def _create_status_bar(self):
        """Create the status bar."""
        self.status_bar = ctk.CTkFrame(self, height=25)
        self.status_bar.pack(fill="x", padx=5, pady=5)

        # Word count
        self.status_words = ctk.CTkLabel(
            self.status_bar,
            text="Words: 0"
        )
        self.status_words.pack(side="left", padx=10)

        # Current chapter
        self.status_chapter = ctk.CTkLabel(
            self.status_bar,
            text="No chapter"
        )
        self.status_chapter.pack(side="left", padx=10)

        # LLM status
        self.status_llm = ctk.CTkLabel(
            self.status_bar,
            text="LLM: Ready"
        )
        self.status_llm.pack(side="right", padx=10)

        # Save status
        self.status_save = ctk.CTkLabel(
            self.status_bar,
            text="Saved"
        )
        self.status_save.pack(side="right", padx=10)

    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        self.bind("<Control-s>", lambda e: self._save_project())
        self.bind("<Control-n>", lambda e: self._new_project())
        self.bind("<Control-o>", lambda e: self._open_project())
        self.bind("<Control-Shift-c>", lambda e: self._llm_continue())
        self.bind("<Control-Shift-s>", lambda e: self._llm_suggest())

    # Menu handlers
    def _show_file_menu(self):
        """Show file menu options."""
        menu = ctk.CTkToplevel(self)
        menu.geometry("150x150+{}+{}".format(
            self.file_menu.winfo_rootx(),
            self.file_menu.winfo_rooty() + 30
        ))
        menu.overrideredirect(True)
        menu.focus_set()
        menu.bind("<FocusOut>", lambda e: menu.destroy())

        ctk.CTkButton(menu, text="New Project", command=lambda: [menu.destroy(), self._new_project()]).pack(fill="x", padx=5, pady=2)
        ctk.CTkButton(menu, text="Open Project", command=lambda: [menu.destroy(), self._open_project()]).pack(fill="x", padx=5, pady=2)
        ctk.CTkButton(menu, text="Save", command=lambda: [menu.destroy(), self._save_project()]).pack(fill="x", padx=5, pady=2)
        ctk.CTkButton(menu, text="Export", command=lambda: [menu.destroy(), self._export_project()]).pack(fill="x", padx=5, pady=2)

    def _show_project_menu(self):
        """Show project menu options."""
        pass  # TODO: Implement project menu

    def _show_view_menu(self):
        """Show view menu options."""
        pass  # TODO: Implement view menu

    def _show_llm_menu(self):
        """Show LLM menu options."""
        pass  # TODO: Implement LLM settings menu

    def _show_help(self):
        """Show help dialog."""
        pass  # TODO: Implement help

    # Project operations
    def _new_project(self):
        """Create a new project."""
        dialog = NewProjectDialog(self)
        self.wait_window(dialog)

        if dialog.result:
            title, genre, author = dialog.result
            self.current_project = Project.create_new(title, genre, author)
            self.story_bible = StoryBible()
            self._refresh_project_view()

    def _open_project(self):
        """Open an existing project."""
        pass  # TODO: Implement project open dialog

    def _save_project(self):
        """Save the current project."""
        if self.current_project:
            # Update current chapter content
            if self.current_chapter:
                if self.current_chapter.scenes:
                    self.current_chapter.scenes[0].content = self.editor.get("1.0", "end-1c")
                    self.current_chapter.scenes[0].update_word_count()
                self.current_chapter.save(self.current_project.project_path)

            # Save story bible
            if self.story_bible:
                self.story_bible.save(self.current_project.project_path)

            # Save project metadata
            self.current_project.save()

            self.status_save.configure(text="Saved")

    def _export_project(self):
        """Export project to other formats."""
        pass  # TODO: Implement export

    # Chapter operations
    def _add_chapter(self):
        """Add a new chapter."""
        if not self.current_project:
            return

        chapter_num = len(self.current_project.chapter_ids) + 1
        chapter = Chapter(
            number=chapter_num,
            title=f"Chapter {chapter_num}"
        )
        chapter.add_scene()  # Add empty scene

        chapter.save(self.current_project.project_path)
        self.current_project.chapter_ids.append(chapter.id)
        self.current_project.save()

        self._refresh_chapters_list()
        self._load_chapter(chapter)

    def _load_chapter(self, chapter: Chapter):
        """Load a chapter into the editor."""
        self.current_chapter = chapter
        self.chapter_title_entry.delete(0, "end")
        self.chapter_title_entry.insert(0, chapter.title)

        self.editor.delete("1.0", "end")
        if chapter.scenes:
            self.editor.insert("1.0", chapter.scenes[0].content)

        self.status_chapter.configure(text=f"Chapter {chapter.number}: {chapter.title}")
        self._update_word_count()

    def _refresh_chapters_list(self):
        """Refresh the chapters list."""
        # Clear existing
        for widget in self.chapters_list.winfo_children():
            widget.destroy()

        if not self.current_project:
            return

        # Load chapter info
        chapters_dir = self.current_project.project_path / "chapters"
        if chapters_dir.exists():
            for chapter_file in sorted(chapters_dir.glob("chapter_*.json")):
                try:
                    chapter = Chapter.load(
                        self.current_project.project_path,
                        int(chapter_file.stem.split("_")[1])
                    )
                    btn = ctk.CTkButton(
                        self.chapters_list,
                        text=f"{chapter.number}. {chapter.title or 'Untitled'}",
                        command=lambda c=chapter: self._load_chapter(c),
                        anchor="w"
                    )
                    btn.pack(fill="x", pady=2)
                except Exception:
                    pass

    def _refresh_project_view(self):
        """Refresh all project-related views."""
        if self.current_project:
            self.project_title.configure(text=self.current_project.metadata.title)
            self.genre_selector.set(self.current_project.metadata.genre.value)
            self._refresh_chapters_list()
            self._load_research_docs()

    # Text editing callbacks
    def _on_text_change(self, event=None):
        """Handle text changes in editor."""
        self._update_word_count()
        self.status_save.configure(text="Unsaved")

    def _update_word_count(self):
        """Update word count display."""
        text = self.editor.get("1.0", "end-1c")
        word_count = len(text.split()) if text.strip() else 0

        self.status_words.configure(text=f"Words: {word_count}")

        if self.current_project:
            target = self.current_project.metadata.target_word_count
            self.word_count_label.configure(text=f"Words: {word_count:,} / {target:,}")
            progress = min(1.0, word_count / target) if target > 0 else 0
            self.progress_bar.set(progress)

    # Mode handling
    def _on_mode_change(self, mode: str):
        """Handle writing mode changes."""
        pass  # TODO: Adjust UI based on mode

    # LLM operations
    def _llm_continue(self):
        """Continue writing with LLM assistance."""
        self._run_llm_task("continue")

    def _llm_suggest(self):
        """Get LLM suggestions."""
        self._run_llm_task("suggest")

    def _llm_rewrite(self):
        """Rewrite selected text with LLM."""
        self._run_llm_task("rewrite")

    def _run_llm_task(self, task_type: str):
        """Run an LLM task in background."""
        if not self.current_project:
            return

        self.status_llm.configure(text="LLM: Working...")

        # Get current context
        current_text = self.editor.get("1.0", "end-1c")
        bible_context = self.story_bible.generate_llm_context() if self.story_bible else ""

        async def run_task():
            if task_type == "continue":
                response = await self.llm_service.continue_writing(
                    current_text,
                    bible_context,
                    word_count=300
                )
            elif task_type == "suggest":
                response = await self.llm_service.suggest_options(
                    current_text,
                    bible_context
                )
            elif task_type == "rewrite":
                # Get selected text
                try:
                    selected = self.editor.get("sel.first", "sel.last")
                except:
                    selected = current_text[-500:]
                response = await self.llm_service.rewrite_passage(
                    selected,
                    bible_context
                )
            else:
                return

            # Update UI on main thread
            self.after(0, lambda: self._handle_llm_response(response, task_type))

        self.run_async(run_task())

    def _handle_llm_response(self, response, task_type: str):
        """Handle LLM response on main thread."""
        self.status_llm.configure(text="LLM: Ready")

        if response.error:
            self._add_chat_message("System", f"Error: {response.error}")
            return

        if task_type == "continue":
            # Append to editor
            self.editor.insert("end", "\n" + response.content)
        elif task_type in ["suggest", "rewrite"]:
            # Show in chat panel
            self._add_chat_message("LLM", response.content)

    def _send_chat(self):
        """Send a chat message to the LLM."""
        message = self.chat_input.get().strip()
        if not message:
            return

        self.chat_input.delete(0, "end")
        self._add_chat_message("You", message)
        self.status_llm.configure(text="LLM: Working...")

        # Get context
        current_text = self.editor.get("1.0", "end-1c")
        bible_context = self.story_bible.generate_llm_context() if self.story_bible else ""

        async def send_message():
            response = await self.llm_service.generate_content(
                system_prompt="You are a helpful writing assistant. Help the author with their novel.",
                user_prompt=message,
                context=f"Current text:\n{current_text[-2000:]}\n\nStory Bible:\n{bible_context}"
            )
            self.after(0, lambda: self._handle_chat_response(response))

        self.run_async(send_message())

    def _handle_chat_response(self, response):
        """Handle chat response."""
        self.status_llm.configure(text="LLM: Ready")
        if response.error:
            self._add_chat_message("System", f"Error: {response.error}")
        else:
            self._add_chat_message("LLM", response.content)

    def _add_chat_message(self, sender: str, message: str):
        """Add a message to the chat history."""
        self.chat_history.configure(state="normal")
        self.chat_history.insert("end", f"\n{sender}:\n{message}\n")
        self.chat_history.configure(state="disabled")
        self.chat_history.see("end")

    # Story Bible operations
    def _show_bible_section(self, section: str):
        """Show a section of the story bible."""
        if not self.story_bible:
            self.bible_content.delete("1.0", "end")
            self.bible_content.insert("1.0", "No story bible loaded. Create a project first.")
            return

        content = ""
        if section == "characters":
            for char in self.story_bible.characters:
                content += char.get_llm_summary() + "\n\n"
        elif section == "settings":
            for setting in self.story_bible.settings:
                content += f"**{setting.name}**\n{setting.description}\n\n"
        elif section == "plot":
            for thread in self.story_bible.plot_threads:
                content += f"**{thread.name}** ({thread.type})\n{thread.setup}\n\n"

        self.bible_content.delete("1.0", "end")
        self.bible_content.insert("1.0", content if content else "No entries yet.")

    def _open_bible_editor(self):
        """Open the story bible editor."""
        pass  # TODO: Implement full bible editor

    # Research operations
    def _on_genre_change(self, genre: str):
        """Handle genre selection change."""
        self._load_research_docs()

    def _load_research_docs(self):
        """Load research documents for current genre."""
        # Clear existing
        for widget in self.research_list.winfo_children():
            widget.destroy()

        genre = self.genre_selector.get()
        docs = self.research_service.list_documents(genre)

        for doc in docs[:10]:  # Show first 10
            btn = ctk.CTkButton(
                self.research_list,
                text=doc.title[:30] + "..." if len(doc.title) > 30 else doc.title,
                command=lambda d=doc: self._show_research_doc(d),
                anchor="w",
                height=25
            )
            btn.pack(fill="x", pady=1)

    def _show_research_doc(self, doc):
        """Display a research document."""
        self.research_content.delete("1.0", "end")
        self.research_content.insert("1.0", doc.content)


class NewProjectDialog(ctk.CTkToplevel):
    """Dialog for creating a new project."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("New Project")
        self.geometry("400x300")
        self.resizable(False, False)

        self.result = None

        # Title
        ctk.CTkLabel(self, text="Project Title:").pack(pady=(20, 5))
        self.title_entry = ctk.CTkEntry(self, width=300)
        self.title_entry.pack(pady=5)

        # Author
        ctk.CTkLabel(self, text="Author:").pack(pady=(10, 5))
        self.author_entry = ctk.CTkEntry(self, width=300)
        self.author_entry.pack(pady=5)

        # Genre
        ctk.CTkLabel(self, text="Genre:").pack(pady=(10, 5))
        self.genre_selector = ctk.CTkOptionMenu(
            self,
            values=[g.value for g in Genre],
            width=300
        )
        self.genre_selector.pack(pady=5)

        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="Create",
            command=self._create
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy
        ).pack(side="left", padx=10)

        # Make modal
        self.transient(parent)
        self.grab_set()

    def _create(self):
        """Create the project."""
        title = self.title_entry.get().strip()
        if not title:
            return

        author = self.author_entry.get().strip()
        genre = Genre(self.genre_selector.get())

        self.result = (title, genre, author)
        self.destroy()
