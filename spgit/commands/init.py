"""init command implementation"""

from ..core.repository import Repository
from ..utils.colors import success, error


def init_command(args):
    """Initialize a new spgit repository."""
    try:
        repo = Repository()

        if repo.exists():
            print(error("Fatal: Repository already exists"))
            return 1

        playlist_name = args.name if hasattr(args, 'name') and args.name else None
        repo.init(playlist_name)

        print(success(f"Initialized empty spgit repository in {repo.spgit_dir}"))
        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        return 1
