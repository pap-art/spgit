"""remote command implementation"""

from ..core.repository import find_repository
from ..utils.colors import error, success, info


def remote_command(args):
    """Manage remotes."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Add remote
        if hasattr(args, 'add') and args.add:
            name, url = args.add
            repo.add_remote(name, url)
            print(success(f"Added remote '{name}'"))
            return 0

        # Remove remote
        if hasattr(args, 'remove') and args.remove:
            repo.remove_remote(args.remove)
            print(success(f"Removed remote '{args.remove}'"))
            return 0

        # List remotes
        verbose = hasattr(args, 'verbose') and args.verbose
        remotes = repo.list_remotes()

        if not remotes:
            print("No remotes configured")
            return 0

        for name, url in remotes.items():
            if verbose:
                print(f"{name}\t{url} (fetch)")
                print(f"{name}\t{url} (push)")
            else:
                print(name)

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        return 1
