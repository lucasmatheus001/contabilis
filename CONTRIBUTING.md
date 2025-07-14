# Contributing to Legal Processes Management System

Thank you for your interest in contributing to the Legal Processes Management System! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (optional)
- Git

### Local Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/legal-processes.git
   cd legal-processes
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

## Code Style

We follow PEP 8 and use several tools to maintain code quality:

### Formatting

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

### Running Code Quality Checks

```bash
# Format code
black processes parties legal_processes

# Sort imports
isort processes parties legal_processes

# Lint code
flake8 processes parties legal_processes

# Run all checks
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=processes --cov=parties

# Run specific test file
pytest processes/tests.py

# Run tests excluding slow tests
pytest -m "not slow"
```

### Writing Tests

- Write tests for all new functionality
- Maintain at least 80% test coverage
- Use descriptive test names
- Follow the existing test structure

### Test Structure

```python
class TestFeature(TestCase):
    def setUp(self):
        """Set up test data."""
        pass
    
    def test_feature_behavior(self):
        """Test specific feature behavior."""
        pass
```

## Git Workflow

### Branch Naming

- `feature/description`: New features
- `bugfix/description`: Bug fixes
- `hotfix/description`: Urgent fixes
- `docs/description`: Documentation updates

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make your changes**
   - Write code following the style guide
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks**
   ```bash
   pre-commit run --all-files
   pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature
   ```

6. **Create Pull Request**
   - Use the PR template
   - Describe your changes
   - Link related issues

## Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Coverage maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## Code Review Guidelines

### For Contributors

- Respond to review comments promptly
- Keep commits focused and atomic
- Address all review feedback

### For Reviewers

- Be constructive and specific
- Focus on code quality and functionality
- Consider security implications
- Check test coverage

## Security

### Reporting Security Issues

- **DO NOT** create public issues for security vulnerabilities
- Email security issues to: security@example.com
- Include detailed description and reproduction steps

### Security Best Practices

- Never commit sensitive data
- Use environment variables for secrets
- Validate all user inputs
- Follow OWASP guidelines

## Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Keep API documentation current

### Documentation Standards

- Use clear, concise language
- Include code examples
- Follow existing formatting

## Release Process

### Versioning

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version bumped
- [ ] Release notes written

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions
- **Documentation**: Check README.md and inline docs

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's code of conduct

Thank you for contributing to the Legal Processes Management System! 