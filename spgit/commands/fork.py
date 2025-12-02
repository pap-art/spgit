"""fork command implementation"""

import os
from pathlib import Path
from ..core.repository import Repository
from ..core.spotify import get_spotify_client
from ..core.objects import create_tree_from_tracks, Commit, write_object
from ..utils.colors import success, error, info


def fork_command(args):
    """
    Fork a Spotify playlist - clone it and create your own copy.

    This command:
    1. Fetches the source playlist
    2. Creates a new playlist on your Spotify account
    3. Copies all tracks to your new playlist
    4. Sets up a local spgit repository
    """
    try:
        source_url = args.url
        new_name = args.name if hasattr(args, 'name') and args.name else None
        directory = args.directory if hasattr(args, 'directory') and args.directory else None

        print(info(f"Forking playlist from {source_url}..."))

        # Get Spotify client
        sp = get_spotify_client()

        # Extract source playlist ID
        source_playlist_id = sp.get_playlist_id(source_url)

        # Get source playlist info
        source_playlist = sp.get_playlist(source_playlist_id)
        source_name = source_playlist["name"]

        print(info(f"Source playlist: {source_name}"))

        # Determine new playlist name
        if not new_name:
            new_name = f"{source_name} (Fork)"

        print(info(f"Creating new playlist: {new_name}"))

        # Create new playlist on Spotify
        new_playlist_id = sp.create_playlist(
            name=new_name,
            description=f"Forked from {source_name}",
            public=False  # Private by default for safety
        )

        print(success(f"Created playlist on Spotify: {new_name}"))

        # Fetch tracks from source
        print(info(f"Fetching tracks from source..."))
        tracks = sp.get_playlist_tracks(source_playlist_id)

        print(info(f"Received {len(tracks)} tracks"))

        # Add tracks to new playlist
        if tracks:
            print(info(f"Copying {len(tracks)} tracks to new playlist..."))
            sp.add_tracks(new_playlist_id, tracks)
            print(success(f"Copied all tracks!"))

        # Determine directory name
        if not directory:
            directory = new_name.replace("/", "-").replace("\\", "-")

        target_dir = Path(directory).resolve()

        if target_dir.exists():
            print(error(f"Fatal: destination path '{directory}' already exists"))
            return 1

        # Create directory and initialize repository
        target_dir.mkdir(parents=True, exist_ok=True)
        os.chdir(target_dir)

        repo = Repository()

        # Manually initialize without calling init() to avoid double commit
        repo.spgit_dir.mkdir(parents=True, exist_ok=True)
        repo.objects_dir.mkdir(exist_ok=True)
        repo.refs_dir.mkdir(exist_ok=True)
        repo.heads_dir.mkdir(exist_ok=True)
        repo.tags_dir.mkdir(exist_ok=True)
        repo.remotes_dir.mkdir(exist_ok=True)
        repo.logs_dir.mkdir(exist_ok=True)
        (repo.logs_dir / "refs" / "heads").mkdir(parents=True, exist_ok=True)

        # Initialize HEAD to point to main branch
        repo.head_path.write_text("ref: refs/heads/main")

        # Get new playlist URL
        new_url = f"https://open.spotify.com/playlist/{new_playlist_id}"

        # Initialize config with all settings
        config = {
            "core": {
                "repositoryformatversion": 0,
                "filemode": True,
                "bare": False
            },
            "playlist": {
                "name": new_name,
                "id": new_playlist_id
            },
            "remote": {
                "origin": {"url": new_url},
                "upstream": {"url": source_url}
            },
            "branch": {
                "main": {
                    "remote": "origin",
                    "merge": "refs/heads/main"
                }
            }
        }
        repo._write_config(config)
        repo._write_index({})

        # Create tree from tracks
        tree = create_tree_from_tracks(repo, tracks)

        # Create commit
        commit = Commit(
            tree=tree,
            parent=None,
            message=f"Fork playlist '{source_name}' as '{new_name}'",
            author="spgit",
            committer="spgit"
        )
        commit_hash = write_object(repo, commit)

        # Update main branch
        repo._update_ref("refs/heads/main", commit_hash)
        repo._update_reflog("refs/heads/main", None, commit_hash, f"fork: from {source_url}")

        # Update index to match commit
        repo.update_index({"tree": tree, "tracks": {track.uri: track.to_dict() for track in tracks}})

        print()
        print(success(f"Successfully forked '{source_name}'!"))
        print(info(f"Your new playlist: {new_url}"))
        print(info(f"Local repository: {directory}"))
        print()
        print("Next steps:")
        print(f"  cd \"{directory}\"")
        print("  spgit status")
        print("  spgit log")
        print()
        print("To sync changes:")
        print("  Edit playlist in Spotify, then:")
        print("  spgit add .")
        print("  spgit commit -m \"Your changes\"")
        print("  spgit push")

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
