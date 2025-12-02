"""cherry-pick command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit as CommitObj, write_object, Commit
from ..utils.colors import error, success


def cherrypick_command(args):
    """Apply changes from a specific commit."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        commit_hash = args.commit

        # Read commit to cherry-pick
        try:
            commit_obj = read_object(repo, commit_hash)
            if not isinstance(commit_obj, CommitObj):
                print(error(f"'{commit_hash}' is not a commit"))
                return 1
        except ValueError:
            print(error(f"Commit '{commit_hash}' not found"))
            return 1

        # Get current HEAD
        head_commit = repo.get_head_commit()
        current_branch = repo.get_current_branch()

        if not current_branch:
            print(error("Fatal: cannot cherry-pick in detached HEAD state"))
            return 1

        # Create new commit with cherry-picked tree
        new_commit = Commit(
            tree=commit_obj.tree,
            parent=head_commit,
            message=f"{commit_obj.message}\n\n(cherry picked from commit {commit_hash})",
            author=commit_obj.author,
            committer="spgit"
        )
        new_hash = write_object(repo, new_commit)

        # Update branch
        repo._update_ref(f"refs/heads/{current_branch}", new_hash)
        repo._update_reflog(
            f"refs/heads/{current_branch}",
            head_commit,
            new_hash,
            f"cherry-pick: {commit_hash[:7]}"
        )

        print(success(f"Cherry-picked {commit_hash[:7]}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
