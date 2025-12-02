# spgit - Git for Spotify Playlists

**spgit** is a complete command-line version control system for Spotify playlists that works exactly like git. Track changes, create branches, merge playlists, and collaborate on your music collection with the familiar git workflow.

## Features

- **Complete Git Parity**: All essential git commands work with Spotify playlists
- **Version Control**: Track every change to your playlists with commits
- **Branching**: Create experimental playlist variations without affecting the main version
- **Merging**: Combine playlists intelligently with multiple merge strategies
- **Collaboration**: Share and synchronize playlists with others
- **History**: View complete timeline of all changes
- **Fast**: Optimized for performance with efficient caching and batching

## Installation

### Via pip (Recommended)

```bash
pip install spgit
```

### From Source

```bash
git clone https://github.com/yourusername/spgit.git
cd spgit
pip install -e .
```

## Quick Start

### 1. Configure Spotify API Credentials

First, create a Spotify app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard):

1. Log in with your Spotify account
2. Click "Create an App"
3. Note your Client ID and Client Secret

Configure spgit:

```bash
spgit config --global
# Enter your Client ID and Client Secret when prompted
```

### 2. Clone a Playlist

```bash
spgit clone https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
cd "Today's Top Hits"
```

### 3. Make Changes

Edit your playlist in the Spotify app, then:

```bash
spgit add .
spgit commit -m "Added some new tracks"
spgit push
```

### 4. Create Branches

```bash
# Create a workout variation
spgit checkout -b workout-mix
# Edit playlist in Spotify
spgit add .
spgit commit -m "Made it more energetic"

# Switch back to main
spgit checkout main

# Merge changes
spgit merge workout-mix
```

## Command Reference

### Repository Management

#### `spgit init [--name NAME]`
Initialize a new repository in the current directory.

```bash
spgit init --name "My Playlist"
```

#### `spgit clone <url> [directory]`
Clone a Spotify playlist.

```bash
spgit clone https://open.spotify.com/playlist/xyz
spgit clone https://open.spotify.com/playlist/xyz my-playlist
```

#### `spgit config [--global] [--set KEY VALUE]`
Configure spgit settings.

```bash
# Interactive setup
spgit config --global

# Set specific values
spgit config --set spotify.client_id YOUR_ID
spgit config --set spotify.client_secret YOUR_SECRET

# List configuration
spgit config --list

# Get specific value
spgit config --get spotify.client_id
```

### Working with Changes

#### `spgit status`
Show the working tree status.

```bash
spgit status
```

#### `spgit add <files>` or `spgit add .` or `spgit add --all`

Add tracks to the staging area.

```bash
# Add all changes from Spotify
spgit add .
# Or
spgit add --all
spgit add -a

# Add specific track URIs
spgit add spotify:track:xyz
```

#### `spgit diff [--staged]`
Show changes between commits, commit and working tree, etc.

```bash
# Show unstaged changes
spgit diff

# Show staged changes
spgit diff --staged
```

#### `spgit commit -m "message"`
Record changes to the repository.

```bash
spgit commit -m "Added workout tracks"
```

### Viewing History

#### `spgit log [--oneline] [--graph] [-n LIMIT]`
Show commit logs.

```bash
# Full log
spgit log

# Concise view
spgit log --oneline

# With graph
spgit log --graph --oneline

# Limit entries
spgit log -n 10
```

#### `spgit show [commit]`
Show commit details and tracks.

```bash
spgit show
spgit show abc123
```

#### `spgit blame <track-uri>`
Show when a track was added and by whom.

```bash
spgit blame spotify:track:xyz
```

#### `spgit reflog [ref]`
Show reference logs (history of HEAD movements).

```bash
spgit reflog
spgit reflog main
```

### Branching

#### `spgit branch [name]` or `spgit branch -d <name>`
List, create, or delete branches.

```bash
# List branches
spgit branch

# Create branch
spgit branch chill-vibes

# Delete branch
spgit branch -d chill-vibes
```

#### `spgit checkout <branch>` or `spgit checkout -b <name>`
Switch branches or restore working tree files.

```bash
# Switch to existing branch
spgit checkout main

# Create and switch to new branch
spgit checkout -b experimental

# Checkout specific commit (detached HEAD)
spgit checkout abc123
```

### Merging and Rebasing

#### `spgit merge <branch> [--strategy STRATEGY]`
Merge branches together.

```bash
# Default merge (union)
spgit merge feature-branch

# Merge with specific strategy
spgit merge feature-branch --strategy append
spgit merge feature-branch --strategy intersection
spgit merge feature-branch --strategy union
```

**Merge Strategies:**
- `union` - Combine all unique tracks from both branches (default)
- `append` - Add tracks from merge branch to end of current branch
- `intersection` - Keep only tracks that exist in both branches

#### `spgit rebase <branch>`
Reapply commits on top of another branch.

```bash
spgit rebase main
```

#### `spgit cherry-pick <commit>`
Apply changes from a specific commit.

```bash
spgit cherry-pick abc123
```

### Remote Operations

#### `spgit remote [-v] [--add NAME URL] [--remove NAME]`
Manage remotes.

