# Contributing to DeepSignal

Thank you for your interest in contributing to DeepSignal! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Protect user privacy and data security
- Never introduce PII into the codebase

## Development Setup

```bash
# Clone the repository
git clone https://github.com/anandbmuley/deep-signal.git
cd deep-signal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov

# Set up environment
cp .env.example .env
# Edit .env and add your GitHub token
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=deep_signal tests/

# Run specific test file
pytest tests/test_agent_a.py -v
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clear, concise code
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Your Changes

```bash
git add .
git commit -m "Add feature: brief description"
```

Use clear, descriptive commit messages:
- `Add feature: description` for new features
- `Fix: description` for bug fixes
- `Update: description` for changes to existing features
- `Docs: description` for documentation changes

### 4. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## What to Contribute

### High Priority

- Additional data source agents (LinkedIn, Stack Overflow, etc.)
- Improved green-washing detection algorithms
- Performance optimizations
- More comprehensive tests
- Documentation improvements

### Welcome Contributions

- Bug fixes
- New risk detection patterns
- Example scripts and use cases
- Integration with ATS systems
- UI/Dashboard components

### Areas Needing Attention

- Machine learning integration
- Real-time monitoring capabilities
- Batch processing optimizations
- API endpoint development
- Internationalization

## Adding New Agents

To add a new agent:

1. Create a new file in `src/deep_signal/agents/`
2. Implement the agent class with `analyze(candidate)` method
3. Return an `AgentReport` object
4. Add tests in `tests/test_your_agent.py`
5. Update orchestrator to include the new agent
6. Update documentation

Example agent structure:

```python
from ..models.candidate import CandidateProfile
from ..models.report import AgentReport, RiskFactor, RiskLevel

class YourAgent:
    def __init__(self):
        self.agent_name = "Your Agent Name"
    
    def analyze(self, candidate: CandidateProfile) -> AgentReport:
        # Your analysis logic here
        return AgentReport(
            agent_name=self.agent_name,
            score=score,
            confidence=confidence,
            risk_factors=risks,
            signals=signals
        )
```

## Testing Guidelines

- Write tests for all new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use meaningful test names
- Mock external API calls

## Documentation

When adding features:

- Update README.md if user-facing
- Add docstrings to all new functions/classes
- Update ARCHITECTURE.md for architectural changes
- Add examples if appropriate
- Update type hints

## Security Considerations

**CRITICAL:** This project handles sensitive candidate data.

### Must Do:
- Never log or store PII
- Validate all inputs for PII
- Use anonymous identifiers only
- Sanitize data before processing
- Follow GDPR/privacy best practices

### Code Review Checklist:
- [ ] No PII in test data
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] Error messages don't leak PII
- [ ] External API calls are secure

## Pull Request Process

1. **Update tests**: Ensure all tests pass
2. **Update documentation**: Keep docs in sync with code
3. **Add examples**: If adding new features
4. **Code review**: Address reviewer feedback
5. **Squash commits**: Before merging (if requested)

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## Thank You!

Your contributions help make DeepSignal better for everyone. We appreciate your time and effort!
