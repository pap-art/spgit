"""add command implementation"""

from ..core.repository import find_repository
from ..core.spotify import get_spotify_client
from ..core.objects import Track
from ..utils.colors import success, error, info


def add_command(args):
    """Add tracks to staging area."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Get current index
        index = repo.read_index()
        staged_tracks = index.get("tracks", {})

        # Check if --all flag or "." in files
        add_all = (hasattr(args, 'all') and args.all) or (hasattr(args, 'files') and '.' in args.files)

        if add_all:
            # Add all tracks from Spotify
            print(info("Fetching current playlist state from Spotify..."))

            config = repo.read_config()
            playlist_id = config.get("playlist", {}).get("id")

            if not playlist_id:
                print(error("No playlist ID configured. Use 'spgit clone' or configure manually."))
                return 1

            sp = get_spotify_client(repo)
            tracks = sp.get_playlist_tracks(playlist_id)

            # Compare with current staging area to show what changed
            old_uris = set(staged_tracks.keys())
            new_uris = {track.uri for track in tracks}

            added_uris = new_uris - old_uris
            removed_uris = old_uris - new_uris

            # Update staged tracks
            new_staged_tracks = {track.uri: track.to_dict() for track in tracks}

            # Show what changed
            if added_uris or removed_uris:
                if added_uris:
                    print(info(f"Added {len(added_uris)} track(s)"))
                    for uri in list(added_uris)[:5]:  # Show first 5
                        track_dict = new_staged_tracks[uri]
                        from ..utils.colors import added as added_color
                        print(f"  {added_color('+')} {track_dict['name']} - {track_dict['artist']}")
                    if len(added_uris) > 5:
                        print(f"  ... and {len(added_uris) - 5} more")

                if removed_uris:
                    print(info(f"Removed {len(removed_uris)} track(s)"))
                    for uri in list(removed_uris)[:5]:  # Show first 5
                        track_dict = staged_tracks[uri]
                        from ..utils.colors import removed as removed_color
                        print(f"  {removed_color('-')} {track_dict['name']} - {track_dict['artist']}")
                    if len(removed_uris) > 5:
                        print(f"  ... and {len(removed_uris) - 5} more")
            else:
                print(info(f"No changes ({len(tracks)} tracks)"))

            staged_tracks = new_staged_tracks

        elif hasattr(args, 'files') and args.files:
            # Add specific track URIs
            for uri in args.files:
                if not uri.startswith("spotify:track:"):
                    print(error(f"Invalid track URI: {uri}"))
                    continue

                # Fetch track info from Spotify
                sp = get_spotify_client(repo)
                tracks = sp.search_track(uri, limit=1)

                if tracks:
                    track = tracks[0]
                    staged_tracks[track.uri] = track.to_dict()
                    print(info(f"Added: {track.name} - {track.artist}"))

        # Update index
        from ..core.objects import create_tree_from_tracks, Track as TrackObj
        track_objects = [TrackObj.from_dict(data) for data in staged_tracks.values()]
        tree = create_tree_from_tracks(repo, track_objects)

        index["tree"] = tree
        index["tracks"] = staged_tracks
        repo.update_index(index)

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
