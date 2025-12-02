"""clone command implementation"""

import os
from pathlib import Path
from ..core.repository import Repository
from ..core.spotify import get_spotify_client
from ..core.objects import Track, create_tree_from_tracks, Commit, write_object
from ..utils.colors import success, error, info


def clone_command(args):
    """Clone a Spotify playlist."""
    try:
        url = args.url
        directory = args.directory if hasattr(args, 'directory') and args.directory else None

        print(info(f"Cloning playlist from {url}..."))

        # Get Spotify client
        sp = get_spotify_client()

        # Extract playlist ID
        playlist_id = sp.get_playlist_id(url)

        # Get playlist info
        playlist = sp.get_playlist(playlist_id)
        playlist_name = playlist["name"]

        print(info(f"Playlist: {playlist_name}"))

        # Determine directory name
        if not directory:
            # Sanitize playlist name for directory
            directory = playlist_name.replace("/", "-").replace("\\", "-")

        target_dir = Path(directory).resolve()

        if target_dir.exists():
            print(error(f"Fatal: destination path '{directory}' already exists"))
            return 1

        # Create directory and initialize repository
        target_dir.mkdir(parents=True, exist_ok=True)
        os.chdir(target_dir)

        repo = Repository()
        repo.init(playlist_name)

        # Store remote URL
        repo.add_remote("origin", url)
        repo.update_config("playlist", "id", playlist_id)

        # Fetch tracks
        print(info(f"Fetching tracks..."))
        tracks = sp.get_playlist_tracks(playlist_id)

        print(info(f"Received {len(tracks)} tracks"))

        # Create tree from tracks
        tree = create_tree_from_tracks(repo, tracks)

        # Create commit
        commit = Commit(
            tree=tree,
            parent=None,
            message=f"Clone playlist '{playlist_name}'",
            author="spgit",
            committer="spgit"
        )
        commit_hash = write_object(repo, commit)

        # Update main branch
        repo._update_ref("refs/heads/main", commit_hash)
        repo._update_reflog("refs/heads/main", None, commit_hash, f"clone: from {url}")

        # Set upstream
        repo.update_config("branch", "main", {"remote": "origin", "merge": "refs/heads/main"})

        # Update index to match commit
        repo.update_index({"tree": tree, "tracks": {track.uri: track.to_dict() for track in tracks}})

        print(success(f"Cloned '{playlist_name}' into '{directory}'"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
