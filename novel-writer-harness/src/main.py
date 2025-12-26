#!/usr/bin/env python3
"""
Novel Writer Harness - Main Entry Point

A GUI application for collaborative novel writing between humans and LLMs.
"""
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))


def main():
    """Run the Novel Writer Harness application."""
    from gui import MainWindow

    print("Starting Novel Writer Harness...")
    print("=" * 50)

    app = MainWindow()

    # Center window on screen
    app.update_idletasks()
    width = app.winfo_width()
    height = app.winfo_height()
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"+{x}+{y}")

    print("Application ready.")
    print("Use File > New Project to start writing.")
    print("=" * 50)

    app.mainloop()


if __name__ == "__main__":
    main()
