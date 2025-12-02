"""blame command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit, get_commit_history, get_commit_tree
from ..utils.colors import error, info, gray
from ..utils.helpers import format_timestamp


def blame_command(args):
    """Show when each track was added."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        track_uri = args.track if hasattr(args, 'track') and args.track else None

        if not track_uri:
            print(error("Fatal: no track URI specified"))
            return 1

        head_commit = repo.get_head_commit()
        if not head_commit:
            print(error("Fatal: no commits yet"))
            return 1

        # Find when track was added
        history = get_commit_history(repo, head_commit)

        for commit_hash in reversed(history):
            try:
                commit = read_object(repo, commit_hash)
                if not isinstance(commit, Commit):
                    continue

                tracks = get_commit_tree(repo, commit_hash)

                if track_uri in tracks:
                    track = tracks[track_uri]
                    print(f"{commit_hash[:7]} ({format_timestamp(commit.timestamp)}) {track.name} - {track.artist}")
                    print(f"  Added by: {commit.author}")
                    print(f"  Message: {commit.message.split(chr(10))[0]}")
                    return 0

            except ValueError:
                continue

        print(error(f"Track '{track_uri}' not found in history"))
        return 1

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
