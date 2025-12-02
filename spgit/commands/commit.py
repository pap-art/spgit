"""commit command implementation"""

from ..core.repository import find_repository
from ..core.objects import Commit, write_object
from ..utils.colors import success, error, info, branch as branch_color


def commit_command(args):
    """Create a new commit."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Get commit message
        if not hasattr(args, 'message') or not args.message:
            print(error("Fatal: no commit message provided. Use -m flag."))
            return 1

        message = args.message

        # Get current branch and HEAD
        current_branch = repo.get_current_branch()
        head_commit = repo.get_head_commit()

        if not current_branch:
            print(error("Fatal: cannot commit to detached HEAD"))
            return 1

        # Get staged changes
        index = repo.read_index()
        tree = index.get("tree", {})

        if not tree:
            print(error("Nothing to commit"))
            return 1

        # Create commit
        commit = Commit(
            tree=tree,
            parent=head_commit,
            message=message,
            author="spgit",
            committer="spgit"
        )
        commit_hash = write_object(repo, commit)

        # Update branch
        repo._update_ref(f"refs/heads/{current_branch}", commit_hash)
        repo._update_reflog(
            f"refs/heads/{current_branch}",
            head_commit,
            commit_hash,
            f"commit: {message}"
        )
        repo._update_reflog(
            "HEAD",
            head_commit,
            commit_hash,
            f"commit: {message}"
        )

        # Count changes
        track_count = len(tree)

        print(f"[{branch_color(current_branch)} {commit_hash[:7]}] {message}")
        print(f"{track_count} track{'s' if track_count != 1 else ''}")

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
