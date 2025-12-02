# Contributing to spgit

Thank you for your interest in contributing to spgit! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and inclusive. We welcome contributions from everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/spgit/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, spotipy version)

### Suggesting Features

1. Check if the feature has been requested in [Issues](https://github.com/yourusername/spgit/issues)
2. Create a new issue describing:
   - The feature and its use case
   - How it aligns with spgit's goals
   - Potential implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code with black (`black spgit/`)
7. Lint code (`flake8 spgit/`)
8. Commit your changes (`git commit -m 'Add amazing feature'`)
9. Push to your branch (`git push origin feature/amazing-feature`)
10. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/spgit.git
cd spgit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=spgit --cov-report=html
```

## Code Style

- Follow PEP 8
- Use black for formatting (line length 100)
- Use type hints where appropriate
- Write docstrings for public functions/classes
- Keep functions focused and small

## Testing

- Write tests for all new features
- Maintain test coverage above 80%
- Use descriptive test names
- Test edge cases and error conditions

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense (e.g., "Add", "Fix", "Update")
- Reference issues when applicable (#123)

## Questions?

Feel free to ask questions in [Discussions](https://github.com/yourusername/spgit/discussions).
