# Contributing Guidelines

Terimakasih tertarik berkontribusi! 🙏

## Core Values

Sebelum contribute, pahami prinsip core:

1. **Privacy First** - Semua kontribusi harus privacy-preserving
2. **No Surveillance** - Tidak ada fitur biometric ID atau event recording
3. **Transparency** - Code harus auditable
4. **Dignity** - Technology untuk enhance human dignity

## How to Contribute

### 1. Report Issues

**Bug Report:**
```markdown
**Deskripsi**: Penjelasan bug
**Steps to Reproduce**: 
1. Step one
2. Step two
**Expected**: Yang seharusnya terjadi
**Actual**: Yang benar-benar terjadi
**Environment**: OS, Python version, dll
```

**Feature Request:**
```markdown
**Use Case**: Kenapa fitur ini perlu?
**Proposed Solution**: Bagaimana cara kerjanya?
**Privacy Check**: Apakah privacy-preserving?
```

### 2. Code Contributions
```bash
# Fork repository
# Clone fork Anda
git clone https://github.com/YOUR_USERNAME/privacy-preserving-robotics.git

# Create branch
git checkout -b feature/nama-fitur

# Make changes
# ...

# Commit
git commit -m "Add: deskripsi singkat"

# Push
git push origin feature/nama-fitur

# Create Pull Request di GitHub
```

### 3. Documentation

- Fix typos
- Improve clarity
- Add examples
- Translate to other languages

## Privacy Review Checklist

Sebelum submit code, cek:

- [ ] Tidak ada biometric data storage
- [ ] Tidak ada event logging dengan timestamps
- [ ] Tidak ada personal information yang reconstructable
- [ ] Hanya ephemeral identities
- [ ] Pattern-based memory, bukan events
- [ ] Learning tanpa raw data storage

## Code Style

- Follow PEP 8 (Python)
- Use type hints
- Write docstrings
- Keep functions focused

## Testing
```bash
# Run tests
pytest tests/

# Check coverage
pytest --cov=src tests/
```

## Communication

- **Issues**: Bug reports & feature requests
- **Discussions**: Questions & ideas
- **Email**: harapan.bontang@gmail.com

## License

By contributing, you agree your contributions will be licensed under GPL-3.0.

---

**Questions?** Jangan ragu bertanya!
