# spgit Usage Examples

Comprehensive examples demonstrating spgit workflows.

## Basic Workflow

### Starting from Scratch

```bash
# Initialize new repository
mkdir my-playlist
cd my-playlist
spgit init --name "My Awesome Playlist"

# Create playlist on Spotify, then add tracks
spgit add .
spgit commit -m "Initial playlist"
```

### Cloning Existing Playlist

```bash
# Clone from Spotify
spgit clone https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
cd "Today's Top Hits"

# Make changes in Spotify app
spgit add .
spgit commit -m "Removed old tracks"
spgit push
```

## Branching Workflows

### Feature Branches

```bash
# Create workout variation
spgit checkout -b workout
# Edit in Spotify to make it more energetic
spgit add .
spgit commit -m "Increased tempo and energy"

# Create chill variation
spgit checkout main
spgit checkout -b chill
# Edit in Spotify to make it more relaxed
spgit add .
spgit commit -m "Made it more chill"

# Merge best of both
spgit checkout main
spgit merge workout --strategy append
spgit merge chill --strategy append
```

### Experimental Changes

```bash
# Experiment safely
spgit checkout -b experiment
# Make radical changes in Spotify
spgit add .
spgit commit -m "Experimental mix"

# Test it, then decide:

# If you like it:
spgit checkout main
spgit merge experiment

# If you don't:
spgit checkout main
spgit branch -d experiment
```

## Collaboration Workflows

### Team Playlist

```bash
# Team member 1: Clone shared playlist
spgit clone https://open.spotify.com/playlist/team-playlist
cd team-playlist

# Add your tracks
spgit add .
spgit commit -m "Added my recommendations"
spgit push

# Team member 2: Get updates
cd team-playlist
spgit pull
# Add more tracks
spgit add .
spgit commit -m "Added more variety"
spgit push
```

### Review Before Merging

```bash
# Create suggestion branch
spgit checkout -b suggestions

# Add tracks in Spotify
spgit add .
spgit commit -m "Suggested additions"

# Share with team (push to separate playlist)
# Team reviews, then maintainer merges:
spgit checkout main
spgit merge suggestions
spgit push
```

## Advanced Workflows

### Playlist Archaeology

```bash
# View history
spgit log --oneline

# Checkout old version
spgit checkout abc123

# Listen to it, then return to present
spgit checkout main

# Or restore old version permanently
spgit reset --hard abc123
```

### Cherry-Picking Tracks

```bash
# View branch differences
spgit log feature --oneline

# Pick specific good changes
spgit cherry-pick abc123
spgit cherry-pick def456
```

### Rebasing for Clean History

```bash
# Create feature branch
spgit checkout -b feature

# Make several commits
spgit commit -m "Add track 1"
spgit commit -m "Add track 2"
spgit commit -m "Add track 3"

# Rebase onto updated main
spgit checkout main
spgit pull
spgit checkout feature
spgit rebase main
```

### Stashing Work

```bash
# In middle of changes
spgit add .

# Need to switch branches urgently
spgit stash save -m "Work in progress"

# Do urgent work
spgit checkout hotfix
# Fix and commit
spgit checkout main

# Resume previous work
spgit stash pop
```

## Merge Strategy Examples

### Union Merge (Default)

Combines all unique tracks from both branches:

```bash
# Branch A: [track1, track2, track3]
# Branch B: [track2, track3, track4]
spgit merge branch-b
# Result: [track1, track2, track3, track4]
```

### Append Merge

Adds tracks from merge branch to end:

```bash
# Branch A: [track1, track2]
# Branch B: [track3, track4]
spgit merge branch-b --strategy append
# Result: [track1, track2, track3, track4]
```

### Intersection Merge

Keeps only common tracks:

```bash
# Branch A: [track1, track2, track3]
# Branch B: [track2, track3, track4]
spgit merge branch-b --strategy intersection
# Result: [track2, track3]
```

## Playlist Organization

### Genre-Based Branches

```bash
# Create genre branches
spgit checkout -b rock
# Add rock tracks
spgit commit -m "Rock collection"

spgit checkout main
spgit checkout -b electronic
# Add electronic tracks
spgit commit -m "Electronic collection"

# Create mixed playlist
spgit checkout main
spgit merge rock --strategy append
spgit merge electronic --strategy append
```

### Time-Based Snapshots

```bash
# Tag monthly versions
spgit tag january-2024
# Next month
spgit tag february-2024

# Compare months
spgit diff january-2024 february-2024

# Restore old version
spgit checkout january-2024
```

### Seasonal Playlists

```bash
# Create seasonal branches
spgit checkout -b summer
spgit checkout -b winter
spgit checkout -b spring
spgit checkout -b fall

# Rotate seasonally
spgit checkout main
spgit reset --hard summer  # In summer
spgit reset --hard winter  # In winter
```

## Automation Examples

### Backup Script

```bash
#!/bin/bash
# daily-backup.sh

cd ~/playlists/my-playlist
spgit add .
spgit commit -m "Daily backup $(date +%Y-%m-%d)"
spgit push
```

### Sync Multiple Playlists

```bash
#!/bin/bash
# sync-all.sh

for playlist in workout chill party; do
    cd ~/playlists/$playlist
    spgit pull
    spgit add .
    spgit commit -m "Auto-sync $(date)"
    spgit push
done
```

## Troubleshooting Examples

### Undo Last Commit

```bash
# Keep changes
spgit reset --soft HEAD~1

# Discard changes
spgit reset --hard HEAD~1
```

### Fix Wrong Branch

```bash
# Made changes on wrong branch
spgit stash
spgit checkout correct-branch
spgit stash pop
spgit commit -m "Fix: correct branch"
```

### Recover Deleted Branch

```bash
# View reflog
spgit reflog

# Find deleted branch commit
spgit checkout abc123
spgit checkout -b recovered-branch
```

### Clean Up Mistakes

```bash
# Remove last 3 commits
spgit reset --hard HEAD~3

# Undo specific commit
spgit revert abc123

# Start over from remote
spgit reset --hard origin/main
```

## Performance Tips

### Batch Operations

```bash
# Instead of multiple small commits
spgit add .
spgit commit -m "Multiple changes"

# Instead of:
# spgit add track1
# spgit commit -m "Add track1"
# spgit add track2
# spgit commit -m "Add track2"
```

### Efficient Pulls

```bash
# Pull less frequently for large playlists
# Use --no-verify if available (future feature)
```

## Integration Examples

### With GitHub Actions

```yaml
# .github/workflows/backup.yml
name: Backup Playlist
on:
  schedule:
    - cron: '0 0 * * *'  # Daily
jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Backup
        run: |
          spgit add .
          spgit commit -m "Auto backup"
          spgit push
```

### With Cron

```bash
# Add to crontab
0 0 * * * cd ~/playlists/my-playlist && spgit add . && spgit commit -m "Daily backup" && spgit push
```

## Tips and Tricks

### View Compact History

```bash
spgit log --oneline -10
```

### Find When Track Was Added

```bash
spgit blame spotify:track:xyz
```

### Compare Branches

```bash
spgit checkout main
spgit diff main..feature
```

### List All Tags

```bash
spgit tag | sort -V
```

### Clean Old Branches

```bash
# List branches
spgit branch

# Delete merged branches
spgit branch -d old-feature
```

### Alias Common Commands

```bash
# Add to ~/.bashrc or ~/.zshrc
alias spst='spgit status'
alias splog='spgit log --oneline'
alias spp='spgit pull'
alias sps='spgit push'
```
