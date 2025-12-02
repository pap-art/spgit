"""branch command implementation"""

from ..core.repository import find_repository
from ..utils.colors import error, success, branch as branch_color, bold


def branch_command(args):
    """List, create, or delete branches."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Delete branch
        if hasattr(args, 'delete') and args.delete:
            branch_name = args.delete
            current = repo.get_current_branch()

            if branch_name == current:
                print(error(f"Cannot delete branch '{branch_name}' checked out at '{repo.work_dir}'"))
                return 1

            if not repo.branch_exists(branch_name):
                print(error(f"Branch '{branch_name}' not found"))
                return 1

            repo.delete_branch(branch_name)
            print(success(f"Deleted branch {branch_name}"))
            return 0

        # Create branch
        if hasattr(args, 'branch_name') and args.branch_name:
            branch_name = args.branch_name
            head_commit = repo.get_head_commit()

            if not head_commit:
                print(error("Fatal: no commits yet"))
                return 1

            if repo.branch_exists(branch_name):
                print(error(f"Fatal: branch '{branch_name}' already exists"))
                return 1

            repo.create_branch(branch_name, head_commit)
            print(success(f"Created branch {branch_name}"))
            return 0

        # List branches
        current = repo.get_current_branch()
        branches = repo.list_branches()

        if not branches:
            print("No branches")
            return 0

        for b in sorted(branches):
            if b == current:
                print(f"* {branch_color(b)}")
            else:
                print(f"  {b}")

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
