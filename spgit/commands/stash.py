"""stash command implementation"""

import json
from ..core.repository import find_repository
from ..utils.colors import error, success, info


def stash_command(args):
    """Stash changes."""
    try:
        repo = find_repository()
        if not repo:
            print(error("Fatal: not a spgit repository"))
            return 1

        # Load stash
        stash_list = []
        if repo.stash_path.exists():
            with open(repo.stash_path, 'r') as f:
                stash_list = json.load(f)

        # Stash save
        if not hasattr(args, 'action') or args.action == 'save':
            index = repo.read_index()
            if not index.get('tracks'):
                print("No local changes to save")
                return 0

            stash_list.append({
                'index': index,
                'message': args.message if hasattr(args, 'message') and args.message else 'WIP on branch'
            })

            with open(repo.stash_path, 'w') as f:
                json.dump(stash_list, f)

            # Clear index
            repo.update_index({})
            print(success(f"Saved working directory and index state"))
            return 0

        # Stash list
        if args.action == 'list':
            if not stash_list:
                print("No stash entries")
                return 0

            for i, stash in enumerate(stash_list):
                print(f"stash@{{{i}}}: {stash['message']}")
            return 0

        # Stash pop
        if args.action == 'pop':
            if not stash_list:
                print(error("No stash entries"))
                return 1

            stash = stash_list.pop()
            repo.update_index(stash['index'])

            with open(repo.stash_path, 'w') as f:
                json.dump(stash_list, f)

            print(success("Restored stash"))
            return 0

        # Stash apply
        if args.action == 'apply':
            if not stash_list:
                print(error("No stash entries"))
                return 1

            index = 0
            if hasattr(args, 'stash') and args.stash:
                index = int(args.stash.split('@{')[1].split('}')[0])

            if index >= len(stash_list):
                print(error(f"Stash entry {index} not found"))
                return 1

            stash = stash_list[index]
            repo.update_index(stash['index'])

            print(success(f"Applied stash@{{{index}}}"))
            return 0

        # Stash drop
        if args.action == 'drop':
            if not stash_list:
                print(error("No stash entries"))
                return 1

            index = 0
            if hasattr(args, 'stash') and args.stash:
                index = int(args.stash.split('@{')[1].split('}')[0])

            if index >= len(stash_list):
                print(error(f"Stash entry {index} not found"))
                return 1

            stash_list.pop(index)

            with open(repo.stash_path, 'w') as f:
                json.dump(stash_list, f)

            print(success(f"Dropped stash@{{{index}}}"))
            return 0

        return 0

    except Exception as e:
        print(error(f"Fatal: {str(e)}"))
        import traceback
        traceback.print_exc()
        return 1
