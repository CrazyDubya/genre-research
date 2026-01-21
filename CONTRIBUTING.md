# Contributing to Genre Research

Thank you for your interest in contributing to the Genre Research repository! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

---

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors:

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Issues

Before creating an issue:
- Check if the issue already exists
- Use the issue template if available
- Provide clear steps to reproduce bugs
- Include relevant system information

### Suggesting Enhancements

We welcome suggestions for:
- New genre research libraries
- Additional writing frameworks
- Tool improvements
- Documentation enhancements

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
6. **Push to your fork** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Contributing Documentation

Documentation contributions are highly valued:
- Improve existing genre guides
- Add new examples and breakdowns
- Fix typos and clarify explanations
- Translate content (future)

---

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- pip or pipenv

### Setting Up Novel Writer Harness

```bash
# Clone the repository
git clone https://github.com/CrazyDubya/genre-research.git
cd genre-research

# Navigate to Novel Writer Harness
cd novel-writer-harness

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run the application
python src/main.py
```

### Environment Variables

Create a `.env` file in `novel-writer-harness/` with:

```
# LLM API Keys (at least one required)
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here

# Optional: Custom models
ANTHROPIC_MODEL=claude-sonnet-4-20250514
OPENAI_MODEL=gpt-4o

# Optional: Ollama (local)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

---

## Coding Standards

### Python Code Style

We follow **PEP 8** with some specific guidelines:

#### Formatting
- **Line length**: Maximum 120 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings (generally)
- **Imports**: Organized using `isort`

#### Code Quality Tools

Run these before committing:

```bash
# Format code
black src/

# Sort imports
isort src/

# Lint code
flake8 src/

# Type check
mypy src/
```

#### Type Hints

- Use type hints for all function parameters and return values
- Use `from typing import ...` for complex types
- Target: 90%+ type hint coverage

```python
# Good
def calculate_word_count(text: str) -> int:
    return len(text.split())

# Also good
from typing import Optional, List

def find_chapter(chapters: List[Chapter], title: str) -> Optional[Chapter]:
    for chapter in chapters:
        if chapter.title == title:
            return chapter
    return None
```

#### Naming Conventions

- **Classes**: `PascalCase` (e.g., `StoryBible`, `LLMService`)
- **Functions/Variables**: `snake_case` (e.g., `calculate_word_count`, `user_input`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_TOKENS`, `DEFAULT_MODEL`)
- **Private methods**: Prefix with `_` (e.g., `_internal_helper`)

---

## Testing Guidelines

### Writing Tests

- Place tests in `novel-writer-harness/tests/`
- Follow the structure: `test_<module>/test_<file>.py`
- Use descriptive test names: `test_<what>_<scenario>_<expected>`

```python
def test_word_count_with_empty_string_returns_zero():
    """Test word count returns 0 for empty string."""
    result = word_count("")
    assert result == 0

def test_word_count_with_multiple_words_returns_correct_count():
    """Test word count calculates correctly."""
    result = word_count("The quick brown fox")
    assert result == 4
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_models/test_chapter.py

# Run specific test
pytest tests/test_models/test_chapter.py::test_scene_word_count
```

### Test Coverage

- Aim for **80%+ coverage** for new code
- Critical paths should have **100% coverage**
- Tests run automatically in CI/CD pipeline

---

## Documentation Standards

### Markdown Files

#### File Organization
- Keep files under **600 lines** for readability
- Use clear heading hierarchy (`#`, `##`, `###`)
- Include table of contents for longer documents

#### Writing Style
- Write in **present tense**
- Be **clear and concise**
- Use **examples** to illustrate concepts
- Include **code snippets** where helpful

#### Links
- Use **relative links** for internal navigation
- Check links with the documentation CI workflow
- Format: `[Link Text](./relative/path.md)`

### Python Docstrings

Use **Google-style docstrings**:

```python
def calculate_readability(text: str, include_syllables: bool = False) -> dict:
    """
    Calculate readability metrics for text.

    Computes various readability scores including word count,
    sentence count, and optionally syllable count.

    Args:
        text: The text to analyze
        include_syllables: Whether to include syllable count

    Returns:
        Dictionary with readability metrics:
        - words: Total word count
        - sentences: Total sentence count
        - avg_word_length: Average characters per word
        - avg_sentence_length: Average words per sentence

    Raises:
        ValueError: If text is None

    Example:
        >>> metrics = calculate_readability("Hello world. How are you?")
        >>> metrics['words']
        5
    """
    # Implementation
```

### Genre Research Documentation

When adding new genre research:

1. **Follow the established structure**:
   ```
   genre-name-research/
   ├── README.md (overview)
   ├── QUICKSTART.md (getting started)
   ├── fundamentals/ (core concepts)
   ├── characters/ (character archetypes)
   ├── plot-structure/ (story structures)
   ├── examples/ (concrete examples)
   └── story-framework/ (templates/checklists)
   ```

2. **Use consistent formatting**
3. **Include concrete examples**
4. **Cross-reference related content**
5. **Keep individual files focused and digestible**

---

## Pull Request Process

### Before Submitting

1. ✅ **Run all tests** and ensure they pass
2. ✅ **Run code quality tools** (black, isort, flake8)
3. ✅ **Update documentation** if needed
4. ✅ **Add tests** for new functionality
5. ✅ **Check for large files** (documentation >1000 lines)

### PR Description

Include in your PR description:

- **What**: Brief description of changes
- **Why**: Reason for the changes
- **How**: Implementation approach
- **Testing**: How you tested the changes
- **Screenshots**: For UI changes (if applicable)

### Example PR Template

```markdown
## Description
Brief description of what this PR does.

## Related Issue
Closes #123

## Changes Made
- Added X feature
- Fixed Y bug
- Updated Z documentation

## Testing
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Manually tested the changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** run (tests, linting, coverage)
2. **Code review** by maintainers
3. **Address feedback** and update PR
4. **Approval** and merge

### Commit Messages

Write clear, descriptive commit messages:

```
feat: Add romantic comedy structure examples

- Created detailed breakdown of romcom formula
- Included "When Harry Met Sally" case study
- Added beat-by-beat structure analysis
```

Prefix types:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Formatting changes
- `chore:` Maintenance tasks

---

## Project Structure

### Repository Organization

```
genre-research/
├── action-genre-research/
├── comedy-writing-research/
├── horror-genre-research/
├── romance-story-research/
├── ... (other genre libraries)
├── novel-writer-harness/        # Python GUI application
│   ├── src/
│   │   ├── models/               # Data models
│   │   ├── services/             # Business logic
│   │   ├── gui/                  # UI components
│   │   └── utils/                # Helper functions
│   ├── tests/                    # Test files
│   └── requirements.txt
├── .github/
│   └── workflows/                # CI/CD pipelines
├── COMPREHENSIVE_CODE_REVIEW.md
├── CONTRIBUTING.md               # This file
└── README.md
```

### Key Files

- **README.md**: Repository overview and navigation
- **COMPREHENSIVE_CODE_REVIEW.md**: Detailed code analysis
- **P1_IMPLEMENTATION_SUMMARY.md**: Implementation progress
- **Genre README files**: Entry points for each genre

---

## Getting Help

### Questions

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Create an issue with the bug template
- **Feature requests**: Create an issue with the feature template

### Communication

- Be patient and respectful
- Provide context and details
- Share relevant code snippets
- Include error messages and logs

---

## Recognition

Contributors will be recognized in:
- Git commit history
- Release notes for significant contributions
- Project acknowledgments

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Genre Research!** 🎉

Your contributions help writers worldwide create better stories.
