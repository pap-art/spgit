"""compare command implementation"""

from ..core.repository import find_repository
from ..core.spotify import get_spotify_client
from ..core.objects import Track, get_commit_tree
from ..utils.colors import success, error, info, added, removed, bold


def compare_command(args):
    """
    Compare current playlist with upstream or another remote.
    Shows tracks that differ between your fork and the original.
    """
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Determine what to compare with
        remote = args.remote if hasattr(args, 'remote') and args.remote else "upstream"

        # Get remote URL
        remote_url = repo.get_remote_url(remote)
        if not remote_url:
            print(error(f"Remote '{remote}' not found"))
            print(info("Available remotes:"))
            remotes = repo.list_remotes()
            for name, url in remotes.items():
                print(f"  {name}: {url}")
            return 1

        print(info(f"Comparing with {remote}..."))

        # Get current playlist tracks
        config = repo.read_config()
        current_playlist_id = config.get("playlist", {}).get("id")

        if not current_playlist_id:
            print(error("No playlist ID configured"))
            return 1

        sp = get_spotify_client(repo)

        print(info("Fetching your playlist..."))
        current_tracks = sp.get_playlist_tracks(current_playlist_id)
        current_uris = {track.uri: track for track in current_tracks}

        # Get upstream playlist tracks
        print(info(f"Fetching {remote} playlist..."))
        upstream_playlist_id = sp.get_playlist_id(remote_url)
        upstream_tracks = sp.get_playlist_tracks(upstream_playlist_id)
        upstream_uris = {track.uri: track for track in upstream_tracks}

        # Calculate differences
        only_in_yours = set(current_uris.keys()) - set(upstream_uris.keys())
        only_in_upstream = set(upstream_uris.keys()) - set(current_uris.keys())
        in_both = set(current_uris.keys()) & set(upstream_uris.keys())

        # Display results
        print()
        print(bold("═" * 60))
        print(bold(f"Comparison: YOUR PLAYLIST vs {remote.upper()}"))
        print(bold("═" * 60))
        print()

        print(f"Your playlist:      {len(current_tracks)} tracks")
        print(f"{remote.capitalize()} playlist:     {len(upstream_tracks)} tracks")
        print(f"Tracks in common:   {len(in_both)} tracks")
        print()

        if only_in_yours:
            print(bold(added(f"✓ Tracks ONLY in yours ({len(only_in_yours)}):")))
            for uri in sorted(only_in_yours)[:10]:  # Show first 10
                track = current_uris[uri]
                print(f"  {added('+')} {track.name} - {track.artist}")
            if len(only_in_yours) > 10:
                print(f"  {added('...')} and {len(only_in_yours) - 10} more")
            print()

        if only_in_upstream:
            print(bold(removed(f"✗ Tracks ONLY in {remote} ({len(only_in_upstream)}):")))
            for uri in sorted(only_in_upstream)[:10]:  # Show first 10
                track = upstream_uris[uri]
                print(f"  {removed('-')} {track.name} - {track.artist}")
            if len(only_in_upstream) > 10:
                print(f"  {removed('...')} and {len(only_in_upstream) - 10} more")
            print()

        if not only_in_yours and not only_in_upstream:
            print(success("✓ Playlists are identical!"))
            print()

        # Summary
        print(bold("Summary:"))
        if only_in_yours:
            print(added(f"  You have {len(only_in_yours)} unique track(s)"))
        if only_in_upstream:
            print(removed(f"  {remote.capitalize()} has {len(only_in_upstream)} track(s) you don't have"))
        if not only_in_yours and not only_in_upstream:
            print(success("  No differences - playlists are in sync!"))

        print()
        print(bold("═" * 60))

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
