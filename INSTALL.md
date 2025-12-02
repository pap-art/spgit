# Installation Guide

Complete installation instructions for spgit.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Spotify account
- Spotify Developer App credentials

## Method 1: Install from PyPI (Recommended)

Once published to PyPI:

```bash
pip install spgit
```

Verify installation:

```bash
spgit --version
```

## Method 2: Install from Source

### Clone Repository

```bash
git clone https://github.com/yourusername/spgit.git
cd spgit
```

### Install in Development Mode

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .
```

### Install in Production Mode

```bash
pip install .
```

## Method 3: Install with pip from GitHub

```bash
pip install git+https://github.com/yourusername/spgit.git
```

## Post-Installation Setup

### 1. Create Spotify Developer App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **"Create an App"**
4. Fill in:
   - **App name**: spgit (or any name)
   - **App description**: Version control for playlists
   - **Redirect URI**: `http://localhost:8888/callback`
5. Accept terms and click **Create**
6. Note your **Client ID** and **Client Secret**

### 2. Configure spgit

Run the configuration wizard:

```bash
spgit config --global
```

Enter your credentials when prompted:
```
Enter your Spotify Client ID: YOUR_CLIENT_ID
Enter your Spotify Client Secret: YOUR_CLIENT_SECRET
```

Or set manually:

```bash
spgit config --global --set spotify.client_id YOUR_CLIENT_ID
spgit config --global --set spotify.client_secret YOUR_CLIENT_SECRET
```

### 3. Test Installation

```bash
# Check version
spgit --version

# View help
spgit --help

# Try initializing a test repo
mkdir test-playlist
cd test-playlist
spgit init --name "Test Playlist"
```

## Platform-Specific Instructions

### Windows

```powershell
# Install Python from python.org
# Open PowerShell or Command Prompt

# Install spgit
pip install spgit

# Configure
spgit config --global
```

**Note**: Windows may require enabling ANSI color support. spgit handles this automatically.

### macOS

```bash
# Install Python (if not already installed)
brew install python3

# Install spgit
pip3 install spgit

# Configure
spgit config --global
```

### Linux

```bash
# Python is usually pre-installed
# If not:
sudo apt-get install python3 python3-pip  # Debian/Ubuntu
sudo yum install python3 python3-pip      # CentOS/RHEL
sudo dnf install python3 python3-pip      # Fedora

# Install spgit
pip3 install spgit

# Configure
spgit config --global
```

## Development Installation

For contributing to spgit:

```bash
# Clone repository
git clone https://github.com/yourusername/spgit.git
cd spgit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black spgit/

# Lint
flake8 spgit/

# Type check
mypy spgit/
```

## Troubleshooting

### Command Not Found

If `spgit` command is not found after installation:

1. **Check if pip installed to user directory**:
   ```bash
   pip install --user spgit
   ```

2. **Add to PATH** (if user install):
   - **Linux/macOS**: Add to `~/.bashrc` or `~/.zshrc`:
     ```bash
     export PATH="$HOME/.local/bin:$PATH"
     ```
   - **Windows**: Add `%APPDATA%\Python\Python3X\Scripts` to PATH

3. **Use python -m**:
   ```bash
   python -m spgit --version
   ```

### Permission Errors

**Linux/macOS**:
```bash
pip install --user spgit
```

Or use virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate
pip install spgit
```

**Windows**:
Run as administrator or use:
```bash
pip install --user spgit
```

### Dependency Issues

If spotipy fails to install:

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies manually
pip install spotipy

# Then install spgit
pip install spgit
```

### SSL Certificate Errors

```bash
# Upgrade certifi
pip install --upgrade certifi

# Or disable SSL verification (not recommended)
export PYTHONHTTPSVERIFY=0  # Linux/macOS
set PYTHONHTTPSVERIFY=0     # Windows
```

### Python Version Issues

Check Python version:
```bash
python --version
```

spgit requires Python 3.8+. If you have an older version:

**Linux**:
```bash
sudo apt-get install python3.8
python3.8 -m pip install spgit
```

**macOS**:
```bash
brew install python@3.8
python3.8 -m pip install spgit
```

**Windows**:
Download from [python.org](https://www.python.org/downloads/)

## Uninstallation

```bash
pip uninstall spgit
```

Clean up configuration:
```bash
rm -rf ~/.spgit
```

## Upgrading

```bash
# From PyPI
pip install --upgrade spgit

# From source
cd spgit
git pull
pip install --upgrade .
```

## Verify Installation

Run verification script:

```bash
# Check version
spgit --version

# Check help
spgit --help

# Check config
spgit config --list

# Create test repo
mkdir /tmp/spgit-test
cd /tmp/spgit-test
spgit init
ls -la .spgit
```

Expected output:
```
.spgit/
├── HEAD
├── config
├── index
├── objects/
├── refs/
│   ├── heads/
│   ├── tags/
│   └── remotes/
└── logs/
```

## Docker Installation (Optional)

Create Dockerfile:

```dockerfile
FROM python:3.11-slim

RUN pip install spgit

WORKDIR /workspace

CMD ["spgit", "--help"]
```

Build and run:

```bash
docker build -t spgit .
docker run -it -v $(pwd):/workspace spgit
```

## Next Steps

After installation:

1. Read [QUICKSTART.md](QUICKSTART.md) for basic usage
2. Check [README.md](README.md) for complete documentation
3. Try [EXAMPLES.md](EXAMPLES.md) for workflow examples
4. Join community discussions
5. Report issues on GitHub

## Getting Help

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/spgit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/spgit/discussions)

## Support

If you encounter issues not covered here:

1. Check GitHub Issues
2. Enable debug mode: `export SPGIT_DEBUG=1`
3. Run with verbose output
4. Report with:
   - OS and version
   - Python version
   - spgit version
   - Full error message
   - Steps to reproduce