```bash
# List remotes
spgit remote

# List with URLs
spgit remote -v

# Add remote
spgit remote --add origin https://open.spotify.com/playlist/xyz

# Remove remote
spgit remote --remove origin
```

#### `spgit fetch [remote]`
Download from Spotify without merging.

```bash
spgit fetch origin
```

#### `spgit pull [remote]`
Fetch from and merge with Spotify playlist.

```bash
spgit pull origin
```

#### `spgit push [remote]`
Update remote Spotify playlist.

```bash
spgit push origin
```

### Undoing Changes

#### `spgit reset [--soft|--mixed|--hard] <commit>`
Reset current HEAD to specified state.

```bash
# Keep changes staged
spgit reset --soft HEAD~1

# Keep changes unstaged (default)
spgit reset HEAD~1
spgit reset --mixed HEAD~1

# Discard all changes
spgit reset --hard HEAD~1
```

#### `spgit revert <commit>`
Create new commit that undoes a previous commit.

```bash
spgit revert abc123
```

### Stashing

#### `spgit stash [save|list|pop|apply|drop]`
Temporarily save changes.

```bash
# Save changes
spgit stash
spgit stash save -m "Work in progress"

# List stashes
spgit stash list

# Apply and remove most recent stash
spgit stash pop

# Apply without removing
spgit stash apply
spgit stash apply stash@{0}

# Remove stash
spgit stash drop stash@{0}
```

### Tagging

#### `spgit tag [name] [commit]` or `spgit tag -d <name>`
Create, list, or delete tags.

```bash
# List tags
spgit tag

# Create tag
spgit tag v1.0

# Create tag on specific commit
spgit tag v1.0 abc123

# Delete tag
spgit tag -d v1.0
```

## Advanced Usage

### .spgitignore

Create a `.spgitignore` file to ignore specific track patterns:

```
# Ignore all tracks from a specific artist
spotify:artist:xyz*

# Ignore specific tracks
spotify:track:abc123
spotify:track:def456
```

### Workflow Examples

#### Collaborative Playlist Management

```bash
# Clone shared playlist
spgit clone https://open.spotify.com/playlist/shared

# Fetch latest changes
spgit pull

# Make your changes in Spotify
spgit add .
spgit commit -m "Added my favorite tracks"

# Push changes
spgit push
```

#### Experimental Variations

```bash
# Create experimental branch
spgit checkout -b party-mix

# Modify playlist in Spotify
spgit add .
spgit commit -m "Made it more upbeat"

# Test it out, then merge if you like it
spgit checkout main
spgit merge party-mix

# Or discard if you don't
spgit branch -d party-mix
```

#### Reverting Unwanted Changes

```bash
# View history
spgit log --oneline

# Revert specific commit
spgit revert abc123

# Or reset to previous state
spgit reset --hard HEAD~3
```

#### Time Travel

```bash
# View old versions
spgit checkout abc123

# Return to present
spgit checkout main
```

## Architecture

### Storage Structure

spgit uses a git-like storage structure:

```
.spgit/
├── HEAD           # Current branch pointer
├── config         # Repository configuration
├── index          # Staging area
├── objects/       # Commits and trees (SHA-1 hashes)
│   └── ab/
│       └── cdef123...
├── refs/
│   ├── heads/     # Branch pointers
│   │   ├── main
│   │   └── feature
│   ├── tags/      # Tag pointers
│   └── remotes/   # Remote branch pointers
└── logs/          # Reflog
    ├── HEAD
    └── refs/
        └── heads/
```

### Data Model

- **Tracks**: Stored as blob objects with metadata (name, artist, album, URI, duration)
- **Trees**: Collections of tracks (playlist snapshots)
- **Commits**: Immutable snapshots with parent links and metadata
- **Branches**: Pointers to commits
- **Remotes**: Links to Spotify playlist URLs

### Performance Optimizations

- SHA-1 hashing for efficient object storage
- zlib compression for objects
- Batch API requests (100 tracks per request)
- Local caching of Spotify authentication
- Fast-forward merges when possible

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:

```bash
# Reconfigure credentials
spgit config --global

# Clear cache
rm -rf ~/.spgit/.cache-spotipy
```

### Rate Limiting

Spotify API has rate limits. If you hit them:
- Wait a few minutes before retrying
- Reduce frequency of push/pull operations
- Use batching with `add .` instead of individual tracks

### Merge Conflicts

spgit uses automatic merge strategies. If the result isn't what you want:

```bash
# Undo merge
spgit reset --hard HEAD~1

# Try different strategy
spgit merge branch-name --strategy intersection
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=spgit --cov-report=html
```

### Code Style

```bash
# Format code
black spgit/

# Lint
flake8 spgit/

# Type checking
mypy spgit/
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Credits

- Built with [spotipy](https://spotipy.readthedocs.io/) for Spotify API access
- Inspired by [git](https://git-scm.com/)

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/spgit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/spgit/discussions)

## Changelog

### v1.0.0 (2024-12-02)

- Initial release
- Complete git command parity
- Support for all major git operations
- Spotify Web API integration
- Three-way merge algorithm
- Reflog support
- Color-coded output
- Production-ready and fully tested
