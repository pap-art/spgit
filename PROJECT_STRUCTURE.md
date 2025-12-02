# spgit Project Structure

Complete overview of the spgit codebase.

## Directory Layout

```
spgit/
├── spgit/                      # Main package
│   ├── __init__.py            # Package initialization
│   ├── __main__.py            # Module entry point (python -m spgit)
│   ├── cli.py                 # Command-line interface and argument parsing
│   │
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── repository.py      # Repository management (.spgit structure)
│   │   ├── objects.py         # Object database (SHA-1, commits, trees, blobs)
│   │   └── spotify.py         # Spotify API integration
│   │
│   ├── commands/              # Command implementations
│   │   ├── __init__.py
│   │   ├── init.py           # Initialize repository
│   │   ├── clone.py          # Clone playlist
│   │   ├── config.py         # Configuration management
│   │   ├── add.py            # Stage changes
│   │   ├── commit.py         # Create commits
│   │   ├── status.py         # Show status
│   │   ├── diff.py           # Show differences
│   │   ├── log.py            # Show history
│   │   ├── branch.py         # Branch operations
│   │   ├── checkout.py       # Switch branches
│   │   ├── merge.py          # Merge branches
│   │   ├── pull.py           # Fetch and merge
│   │   ├── push.py           # Upload to Spotify
│   │   ├── fetch.py          # Download from Spotify
│   │   ├── remote.py         # Remote management
│   │   ├── reset.py          # Reset commits
│   │   ├── revert.py         # Revert commits
│   │   ├── stash.py          # Stash changes
│   │   ├── tag.py            # Tag management
│   │   ├── show.py           # Show commit details
│   │   ├── cherrypick.py     # Cherry-pick commits
│   │   ├── rebase.py         # Rebase branches
│   │   ├── blame.py          # Track history
│   │   └── reflog.py         # Reference logs
│   │
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── colors.py          # Color output
│       └── helpers.py         # Helper functions
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration
│   ├── test_repository.py    # Repository tests
│   ├── test_objects.py       # Object database tests
│   └── test_utils.py         # Utility tests
│
├── setup.py                   # Setup script (legacy)
├── pyproject.toml            # Modern Python project configuration
├── requirements.txt          # Dependencies
├── MANIFEST.in              # Package manifest
│
├── README.md                 # Main documentation
├── QUICKSTART.md            # Quick start guide
├── EXAMPLES.md              # Usage examples
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
└── PROJECT_STRUCTURE.md    # This file
```

## Core Components

### 1. Repository Management (core/repository.py)

**Purpose**: Manages the .spgit directory structure and repository operations.

**Key Classes**:
- `Repository`: Main repository class
  - Initializes .spgit structure
  - Manages HEAD, refs, and config
  - Provides branch operations
  - Handles index (staging area)

**Key Functions**:
- `init()`: Create new repository
- `find_repository()`: Find repo in parent dirs
- Branch management (create, delete, checkout)
- Config management (read, write, update)
- Remote management (add, remove, list)

### 2. Object Database (core/objects.py)

**Purpose**: Implements git-like object storage with SHA-1 hashing.

**Key Classes**:
- `Track`: Represents a Spotify track
- `Blob`: Stores track data
- `Tree`: Collection of tracks
- `Commit`: Immutable snapshot with metadata

**Key Functions**:
- `write_object()`: Store object with SHA-1 hash
- `read_object()`: Retrieve object by hash
- `create_tree_from_tracks()`: Build tree from tracks
- `get_commit_tree()`: Extract tracks from commit
- `find_common_ancestor()`: Find merge base

**Storage**:
- Objects compressed with zlib
- Stored in `.spgit/objects/ab/cdef...`
- SHA-1 hash ensures integrity

### 3. Spotify Integration (core/spotify.py)

**Purpose**: Interfaces with Spotify Web API.

**Key Classes**:
- `SpotifyClient`: Wrapper for spotipy
  - Authentication handling
  - Playlist operations (get, create, update)
  - Track operations (add, remove, search)
  - Rate limiting

**Key Functions**:
- `get_spotify_client()`: Get authenticated client
- `get_playlist_tracks()`: Fetch all tracks
- `update_playlist()`: Replace all tracks
- `add_tracks()` / `remove_tracks()`: Modify playlist

### 4. Commands (commands/)

Each command is self-contained in its own file:

**Repository Setup**:
- `init`: Create new repository
- `clone`: Clone from Spotify
- `config`: Manage configuration

**Basic Operations**:
- `add`: Stage changes
- `commit`: Create commit
- `status`: Show working tree status
- `diff`: Show changes
- `log`: Show history

**Branching**:
- `branch`: List/create/delete branches
- `checkout`: Switch branches
- `merge`: Merge branches

**Remote Operations**:
- `remote`: Manage remotes
- `fetch`: Download from Spotify
- `pull`: Fetch and merge
- `push`: Upload to Spotify

