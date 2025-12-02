"""status command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit, get_commit_tree
from ..utils.colors import success, error, branch, added, removed, modified, untracked, bold


def status_command(args):
    """Show working tree status."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Get current branch
        current_branch = repo.get_current_branch()
        head_commit = repo.get_head_commit()

        # Show branch info
        if current_branch:
            print(f"On branch {branch(current_branch)}")
        else:
            print(f"HEAD detached at {head_commit[:7] if head_commit else 'unknown'}")

        # Get HEAD commit tracks
        head_tracks = {}
        if head_commit:
            head_tracks = get_commit_tree(repo, head_commit)

        # Get index (staged) tracks
        index = repo.read_index()
        staged_tracks = {}
        if "tracks" in index:
            from ..core.objects import Track
            staged_tracks = {uri: Track.from_dict(data) for uri, data in index["tracks"].items()}

        # Compare HEAD to index
        staged_added = set(staged_tracks.keys()) - set(head_tracks.keys())
        staged_removed = set(head_tracks.keys()) - set(staged_tracks.keys())
        staged_modified = {uri for uri in staged_tracks.keys() & head_tracks.keys()
                          if staged_tracks[uri] != head_tracks[uri]}

        has_staged = staged_added or staged_removed or staged_modified

        # Show staged changes
        if has_staged:
            print()
            print(bold("Changes to be committed:"))
            print(f"  (use \"spgit reset HEAD <track>...\" to unstage)")
            print()
            for uri in sorted(staged_added):
                track = staged_tracks[uri]
                print(f"  {added('new track:')}   {track.name} - {track.artist}")
            for uri in sorted(staged_removed):
                track = head_tracks[uri]
                print(f"  {removed('deleted:')}    {track.name} - {track.artist}")
            for uri in sorted(staged_modified):
                track = staged_tracks[uri]
                print(f"  {modified('modified:')}   {track.name} - {track.artist}")

        if not has_staged:
            print()
            if head_commit:
                print("nothing to commit, working tree clean")
            else:
                print("No commits yet")

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
