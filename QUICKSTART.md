# spgit Quick Start Guide

Get started with spgit in 5 minutes!

## Installation

```bash
pip install spgit
```

## Setup Spotify API (One-time)

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in and click "Create an App"
3. Note your **Client ID** and **Client Secret**
4. Run:

```bash
spgit config --global
# Paste your Client ID and Client Secret when prompted
```

## Basic Usage

### Clone a Playlist

```bash
# Copy playlist URL from Spotify
spgit clone https://open.spotify.com/playlist/YOUR_PLAYLIST_ID
cd "Playlist Name"
```

### Make Changes

1. Open Spotify and edit your playlist (add/remove tracks)
2. Save changes to spgit:

```bash
spgit add .
spgit commit -m "Added workout tracks"
```

### View History

```bash
spgit log --oneline
```

### Push to Spotify

```bash
spgit push
```

## Creating Branches

```bash
# Create a variation
spgit checkout -b party-mix

# Edit in Spotify app
spgit add .
spgit commit -m "Made it more upbeat"

# Switch back
spgit checkout main

# Merge if you like it
spgit merge party-mix
```

## Common Commands

| Command | Description |
|---------|-------------|
| `spgit clone <url>` | Clone a playlist |
| `spgit status` | Show changes |
| `spgit add .` | Stage all changes |
| `spgit commit -m "msg"` | Save changes |
| `spgit log` | View history |
| `spgit branch` | List branches |
| `spgit checkout <name>` | Switch branches |
| `spgit merge <branch>` | Merge branches |
| `spgit push` | Upload to Spotify |
| `spgit pull` | Download from Spotify |

## Help

```bash
spgit --help
spgit <command> --help
```

## Next Steps

- Read [README.md](README.md) for complete documentation
- Check [EXAMPLES.md](EXAMPLES.md) for workflows
- Report issues on GitHub

## Tips

- Commit frequently to track changes
- Use branches for experiments
- Pull before making changes to avoid conflicts
- Use `spgit log --oneline` for quick history view

Happy playlist versioning! 🎵