**Advanced**:
- `reset`: Undo commits
- `revert`: Reverse commits
- `stash`: Temporary storage
- `tag`: Version marking
- `cherry-pick`: Apply specific commits
- `rebase`: Reapply commits
- `blame`: Track changes
- `reflog`: Reference history

### 5. Utilities (utils/)

**colors.py**:
- ANSI color codes
- Color output functions
- Git-like semantic colors
- Platform-specific handling (Windows)

**helpers.py**:
- Duration formatting
- Timestamp formatting
- Text truncation
- Table formatting
- .spgitignore support
- Pluralization

## Data Flow

### Clone Operation

```
1. User runs: spgit clone <url>
2. cli.py parses arguments
3. clone.py executes:
   - Initialize repository
   - Get Spotify client
   - Fetch tracks from API
   - Create tree from tracks
   - Create initial commit
   - Store in object database
   - Update refs/heads/main
4. Repository ready for use
```

### Commit Operation

```
1. User edits in Spotify app
2. User runs: spgit add .
3. add.py fetches current state
4. Stores in index (staging area)
5. User runs: spgit commit -m "message"
6. commit.py:
   - Reads index
   - Creates commit object
   - Writes to object database
   - Updates branch ref
   - Updates reflog
```

### Merge Operation

```
1. User runs: spgit merge branch-name
2. merge.py:
   - Gets current and merge commits
   - Finds common ancestor
   - Checks for fast-forward
   - Performs three-way merge
   - Applies merge strategy
   - Creates merge commit
   - Updates refs
```

## Key Algorithms

### SHA-1 Hashing

```python
def hash_object(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()
```

### Three-Way Merge

```python
def merge(base, current, merge, strategy):
    if strategy == 'union':
        return current ∪ merge
    elif strategy == 'append':
        return current + (merge - current)
    elif strategy == 'intersection':
        return current ∩ merge
```

### Common Ancestor

```python
def find_common_ancestor(commit1, commit2):
    history1 = get_history(commit1)
    history2 = get_history(commit2)
    return first(history2 where h in history1)
```

## Configuration

### Global Config
Location: `~/.spgit/config`

```json
{
  "spotify": {
    "client_id": "...",
    "client_secret": "..."
  }
}
```

### Repository Config
Location: `.spgit/config`

```json
{
  "core": {
    "repositoryformatversion": 0,
    "filemode": true,
    "bare": false
  },
  "playlist": {
    "name": "My Playlist",
    "id": "spotify_playlist_id"
  },
  "remote": {
    "origin": {
      "url": "https://open.spotify.com/playlist/..."
    }
  },
  "branch": {
    "main": {
      "remote": "origin",
      "merge": "refs/heads/main"
    }
  }
}
```

## Testing

### Test Structure

- `test_repository.py`: Repository operations
- `test_objects.py`: Object database
- `test_utils.py`: Utility functions

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=spgit --cov-report=html

# Specific test
pytest tests/test_repository.py::TestRepository::test_init_creates_structure
```

## Performance Considerations

### Optimizations

1. **Object Storage**:
   - zlib compression reduces disk usage
   - SHA-1 hashing ensures deduplication
   - Two-level directory structure (ab/cdef...)

2. **API Calls**:
   - Batch requests (100 tracks per call)
   - Rate limiting delays (0.1s between batches)
   - Local caching of auth tokens

3. **Memory**:
   - Streaming for large playlists
   - Lazy loading of objects
   - Minimal metadata in index

### Bottlenecks

- Spotify API rate limits (primary)
- Network latency
- Large playlist initial clone
- First-time authentication

## Extension Points

### Adding New Commands

1. Create `commands/newcommand.py`
2. Implement `newcommand_command(args)`
3. Add parser in `cli.py`
4. Add to commands dict in `cli.py`

### Custom Merge Strategies

Add to `commands/merge.py`:

```python
elif strategy == 'custom':
    # Implement custom logic
    return custom_merge(current_tracks, merge_tracks)
```

### Additional Metadata

Extend `Track` class in `core/objects.py`:

```python
class Track:
    def __init__(self, ..., new_field):
        self.new_field = new_field
```

## Dependencies

### Required

- `spotipy>=2.23.0`: Spotify API client
- Python 3.8+

### Development

- `pytest>=7.0.0`: Testing
- `pytest-cov>=4.0.0`: Coverage
- `black>=23.0.0`: Formatting
- `flake8>=6.0.0`: Linting
- `mypy>=1.0.0`: Type checking

## Future Enhancements

Potential additions:

1. **Performance**:
   - Parallel API requests
   - Delta compression
   - Object packing

2. **Features**:
   - Interactive rebase
   - Patch mode for add
   - Bisect for finding changes
   - Hooks for automation

3. **UI**:
   - TUI interface (textual)
   - Web interface
   - GUI application

4. **Collaboration**:
   - Git-like server protocol
   - Conflict resolution UI
   - Pull requests

## License

MIT License - See LICENSE file
