"""tag command implementation"""

from ..core.repository import find_repository
from ..utils.colors import error, success


def tag_command(args):
    """Create, list, or delete tags."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Delete tag
        if hasattr(args, 'delete') and args.delete:
            tag_name = args.delete
            tag_path = repo.tags_dir / tag_name

            if not tag_path.exists():
                print(error(f"Tag '{tag_name}' not found"))
                return 1

            tag_path.unlink()
            print(success(f"Deleted tag '{tag_name}'"))
            return 0

        # Create tag
        if hasattr(args, 'tag_name') and args.tag_name:
            tag_name = args.tag_name
            commit = args.commit if hasattr(args, 'commit') and args.commit else repo.get_head_commit()

            if not commit:
                print(error("Fatal: no commit specified and HEAD has no commits"))
                return 1

            tag_path = repo.tags_dir / tag_name
            if tag_path.exists():
                print(error(f"Tag '{tag_name}' already exists"))
                return 1

            tag_path.write_text(commit)
            print(success(f"Created tag '{tag_name}' at {commit[:7]}"))
            return 0

        # List tags
        tags = repo.list_tags()
        if not tags:
            print("No tags")
            return 0

        for tag in sorted(tags):
            print(tag)

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        return 1
