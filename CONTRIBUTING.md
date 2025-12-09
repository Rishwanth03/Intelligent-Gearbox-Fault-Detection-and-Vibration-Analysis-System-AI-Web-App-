# Contributing to Gearbox Fault Detection System

Thank you for your interest in contributing to the Intelligent Gearbox Fault Detection System! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/Intelligent-Gearbox-Fault-Detection-and-Vibration-Analysis-System-AI-Web-App-.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Set up the development environment (see README.md)

## Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_system.py
```

## Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Comment complex logic

## Adding Features

### Backend Features

- Add new analysis algorithms in `backend/analyzer.py`
- Add new preprocessing methods in `backend/preprocessor.py`
- Add new visualizations in `backend/visualizer.py`
- Update tests in `test_system.py`

### Frontend Features

- Update the main interface in `templates/index.html`
- Maintain responsive design principles
- Ensure accessibility standards are met

### ML Models

- Place trained models in the `models/` directory
- Update model loading code in relevant backend modules
- Document model architecture and training process

## Testing

- Write tests for all new features
- Ensure all existing tests pass
- Test with sample data using `generate_sample_data.py`
- Test the web interface manually

## Documentation

- Update README.md if adding new features or changing setup
- Add comments to complex code sections
- Update API documentation if adding new endpoints

## Submitting Changes

1. Commit your changes with clear, descriptive messages
2. Push to your fork
3. Create a Pull Request with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots for UI changes
   - Test results

## Pull Request Guidelines

- Keep PRs focused on a single feature or bug fix
- Include tests for new functionality
- Update documentation as needed
- Ensure all tests pass
- Follow the existing code style

## Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces
- Sample data if relevant

## Feature Requests

For feature requests, please describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered
- How it benefits other users

## Code Review Process

- All submissions require review
- Maintainers will provide feedback
- Address review comments
- Once approved, changes will be merged

## Community

- Be respectful and inclusive
- Help others learn
- Share knowledge
- Follow the code of conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions about contributing!
