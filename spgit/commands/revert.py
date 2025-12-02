"""revert command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit as CommitObj, write_object, Commit
from ..utils.colors import error, success


def revert_command(args):
    """Revert a commit by creating a new commit that undoes it."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        commit_hash = args.commit

        # Read commit to revert
        try:
            commit_obj = read_object(repo, commit_hash)
            if not isinstance(commit_obj, CommitObj):
                print(error(f"'{commit_hash}' is not a commit"))
                return 1
        except ValueError:
            print(error(f"Commit '{commit_hash}' not found"))
            return 1

        # Get parent commit tree (what it was before)
        if not commit_obj.parents:
            print(error("Cannot revert initial commit"))
            return 1

        parent_tree = read_object(repo, commit_obj.parents[0]).tree

        # Create revert commit
        head_commit = repo.get_head_commit()
        revert_commit = Commit(
            tree=parent_tree,
            parent=head_commit,
            message=f"Revert \"{commit_obj.message}\"\n\nThis reverts commit {commit_hash}.",
            author="spgit",
            committer="spgit"
        )
        revert_hash = write_object(repo, revert_commit)

        # Update branch
        current_branch = repo.get_current_branch()
        repo._update_ref(f"refs/heads/{current_branch}", revert_hash)
        repo._update_reflog(
            f"refs/heads/{current_branch}",
            head_commit,
            revert_hash,
            f"revert: {commit_hash[:7]}"
        )

        print(success(f"Reverted {commit_hash[:7]}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
