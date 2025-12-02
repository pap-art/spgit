"""merge command implementation"""

from ..core.repository import find_repository
from ..core.objects import (
    get_commit_tree, find_common_ancestor, Commit, write_object,
    create_tree_from_tracks, Track
)
from ..utils.colors import error, success, info, bold


def merge_command(args):
    """Merge branches."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        branch_name = args.branch

        # Get current branch
        current_branch = repo.get_current_branch()
        if not current_branch:
            print(error("Fatal: cannot merge in detached HEAD state"))
            return 1

        # Get branch to merge
        if not repo.branch_exists(branch_name):
            print(error(f"Branch '{branch_name}' not found"))
            return 1

        # Get commits
        current_commit = repo.get_head_commit()
        merge_commit = repo.get_branch_commit(branch_name)

        if not current_commit or not merge_commit:
            print(error("Fatal: invalid commit"))
            return 1

        # Check if already up to date
        if current_commit == merge_commit:
            print(info("Already up to date."))
            return 0

        # Find common ancestor
        base_commit = find_common_ancestor(repo, current_commit, merge_commit)

        # Check for fast-forward
        if base_commit == current_commit:
            # Fast-forward merge
            print(info(f"Updating {current_commit[:7]}..{merge_commit[:7]}"))
            print(info("Fast-forward"))

            repo._update_ref(f"refs/heads/{current_branch}", merge_commit)
            repo._update_reflog(
                f"refs/heads/{current_branch}",
                current_commit,
                merge_commit,
                f"merge {branch_name}: Fast-forward"
            )

            # Update index
            tracks = get_commit_tree(repo, merge_commit)
            tree = create_tree_from_tracks(repo, list(tracks.values()))
            repo.update_index({
                "tree": tree,
                "tracks": {uri: track.to_dict() for uri, track in tracks.items()}
            })

            print(success(f"Merged {branch_name} into {current_branch}"))
            return 0

        # Three-way merge
        print(info(f"Merge made by the 'three-way' strategy."))

        base_tracks = get_commit_tree(repo, base_commit) if base_commit else {}
        current_tracks = get_commit_tree(repo, current_commit)
        merge_tracks = get_commit_tree(repo, merge_commit)

        # Get merge strategy
        strategy = args.strategy if hasattr(args, 'strategy') and args.strategy else 'union'

        merged_tracks = _merge_tracks(base_tracks, current_tracks, merge_tracks, strategy)

        # Check for conflicts
        if merged_tracks is None:
            print(error("Automatic merge failed; fix conflicts and then commit the result."))
            return 1

        # Create merge commit
        tree = create_tree_from_tracks(repo, list(merged_tracks.values()))

        commit = Commit(
            tree=tree,
            parent=None,
            parents=[current_commit, merge_commit],
            message=f"Merge branch '{branch_name}' into {current_branch}",
            author="spgit",
            committer="spgit"
        )
        commit_hash = write_object(repo, commit)

        # Update branch
        repo._update_ref(f"refs/heads/{current_branch}", commit_hash)
        repo._update_reflog(
            f"refs/heads/{current_branch}",
            current_commit,
            commit_hash,
            f"merge {branch_name}: Merge made by the 'three-way' strategy."
        )

        # Update index
        repo.update_index({
            "tree": tree,
            "tracks": {uri: track.to_dict() for uri, track in merged_tracks.items()}
        })

        print(success(f"Merged {branch_name} into {current_branch}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1


def _merge_tracks(base_tracks, current_tracks, merge_tracks, strategy='union'):
    """
    Merge track sets using specified strategy.

    Returns merged tracks or None if conflicts
    """
    if strategy == 'union':
        # Union: combine all unique tracks
        merged = {}
        merged.update(current_tracks)
        merged.update(merge_tracks)
        return merged

    elif strategy == 'append':
        # Append: add merge tracks to end of current
        merged = {}
        merged.update(current_tracks)
        for uri, track in merge_tracks.items():
            if uri not in merged:
                merged[uri] = track
        return merged

    elif strategy == 'intersection':
        # Intersection: only keep tracks in both
        merged = {}
        for uri in current_tracks.keys() & merge_tracks.keys():
            merged[uri] = current_tracks[uri]
        return merged

    else:
        # Default to union
        merged = {}
        merged.update(current_tracks)
        merged.update(merge_tracks)
        return merged
