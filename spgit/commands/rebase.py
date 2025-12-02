"""rebase command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit as CommitObj, write_object, Commit, get_commit_history
from ..utils.colors import error, success, info


def rebase_command(args):
    """Reapply commits on top of another branch."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        target_branch = args.branch

        # Get target branch commit
        if not repo.branch_exists(target_branch):
            print(error(f"Branch '{target_branch}' not found"))
            return 1

        target_commit = repo.get_branch_commit(target_branch)
        current_branch = repo.get_current_branch()

        if not current_branch:
            print(error("Fatal: cannot rebase in detached HEAD state"))
            return 1

        current_commit = repo.get_head_commit()

        print(info(f"Rebasing {current_branch} onto {target_branch}..."))

        # Get commits to reapply
        current_history = set(get_commit_history(repo, current_commit))
        target_history = set(get_commit_history(repo, target_commit))

        commits_to_reapply = []
        commit = current_commit

        while commit and commit not in target_history:
            commits_to_reapply.append(commit)
            try:
                commit_obj = read_object(repo, commit)
                if isinstance(commit_obj, CommitObj) and commit_obj.parents:
                    commit = commit_obj.parents[0]
                else:
                    break
            except ValueError:
                break

        commits_to_reapply.reverse()

        # Reapply commits
        new_head = target_commit

        for old_commit in commits_to_reapply:
            old_commit_obj = read_object(repo, old_commit)
            if not isinstance(old_commit_obj, CommitObj):
                continue

            # Create new commit
            new_commit = Commit(
                tree=old_commit_obj.tree,
                parent=new_head,
                message=old_commit_obj.message,
                author=old_commit_obj.author,
                committer="spgit"
            )
            new_head = write_object(repo, new_commit)

        # Update branch
        repo._update_ref(f"refs/heads/{current_branch}", new_head)
        repo._update_reflog(
            f"refs/heads/{current_branch}",
            current_commit,
            new_head,
            f"rebase: onto {target_branch}"
        )

        print(success(f"Successfully rebased {current_branch} onto {target_branch}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
