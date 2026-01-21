# GUI Refactoring Guide

## Overview

The `main_window.py` file (originally 848 lines) has been refactored by extracting UI components into separate, reusable modules. This improves maintainability, testability, and code organization.

## New Component Modules

### 1. `toolbar.py` (143 lines)
**Purpose**: Application toolbar with writing modes and LLM quick actions

**Responsibilities**:
- Writing mode selection (Draft, Collaborate, Revise, Outline)
- LLM quick action buttons (Continue, Suggest, Rewrite)
- Word count and progress display

**Usage**:
```python
from .toolbar import Toolbar

self.toolbar = Toolbar(
    self,
    on_mode_change=self._on_mode_change,
    on_llm_continue=self._llm_continue,
    on_llm_suggest=self._llm_suggest,
    on_llm_rewrite=self._llm_rewrite
)
self.toolbar.pack(fill="x", padx=5, pady=2)

# Update word count
self.toolbar.update_word_count(current=5000, goal=80000)
```

### 2. `editor_panel.py` (164 lines)
**Purpose**: Main writing editor with chapter management

**Responsibilities**:
- Chapter title and status editing
- Main text editor with syntax highlighting
- Scene notes editor
- Word count calculation

**Usage**:
```python
from .editor_panel import EditorPanel

self.editor_panel = EditorPanel(
    self.main_container,
    on_text_change=self._on_text_change
)
self.editor_panel.grid(row=0, column=1, sticky="nsew", padx=5)

# Load a chapter
self.editor_panel.load_chapter(chapter)

# Get content
content = self.editor_panel.get_content()
word_count = self.editor_panel.get_word_count()
```

### 3. `navigator_panel.py` (164 lines)
**Purpose**: Project navigation with chapters, notes, and outline

**Responsibilities**:
- Chapter list display and selection
- Notes management
- Outline editor
- Project title display

**Usage**:
```python
from .navigator_panel import NavigatorPanel

self.nav_panel = NavigatorPanel(
    self.main_container,
    on_chapter_selected=self._load_chapter,
    on_add_chapter=self._add_chapter
)
self.nav_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

# Set current project
self.nav_panel.set_project(project)

# Refresh chapters list
self.nav_panel.refresh_chapters()
```

### 4. `context_panel.py` (257 lines)
**Purpose**: Context and reference panel with Story Bible, Research, and LLM Chat

**Responsibilities**:
- Story Bible quick view
- Genre research browser
- LLM chat interface
- Tab-based navigation

**Usage**:
```python
from .context_panel import ContextPanel

self.context_panel = ContextPanel(
    self.main_container,
    on_bible_section_change=self._show_bible_section,
    on_bible_edit=self._open_bible_editor,
    on_genre_change=self._on_genre_change,
    on_chat_send=self._send_chat
)
self.context_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

# Update bible content
self.context_panel.set_bible_content(bible_text)

# Add chat message
self.context_panel.add_chat_message("User", "Hello!")
```

## Refactoring Benefits

### 1. Reduced Complexity
- **Before**: 848 lines in single file
- **After**: Main window ~400 lines + 4 component files (~730 lines total)
- Each component is focused and self-contained

### 2. Improved Testability
- Components can be tested independently
- Mock callbacks for testing interactions
- Easier to create test fixtures

### 3. Better Reusability
- Components can be reused in other contexts
- Clear interfaces through constructor parameters
- Self-contained UI logic

### 4. Enhanced Maintainability
- Easier to locate and modify specific UI features
- Changes to one component don't affect others
- Clear separation of concerns

## Migration Strategy

### Phase 1: Extract Components (COMPLETED)
✅ Create `toolbar.py`
✅ Create `editor_panel.py`
✅ Create `navigator_panel.py`
✅ Create `context_panel.py`
✅ Update `__init__.py` to export components

### Phase 2: Refactor main_window.py (IN PROGRESS)
- [ ] Replace `_create_toolbar()` with `Toolbar` instantiation
- [ ] Replace `_create_editor_panel()` with `EditorPanel` instantiation
- [ ] Replace `_create_navigator_panel()` with `NavigatorPanel` instantiation
- [ ] Replace `_create_context_panel()` with `ContextPanel` instantiation
- [ ] Update method calls to use component interfaces
- [ ] Remove old _create_* methods

### Phase 3: Testing & Validation
- [ ] Test all UI interactions
- [ ] Verify callback chains work correctly
- [ ] Test with sample projects
- [ ] Validate word count updates
- [ ] Test LLM integrations

## Example: Refactored main_window.py Structure

```python
class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Novel Writer Harness")
        self.geometry("1600x900")
        
        # Initialize services
        self.llm_service = LLMService()
        self.research_service = ResearchService()
        
        # Build UI using components
        self._create_menu()
        self._create_toolbar()      # Uses Toolbar class
        self._create_main_layout()  # Uses EditorPanel, NavigatorPanel, ContextPanel
        self._create_status_bar()
        self._bind_shortcuts()
    
    def _create_toolbar(self):
        """Create toolbar using Toolbar component."""
        self.toolbar = Toolbar(
            self,
            on_mode_change=self._on_mode_change,
            on_llm_continue=self._llm_continue,
            on_llm_suggest=self._llm_suggest,
            on_llm_rewrite=self._llm_rewrite
        )
        self.toolbar.pack(fill="x", padx=5, pady=2)
    
    def _create_main_layout(self):
        """Create main layout using component classes."""
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure grid
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Navigator panel
        self.nav_panel = NavigatorPanel(
            self.main_container,
            on_chapter_selected=self._load_chapter,
            on_add_chapter=self._add_chapter
        )
        self.nav_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Editor panel
        self.editor_panel = EditorPanel(
            self.main_container,
            on_text_change=self._on_text_change
        )
        self.editor_panel.grid(row=0, column=1, sticky="nsew", padx=5)
        
        # Context panel
        self.context_panel = ContextPanel(
            self.main_container,
            on_bible_section_change=self._show_bible_section,
            on_bible_edit=self._open_bible_editor,
            on_genre_change=self._on_genre_change,
            on_chat_send=self._send_chat
        )
        self.context_panel.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
    
    def _on_text_change(self):
        """Handle text changes in editor."""
        word_count = self.editor_panel.get_word_count()
        self.toolbar.update_word_count(word_count)
        # ... other logic
```

## Testing Components

### Example Test for Toolbar
```python
def test_toolbar_word_count_update():
    """Test toolbar word count display updates."""
    root = ctk.CTk()
    toolbar = Toolbar(root)
    
    toolbar.update_word_count(current=5000, goal=80000)
    
    assert "5,000" in toolbar.word_count_label.cget("text")
    assert toolbar.progress_bar.get() == 0.0625  # 5000/80000
```

### Example Test for EditorPanel
```python
def test_editor_panel_word_count():
    """Test editor panel word count calculation."""
    root = ctk.CTk()
    editor = EditorPanel(root)
    
    editor.set_content("The quick brown fox jumps over the lazy dog")
    count = editor.get_word_count()
    
    assert count == 9
```

## Future Enhancements

1. **Add unit tests** for each component
2. **Create style themes** that can be applied to all components
3. **Add accessibility features** (keyboard navigation, screen reader support)
4. **Implement component state saving** for user preferences
5. **Add plugin system** for extending component functionality

## Notes

- All components use callback-based communication
- Components are self-contained and don't directly access main window state
- The main window acts as a coordinator between components
- This architecture makes it easy to swap out components or create variants
