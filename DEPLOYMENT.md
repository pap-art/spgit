# Deployment Checklist

Complete checklist for deploying spgit to production.

## Pre-Deployment Verification

### 1. Code Quality
- [ ] All code formatted with black
- [ ] All code passes flake8 linting
- [ ] Type hints added where appropriate
- [ ] Docstrings complete for public APIs
- [ ] No debug print statements
- [ ] No hardcoded credentials

### 2. Testing
- [ ] All unit tests pass
- [ ] Test coverage > 80%
- [ ] Manual testing on Windows
- [ ] Manual testing on macOS
- [ ] Manual testing on Linux
- [ ] Integration tests with real Spotify API
- [ ] Performance benchmarks recorded

### 3. Documentation
- [ ] README.md complete
- [ ] QUICKSTART.md clear for beginners
- [ ] EXAMPLES.md covers common use cases
- [ ] INSTALL.md covers all platforms
- [ ] CONTRIBUTING.md guides contributors
- [ ] API documentation generated
- [ ] Changelog updated

### 4. Version Control
- [ ] All changes committed
- [ ] Version number updated in `__init__.py`
- [ ] Git tags created for version
- [ ] Release notes written
- [ ] CHANGELOG.md updated

### 5. Dependencies
- [ ] requirements.txt up to date
- [ ] pyproject.toml dependencies correct
- [ ] Version constraints specified
- [ ] Security vulnerabilities checked

## PyPI Deployment

### 1. Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distributions
python -m build

# Verify contents
tar -tzf dist/spgit-*.tar.gz
unzip -l dist/spgit-*.whl
```

### 2. Test on TestPyPI

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ spgit

# Run verification
python verify.py
```

### 3. Deploy to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*

# Verify on PyPI
open https://pypi.org/project/spgit/
```

### 4. Post-Deployment Testing

```bash
# Fresh install
pip install spgit

# Run all verifications
python verify.py

# Test basic workflow
spgit --version
spgit --help
```

## GitHub Release

### 1. Create Release

```bash
# Tag version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Create release on GitHub
# - Go to Releases
# - Click "Draft a new release"
# - Select tag v1.0.0
# - Add release notes
# - Attach distributions
# - Publish release
```

### 2. Release Notes Template

```markdown
# spgit v1.0.0

First stable release of spgit - Git for Spotify Playlists!

## Features

- Complete git-like command set (25 commands)
- Repository management with .spgit directory
- SHA-1 object database with compression
- Three-way merge with multiple strategies
- Branch management and rebasing
- Reflog for history tracking
- Color-coded output
- Cross-platform support

## Installation

```bash
pip install spgit
```

## Quick Start

See [QUICKSTART.md](QUICKSTART.md)

## Documentation

- [README.md](README.md) - Complete documentation
- [EXAMPLES.md](EXAMPLES.md) - Usage examples
- [INSTALL.md](INSTALL.md) - Installation guide

## What's Changed

Initial release with full feature set.

## Contributors

Thanks to all contributors!
```

## Docker Deployment (Optional)

### 1. Build Docker Image

```bash
# Create Dockerfile
docker build -t spgit:1.0.0 .
docker tag spgit:1.0.0 spgit:latest

# Test image
docker run spgit:latest --version
```

### 2. Push to Docker Hub

```bash
# Tag for Docker Hub
docker tag spgit:1.0.0 username/spgit:1.0.0
docker tag spgit:1.0.0 username/spgit:latest

