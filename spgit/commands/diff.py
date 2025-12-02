"""diff command implementation"""

from ..core.repository import find_repository
from ..core.objects import get_commit_tree, Track
from ..utils.colors import error, added, removed, bold, green, red


def diff_command(args):
    """Show differences between commits, commit and working tree, etc."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        staged = hasattr(args, 'staged') and args.staged

        # Get HEAD commit tracks
        head_commit = repo.get_head_commit()
        head_tracks = {}
        if head_commit:
            head_tracks = get_commit_tree(repo, head_commit)

        if staged:
            # Show diff between HEAD and index (staged changes)
            index = repo.read_index()
            staged_tracks = {}
            if "tracks" in index:
                staged_tracks = {uri: Track.from_dict(data) for uri, data in index["tracks"].items()}

            _show_diff(head_tracks, staged_tracks)
        else:
            # Show diff between index and working tree (would need Spotify fetch)
            # For now, show staged vs HEAD
            index = repo.read_index()
            staged_tracks = {}
            if "tracks" in index:
                staged_tracks = {uri: Track.from_dict(data) for uri, data in index["tracks"].items()}

            _show_diff(head_tracks, staged_tracks)

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1


def _show_diff(old_tracks, new_tracks):
    """Show differences between two track sets."""
    added_uris = set(new_tracks.keys()) - set(old_tracks.keys())
    removed_uris = set(old_tracks.keys()) - set(new_tracks.keys())

    if not added_uris and not removed_uris:
        print("No changes")
        return

    if added_uris:
        print(bold(green("Added tracks:")))
        for uri in sorted(added_uris):
            track = new_tracks[uri]
            print(added(f"  + {track.name} - {track.artist}"))
        print()

    if removed_uris:
        print(bold(red("Removed tracks:")))
        for uri in sorted(removed_uris):
            track = old_tracks[uri]
            print(removed(f"  - {track.name} - {track.artist}"))
        print()
