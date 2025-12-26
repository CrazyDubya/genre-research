# Novel Writer Harness

A GUI application for collaborative novel writing between humans and LLMs, leveraging the genre research library for structured, genre-aware storytelling.

## Overview

The Novel Writer Harness provides a complete environment for writing novels with AI assistance:

- **Project Management**: Create, organize, and track novel projects
- **Genre Integration**: Access genre-specific guidance from the research library
- **Story Bible Management**: Maintain consistency with character, setting, and plot tracking
- **LLM Collaboration**: Seamlessly integrate AI suggestions and drafting
- **Writing Interface**: Distraction-free editor with context-aware assistance
- **Progress Tracking**: Monitor word counts, chapter status, and milestones

## Architecture

```
novel-writer-harness/
├── src/
│   ├── main.py                 # Application entry point
│   ├── gui/
│   │   ├── main_window.py      # Main application window
│   │   ├── project_panel.py    # Project management sidebar
│   │   ├── editor_panel.py     # Writing editor
│   │   ├── research_panel.py   # Genre research browser
│   │   ├── bible_panel.py      # Story bible editor
│   │   └── llm_panel.py        # LLM interaction panel
│   ├── models/
│   │   ├── project.py          # Project data model
│   │   ├── chapter.py          # Chapter/scene models
│   │   ├── story_bible.py      # Story bible elements
│   │   └── context.py          # LLM context management
│   ├── services/
│   │   ├── llm_service.py      # LLM API integration
│   │   ├── research_service.py # Genre research access
│   │   ├── export_service.py   # Export to various formats
│   │   └── storage_service.py  # Project persistence
│   └── utils/
│       ├── config.py           # Configuration management
│       └── helpers.py          # Utility functions
├── projects/                   # User project storage
├── config/
│   └── settings.json           # Application settings
└── requirements.txt            # Python dependencies
```

## Key Features

### 1. Context-Aware LLM Integration

The harness maintains a "Story Context" that keeps the LLM informed about:
- Character profiles and relationships
- World-building details
- Plot threads and timeline
- Genre conventions and tropes
- Previously written content

### 2. Genre Research Integration

Direct access to the genre research library:
- Quick-reference panels for genre conventions
- Template insertion from story bibles
- Checklist tracking for revision phases
- Examples and best practices

### 3. Writing Modes

- **Draft Mode**: Free-flowing writing with minimal interference
- **Collaboration Mode**: Real-time LLM suggestions and co-writing
- **Revision Mode**: Systematic editing with checklist integration
- **Outline Mode**: Structure and planning view

### 4. LLM Interaction Patterns

- **Continue**: Let LLM continue from current point
- **Suggest**: Get multiple options for next passage
- **Rewrite**: Request alternative versions of selected text
- **Expand**: Elaborate on sparse passages
- **Condense**: Tighten verbose sections
- **Dialog**: Generate character dialogue
- **Describe**: Add sensory/environmental details

## Installation

```bash
cd novel-writer-harness
pip install -r requirements.txt
python src/main.py
```

## Usage

1. **Create Project**: Start a new novel project with genre selection
2. **Set Up Story Bible**: Define characters, settings, plot outline
3. **Write**: Use the editor with LLM assistance as needed
4. **Track Progress**: Monitor chapters, word count, completion status
5. **Revise**: Use genre-specific checklists for systematic revision
6. **Export**: Generate final manuscript in desired format

## LLM Provider Support

The harness supports multiple LLM backends:
- Claude (Anthropic API)
- OpenAI GPT models
- Local models via Ollama
- Custom API endpoints

## License

MIT License - See LICENSE file for details
