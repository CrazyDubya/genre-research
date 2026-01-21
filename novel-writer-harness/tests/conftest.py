"""
Pytest configuration and shared fixtures.
"""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def sample_project_dir(temp_dir):
    """Create a sample project directory structure."""
    project_dir = temp_dir / "test_project"
    project_dir.mkdir()
    (project_dir / "chapters").mkdir()
    (project_dir / "research").mkdir()
    (project_dir / "exports").mkdir()
    return project_dir