# Push
docker push username/spgit:1.0.0
docker push username/spgit:latest
```

## Post-Deployment

### 1. Monitor

- [ ] Check PyPI downloads
- [ ] Monitor GitHub issues
- [ ] Check error reports
- [ ] Review user feedback

### 2. Announce

- [ ] Post on Reddit (r/Python, r/spotify)
- [ ] Post on Twitter/X
- [ ] Post on Hacker News
- [ ] Post on relevant forums
- [ ] Email newsletter (if applicable)

### 3. Community

- [ ] Set up discussions on GitHub
- [ ] Create Discord/Slack channel (optional)
- [ ] Set up issue templates
- [ ] Create PR templates
- [ ] Add code of conduct

### 4. Maintenance

- [ ] Set up automated testing (GitHub Actions)
- [ ] Set up dependabot for security updates
- [ ] Plan roadmap for v1.1.0
- [ ] Schedule regular releases

## Security

### 1. Security Checklist

- [ ] No credentials in code
- [ ] Secure authentication flow
- [ ] Input validation everywhere
- [ ] No SQL injection (N/A - no SQL)
- [ ] No command injection risks
- [ ] Secure file operations
- [ ] Rate limiting handled

### 2. Vulnerability Response

- [ ] Security policy documented (SECURITY.md)
- [ ] Private vulnerability reporting enabled
- [ ] Response plan in place
- [ ] Security contact listed

## Rollback Plan

If critical issues found:

### 1. Quick Fix

```bash
# Patch version
git checkout v1.0.0
git checkout -b hotfix-1.0.1
# Fix issue
git commit -m "Fix critical issue"
git tag v1.0.1
git push origin v1.0.1

# Build and deploy
python -m build
twine upload dist/*
```

### 2. Version Yank (Last Resort)

```bash
# Yank broken version from PyPI
twine yank spgit==1.0.0 -m "Critical bug found"

# Users can still install with --no-deps if needed
```

## Performance Monitoring

### 1. Metrics to Track

- [ ] Average clone time
- [ ] Average commit time
- [ ] API call frequency
- [ ] Error rates
- [ ] User retention

### 2. Benchmarking

```bash
# Run benchmarks
python benchmark.py

# Record results
# - 100 track clone: X seconds
# - Commit operation: X ms
# - Push operation: X seconds
# - Memory usage: X MB
```

## Legal

- [ ] LICENSE file present (MIT)
- [ ] Copyright notices correct
- [ ] Third-party licenses acknowledged
- [ ] Terms of service reviewed
- [ ] Privacy policy (if collecting data)

## Communication

### 1. Documentation Sites

- [ ] GitHub Pages deployed
- [ ] ReadTheDocs configured (optional)
- [ ] Wiki pages created

### 2. Support Channels

- [ ] GitHub Issues for bugs
- [ ] GitHub Discussions for questions
- [ ] Email for security issues
- [ ] Twitter for announcements

## Continuous Integration

### 1. GitHub Actions

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -e ".[dev]"
          pytest
```

### 2. Automated Releases

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and publish
        run: |
          python -m build
          twine upload dist/*
```

## Final Checks

Before going live:

1. ✅ All tests pass
2. ✅ Documentation complete
3. ✅ Version numbers correct
4. ✅ Changelog updated
5. ✅ Security reviewed
6. ✅ Performance acceptable
7. ✅ License in place
8. ✅ Dependencies secure
9. ✅ Backup plan ready
10. ✅ Team notified

## Go Live!

```bash
# Final verification
python verify.py

# Build
python -m build

# Deploy to PyPI
twine upload dist/*

# Create GitHub release
# Push tag
git push origin v1.0.0

# Announce
# Post on social media
# Update documentation
# Celebrate! 🎉
```

## Post-Launch (Week 1)

- [ ] Monitor error rates
- [ ] Respond to issues within 24h
- [ ] Update FAQ based on questions
- [ ] Fix critical bugs immediately
- [ ] Thank early adopters

## Success Metrics

Track for first month:

- Downloads: Target X
- GitHub stars: Target X
- Issues opened: Normal < 10/week
- Pull requests: Target X
- Community engagement: Growing

## Long Term

- Regular releases (monthly)
- Community growth
- Feature additions based on feedback
- Performance improvements
- Ecosystem integrations

---

**Ready for deployment? Run through this checklist and launch!** 🚀
