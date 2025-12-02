"""checkout command implementation"""

from ..core.repository import find_repository
from ..core.objects import Track, get_commit_tree
from ..utils.colors import error, success, info


def checkout_command(args):
    """Switch branches or restore working tree files."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Create and checkout new branch
        if hasattr(args, 'create_branch') and args.create_branch:
            branch_name = args.branch
            head_commit = repo.get_head_commit()

            if not head_commit:
                print(error("Fatal: no commits yet"))
                return 1

            if repo.branch_exists(branch_name):
                print(error(f"Fatal: branch '{branch_name}' already exists"))
                return 1

            # Create branch
            repo.create_branch(branch_name, head_commit)
            # Checkout branch
            repo.checkout_branch(branch_name)

            print(success(f"Switched to a new branch '{branch_name}'"))
            return 0

        # Checkout existing branch or commit
        target = args.branch if hasattr(args, 'branch') else None

        if not target:
            print(error("Fatal: no branch or commit specified"))
            return 1

        # Check if it's a branch
        if repo.branch_exists(target):
            repo.checkout_branch(target)
            print(success(f"Switched to branch '{target}'"))

            # Update index to match branch
            commit_hash = repo.get_branch_commit(target)
            if commit_hash:
                tracks = get_commit_tree(repo, commit_hash)
                from ..core.objects import create_tree_from_tracks
                tree = create_tree_from_tracks(repo, list(tracks.values()))
                repo.update_index({
                    "tree": tree,
                    "tracks": {uri: track.to_dict() for uri, track in tracks.items()}
                })

        else:
            # Try as commit hash
            try:
                repo.checkout_detached(target)
                print(info(f"Note: switching to '{target}'."))
                print(info("You are in 'detached HEAD' state."))

                # Update index
                tracks = get_commit_tree(repo, target)
                from ..core.objects import create_tree_from_tracks
                tree = create_tree_from_tracks(repo, list(tracks.values()))
                repo.update_index({
                    "tree": tree,
                    "tracks": {uri: track.to_dict() for uri, track in tracks.items()}
                })

            except Exception:
                print(error(f"Error: pathspec '{target}' did not match any file(s) known to spgit"))
                return 1

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
