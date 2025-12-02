"""pull command implementation"""

from ..core.repository import find_repository
from ..core.spotify import get_spotify_client
from ..core.objects import create_tree_from_tracks, Commit, write_object
from ..utils.colors import error, success, info


def pull_command(args):
    """Fetch from and integrate with Spotify playlist."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        remote = args.remote if hasattr(args, 'remote') and args.remote else "origin"

        # Get remote URL
        remote_url = repo.get_remote_url(remote)
        if not remote_url:
            print(error(f"Remote '{remote}' not found"))
            return 1

        # Get current branch
        current_branch = repo.get_current_branch()
        if not current_branch:
            print(error("Fatal: cannot pull in detached HEAD state"))
            return 1

        print(info(f"Pulling from {remote}..."))

        # Fetch from Spotify
        sp = get_spotify_client(repo)
        playlist_id = sp.get_playlist_id(remote_url)
        tracks = sp.get_playlist_tracks(playlist_id)

        print(info(f"Received {len(tracks)} tracks"))

        # Create tree and commit
        tree = create_tree_from_tracks(repo, tracks)
        head_commit = repo.get_head_commit()

        commit = Commit(
            tree=tree,
            parent=head_commit,
            message=f"Pull from {remote}",
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
            f"pull {remote}: Fast-forward"
        )

        # Update index
        repo.update_index({
            "tree": tree,
            "tracks": {track.uri: track.to_dict() for track in tracks}
        })

        print(success(f"Successfully pulled from {remote}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
