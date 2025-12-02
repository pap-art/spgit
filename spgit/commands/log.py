"""log command implementation"""

from ..core.repository import find_repository
from ..core.objects import read_object, Commit
from ..utils.colors import error, commit_hash, yellow, gray, bold
from ..utils.helpers import format_timestamp


def log_command(args):
    """Show commit logs."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        head_commit = repo.get_head_commit()
        if not head_commit:
            print(error("Fatal: no commits yet"))
            return 1

        # Get formatting options
        oneline = hasattr(args, 'oneline') and args.oneline
        graph = hasattr(args, 'graph') and args.graph
        limit = args.limit if hasattr(args, 'limit') and args.limit else None

        # Build commit history
        commits = []
        visited = set()
        queue = [head_commit]
        count = 0

        while queue and (limit is None or count < limit):
            current_hash = queue.pop(0)
            if current_hash in visited:
                continue

            visited.add(current_hash)

            try:
                commit = read_object(repo, current_hash)
                if isinstance(commit, Commit):
                    commits.append((current_hash, commit))
                    queue.extend(commit.parents)
                    count += 1
            except ValueError:
                pass

        # Display commits
        for current_hash, commit in commits:
            if oneline:
                # One-line format
                short_hash = commit_hash(current_hash[:7])
                first_line = commit.message.split('\n')[0]
                print(f"{short_hash} {first_line}")
            else:
                # Full format
                print(commit_hash(f"commit {current_hash}"))
                print(f"Author: {commit.author}")
                print(f"Date:   {format_timestamp(commit.timestamp)}")
                print()
                for line in commit.message.split('\n'):
                    print(f"    {line}")
                print()

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
