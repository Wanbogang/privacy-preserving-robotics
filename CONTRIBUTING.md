# Contributing Guidelines

Thank you for your interest in contributing to the Privacy-Preserving Home Robotics Framework! 🙏

## Core Values

Before contributing, please understand our core principles:

1. **Privacy First** - All contributions must maintain privacy-preserving properties
2. **No Surveillance** - No features that enable biometric identification or event recording
3. **Transparency** - Code should be understandable and auditable
4. **Dignity** - Technology should enhance human dignity, not diminish it

## How to Contribute

### 1. Report Issues

**Bug Report Template:**
```markdown
**Description**: Clear description of the bug
**Steps to Reproduce**: 
1. Step one
2. Step two
3. Step three
**Expected Behavior**: What should happen
**Actual Behavior**: What actually happens
**Environment**: OS, Python version, hardware details
**Screenshots/Logs**: If applicable
```

**Feature Request Template:**
```markdown
**Use Case**: Why is this feature needed?
**Proposed Solution**: How would it work?
**Privacy Considerations**: How does it maintain privacy?
**Alternatives Considered**: Other approaches you've thought about
```

### 2. Code Contributions

#### Setup Development Environment

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR_USERNAME/privacy-preserving-robotics.git
cd privacy-preserving-robotics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Development Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ... code, test, document ...

# Run tests
pytest tests/

# Run linting
flake8 src/
black src/

# Commit with descriptive message
git add .
git commit -m "Add: brief description of changes

Detailed explanation of what was changed and why.
Addresses #issue_number if applicable."

# Push to your fork
git push origin feature/your-feature-name
```

#### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new features
4. Verify privacy checklist (see below)
5. Create pull request with clear description
6. Respond to review feedback

### 3. Documentation Contributions

We welcome improvements to:
- Fix typos and improve clarity
- Add examples and tutorials
- Improve API documentation
- Translate documentation (while keeping English as primary)
- Add diagrams and visualizations

### 4. Research Contributions

- Implement new privacy-preserving algorithms
- Conduct user studies
- Extend framework to new domains
- Theoretical analysis and proofs
- Performance benchmarking

---

## Privacy Review Checklist

**Before submitting code, verify:**

- [ ] No biometric data storage (no face embeddings, voiceprints, etc.)
- [ ] No event logging with timestamps
- [ ] No reconstructable personal information
- [ ] Only ephemeral identities used
- [ ] Pattern-based memory, not event logs
- [ ] Learning without raw data storage
- [ ] Explanations don't reveal surveillance data
- [ ] Sensor choices are non-identifiable
- [ ] Feature extraction discards raw data immediately

**CRITICAL**: If your contribution stores any of the following, it will be rejected:
- ❌ Biometric identifiers (faces, fingerprints, iris scans, voiceprints)
- ❌ Event logs with timestamps
- ❌ Raw sensor data (images, audio recordings, video)
- ❌ Personal identifiable information linked to real identity
- ❌ Detailed activity histories

---

## Code Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:

```python
# Use type hints
def update_pattern(entity_id: str, observation: dict) -> PatternMemory:
    """
    Update entity pattern with new observation.
    
    Args:
        entity_id: Ephemeral entity identifier
        observation: Abstract feature dictionary
        
    Returns:
        Updated pattern memory object
    """
    pass

# Keep functions focused
def calculate_deviation(current: float, baseline: float) -> float:
    """Calculate statistical deviation from baseline."""
    return abs(current - baseline) / baseline

# Use descriptive variable names
entity_pattern = get_pattern(entity_id)
deviation_score = calculate_deviation(current_activity, entity_pattern.baseline)
```

### Documentation Style

- Write docstrings for all public functions
- Include type information
- Provide usage examples
- Explain privacy implications where relevant

### Naming Conventions

```python
# Classes: PascalCase
class PatternMemory:
    pass

# Functions/methods: snake_case
def detect_anomaly():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_ENTITY_LIFETIME = 30  # days
SIMILARITY_THRESHOLD = 0.85

# Private methods: _leading_underscore
def _internal_helper():
    pass
```

---

## Testing Guidelines

### Unit Tests

```python
import pytest
from src.core import EphemeralIdentity

def test_entity_id_is_ephemeral():
    """Verify entity IDs expire after inactivity."""
    identity_manager = EphemeralIdentity()
    entity_id = identity_manager.create_entity()
    
    # Simulate inactivity period
    simulate_time_passage(days=31)
    
    # Verify entity no longer exists
    assert not identity_manager.exists(entity_id)

def test_no_biometric_storage():
    """Verify no biometric data is stored."""
    storage = get_storage_system()
    
    # Process test data
    process_sensor_data(test_depth_image)
    
    # Verify no biometric data stored
    assert not storage.contains_biometric_data()
    assert not storage.contains_image_data()
```

### Integration Tests

Test complete workflows while verifying privacy properties.

### Privacy Property Tests

Every PR should include tests that verify privacy guarantees are maintained.

---

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
Add: Feature description (for new features)
Fix: Bug description (for bug fixes)
Update: What was updated (for modifications)
Docs: Documentation changes
Test: Test additions or changes
Refactor: Code restructuring without behavior change
```

Example:
```
Add: Anomaly detection for sleep patterns

Implements statistical anomaly detection for sleep monitoring use case.
Uses exponential moving average with decay factor to adapt to
changing patterns without storing historical events.

Addresses #42
```

---

## Code Review Process

### What Reviewers Look For

1. **Privacy Compliance**: Does it maintain privacy guarantees?
2. **Code Quality**: Is it readable, testable, maintainable?
3. **Documentation**: Are changes documented?
4. **Tests**: Are there adequate tests?
5. **Performance**: Is it efficient enough for real-time use?

### Response Time

- Initial review: Within 1 week
- Follow-up reviews: Within 3 days
- Simple fixes: May be merged quickly
- Major features: May require multiple review rounds

---

## Communication Channels

### GitHub Issues
For bug reports, feature requests, and technical discussions.

### GitHub Discussions
For general questions, ideas, and community discussion.

### Email
For sensitive topics or private inquiries: harapan.bontang@gmail.com

---

## Recognition

### Contributor List
All contributors will be acknowledged in [CONTRIBUTORS.md](CONTRIBUTORS.md).

### Significant Contributions
Major contributions may warrant:
- Co-authorship on future papers
- Maintainer status
- Special recognition in releases

---

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to: harapan.bontang@gmail.com

---

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0.

This means:
- Your code will remain open source
- Others can use, modify, and distribute it
- Derivative works must also be open source
- You retain copyright to your contributions

---

## Getting Help

**Stuck? Have questions?**

- Check existing [Issues](https://github.com/Wanbogang/privacy-preserving-robotics/issues)
- Start a [Discussion](https://github.com/Wanbogang/privacy-preserving-robotics/discussions)
- Email: harapan.bontang@gmail.com

**Don't hesitate to ask!** We're here to help and we appreciate your interest in contributing.

---

## Quick Start Checklist

- [ ] Read and understand core values
- [ ] Fork the repository
- [ ] Clone your fork locally
- [ ] Create a feature branch
- [ ] Make your changes
- [ ] Write/update tests
- [ ] Run tests and linting
- [ ] Check privacy compliance
- [ ] Commit with clear messages
- [ ] Push to your fork
- [ ] Create pull request
- [ ] Respond to review feedback

---

**Thank you for contributing to privacy-preserving robotics!** Together, we can build technology that respects human dignity. 🤝
