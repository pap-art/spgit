"""reset command implementation"""

from ..core.repository import find_repository
from ..core.objects import get_commit_tree, create_tree_from_tracks
from ..utils.colors import error, success, info


def reset_command(args):
    """Reset current HEAD to specified state."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        mode = 'mixed'  # default
        if hasattr(args, 'soft') and args.soft:
            mode = 'soft'
        elif hasattr(args, 'hard') and args.hard:
            mode = 'hard'

        commit = args.commit if hasattr(args, 'commit') and args.commit else 'HEAD'

        # Resolve commit
        if commit == 'HEAD':
            target_commit = repo.get_head_commit()
        elif commit.startswith('HEAD~'):
            # Handle HEAD~N
            steps = int(commit[5:]) if len(commit) > 5 else 1
            target_commit = repo.get_head_commit()

            from ..core.objects import read_object, Commit as CommitObj
            for _ in range(steps):
                if not target_commit:
                    break
                commit_obj = read_object(repo, target_commit)
                if isinstance(commit_obj, CommitObj) and commit_obj.parents:
                    target_commit = commit_obj.parents[0]
                else:
                    target_commit = None
        else:
            target_commit = commit

        if not target_commit:
            print(error("Fatal: invalid commit"))
            return 1

        current_branch = repo.get_current_branch()
        if not current_branch:
            print(error("Fatal: cannot reset in detached HEAD state"))
            return 1

        old_commit = repo.get_head_commit()

        # Update branch pointer
        repo._update_ref(f"refs/heads/{current_branch}", target_commit)
        repo._update_reflog(
            f"refs/heads/{current_branch}",
            old_commit,
            target_commit,
            f"reset: moving to {commit}"
        )

        if mode in ('mixed', 'hard'):
            # Update index
            tracks = get_commit_tree(repo, target_commit)
            tree = create_tree_from_tracks(repo, list(tracks.values()))
            repo.update_index({
                "tree": tree,
                "tracks": {uri: track.to_dict() for uri, track in tracks.items()}
            })

        print(success(f"HEAD is now at {target_commit[:7]}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
