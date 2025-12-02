"""push command implementation"""

from ..core.repository import find_repository
from ..core.spotify import get_spotify_client
from ..core.objects import get_commit_tree
from ..utils.colors import error, success, info


def push_command(args):
    """Update remote Spotify playlist."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        remote = args.remote if hasattr(args, 'remote') and args.remote else "origin"

        # Get remote URL
        remote_url = repo.get_remote_url(remote)
        if not remote_url:
            print(error(f"Remote '{remote}' not found"))
            return 1

        # Get current branch
        current_branch = repo.get_current_branch()
        if not current_branch:
            print(error("Fatal: cannot push from detached HEAD state"))
            return 1

        head_commit = repo.get_head_commit()
        if not head_commit:
            print(error("Fatal: no commits to push"))
            return 1

        print(info(f"Pushing to {remote}..."))

        # Get tracks from HEAD commit
        tracks = get_commit_tree(repo, head_commit)
        track_list = list(tracks.values())

        # Push to Spotify
        sp = get_spotify_client(repo)
        playlist_id = sp.get_playlist_id(remote_url)
        sp.update_playlist(playlist_id, track_list)

        print(info(f"Pushed {len(track_list)} tracks"))
        print(success(f"Successfully pushed to {remote}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
