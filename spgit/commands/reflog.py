"""reflog command implementation"""

from ..core.repository import find_repository
from ..utils.colors import error, commit_hash, bold


def reflog_command(args):
    """Show reflog."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        ref = args.ref if hasattr(args, 'ref') and args.ref else "HEAD"

        # Read reflog
        reflog_path = repo.logs_dir / ref

        if not reflog_path.exists():
            # Try as branch
            reflog_path = repo.logs_dir / "refs" / "heads" / ref

        if not reflog_path.exists():
            print(error(f"Reflog for '{ref}' not found"))
            return 1

        with open(reflog_path, 'r') as f:
            lines = f.readlines()

        # Display reflog
        for i, line in enumerate(reversed(lines[-20:])):  # Show last 20 entries
            parts = line.strip().split(' ', 2)
            if len(parts) >= 3:
                old_hash, new_hash, message = parts
                print(f"{commit_hash(new_hash[:7])} {ref}@{{{i}}}: {message}")

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
