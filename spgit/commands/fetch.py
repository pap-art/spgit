"""fetch command implementation"""

from ..core.repository import find_repository
from ..core.spotify import get_spotify_client
from ..utils.colors import error, success, info


def fetch_command(args):
    """Download from Spotify without merging."""
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

        print(info(f"Fetching from {remote}..."))

        # Fetch from Spotify
        sp = get_spotify_client(repo)
        playlist_id = sp.get_playlist_id(remote_url)
        tracks = sp.get_playlist_tracks(playlist_id)

        print(info(f"Received {len(tracks)} tracks"))
        print(success(f"Successfully fetched from {remote}"))
        print(info("Run 'spgit merge' to merge changes"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
