"""show command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit, get_commit_tree
from ..utils.colors import error, commit_hash, bold
from ..utils.helpers import format_timestamp


def show_command(args):
    """Show commit details."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        commit_ref = args.commit if hasattr(args, 'commit') and args.commit else repo.get_head_commit()

        if not commit_ref:
            print(error("Fatal: no commit specified"))
            return 1

        # Read commit
        try:
            commit = read_object(repo, commit_ref)
            if not isinstance(commit, Commit):
                print(error(f"'{commit_ref}' is not a commit"))
                return 1
        except ValueError:
            print(error(f"Commit '{commit_ref}' not found"))
            return 1

        # Display commit details
        print(commit_hash(f"commit {commit_ref}"))
        if len(commit.parents) > 1:
            print(f"Merge: {' '.join(p[:7] for p in commit.parents)}")
        print(f"Author: {commit.author}")
        print(f"Date:   {format_timestamp(commit.timestamp)}")
        print()
        for line in commit.message.split('\n'):
            print(f"    {line}")
        print()

        # Display tracks
        tracks = get_commit_tree(repo, commit_ref)
        print(bold(f"Tracks ({len(tracks)}):"))
        for uri, track in list(tracks.items())[:10]:  # Show first 10
            print(f"  {track.name} - {track.artist}")

        if len(tracks) > 10:
            print(f"  ... and {len(tracks) - 10} more")

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
