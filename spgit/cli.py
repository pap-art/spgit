"""
Main CLI entry point for spgit.
"""

import sys
import argparse
from . import __version__

# Import all commands
from .commands.init import init_command
from .commands.clone import clone_command
from .commands.fork import fork_command
from .commands.config import config_command
from .commands.add import add_command
from .commands.commit import commit_command
from .commands.status import status_command
from .commands.diff import diff_command
from .commands.compare import compare_command
from .commands.log import log_command
from .commands.branch import branch_command
from .commands.checkout import checkout_command
from .commands.merge import merge_command
from .commands.pull import pull_command
from .commands.push import push_command
from .commands.fetch import fetch_command
from .commands.remote import remote_command
from .commands.reset import reset_command
from .commands.revert import revert_command
from .commands.stash import stash_command
from .commands.tag import tag_command
from .commands.show import show_command
from .commands.cherrypick import cherrypick_command
from .commands.rebase import rebase_command
from .commands.blame import blame_command
from .commands.reflog import reflog_command


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='spgit',
        description='Git for Spotify Playlists',
        epilog='Use "spgit <command> --help" for more information about a command.'
    )

    parser.add_argument('--version', action='version', version=f'spgit {__version__}')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # init
    init_parser = subparsers.add_parser('init', help='Initialize a new repository')
    init_parser.add_argument('--name', help='Playlist name')

    # clone
    clone_parser = subparsers.add_parser('clone', help='Clone a Spotify playlist')
    clone_parser.add_argument('url', help='Spotify playlist URL')
    clone_parser.add_argument('directory', nargs='?', help='Directory name')

    # fork
    fork_parser = subparsers.add_parser('fork', help='Fork a playlist (clone and create your own copy on Spotify)')
    fork_parser.add_argument('url', help='Source Spotify playlist URL')
    fork_parser.add_argument('--name', help='Name for your new playlist')
    fork_parser.add_argument('--directory', help='Local directory name')

    # config
    config_parser = subparsers.add_parser('config', help='Configure spgit')
    config_parser.add_argument('--global', dest='global_config', action='store_true', help='Use global config')
    config_parser.add_argument('--list', action='store_true', help='List all configuration')
    config_parser.add_argument('--get', help='Get a configuration value')
    config_parser.add_argument('--set', nargs=2, metavar=('KEY', 'VALUE'), help='Set a configuration value')
    config_parser.add_argument('--unset', help='Unset a configuration value')

    # add
    add_parser = subparsers.add_parser('add', help='Add tracks to staging area')
    add_parser.add_argument('files', nargs='*', help='Track URIs to add (or use "." for all)')
    add_parser.add_argument('-a', '--all', action='store_true', help='Add all tracks')

    # commit
    commit_parser = subparsers.add_parser('commit', help='Record changes to repository')
    commit_parser.add_argument('-m', '--message', required=True, help='Commit message')

    # status
    status_parser = subparsers.add_parser('status', help='Show working tree status')

    # diff
    diff_parser = subparsers.add_parser('diff', help='Show changes')
    diff_parser.add_argument('--staged', action='store_true', help='Show staged changes')

    # compare
    compare_parser = subparsers.add_parser('compare', help='Compare with upstream or another remote')
    compare_parser.add_argument('--remote', default='upstream', help='Remote to compare with (default: upstream)')

    # log
    log_parser = subparsers.add_parser('log', help='Show commit logs')
    log_parser.add_argument('--oneline', action='store_true', help='Show one line per commit')
    log_parser.add_argument('--graph', action='store_true', help='Show graph')
    log_parser.add_argument('-n', '--limit', type=int, help='Limit number of commits')

    # branch
    branch_parser = subparsers.add_parser('branch', help='List, create, or delete branches')
    branch_parser.add_argument('branch_name', nargs='?', help='Branch name to create')
    branch_parser.add_argument('-d', '--delete', help='Delete branch')

    # checkout
    checkout_parser = subparsers.add_parser('checkout', help='Switch branches')
    checkout_parser.add_argument('branch', help='Branch name or commit hash')
    checkout_parser.add_argument('-b', dest='create_branch', action='store_true', help='Create and checkout new branch')

    # merge
    merge_parser = subparsers.add_parser('merge', help='Merge branches')
    merge_parser.add_argument('branch', help='Branch to merge')
    merge_parser.add_argument('--strategy', choices=['union', 'append', 'intersection'], default='union', help='Merge strategy')

    # pull
    pull_parser = subparsers.add_parser('pull', help='Fetch and merge from Spotify')
    pull_parser.add_argument('remote', nargs='?', default='origin', help='Remote name')

    # push
    push_parser = subparsers.add_parser('push', help='Update Spotify playlist')
    push_parser.add_argument('remote', nargs='?', default='origin', help='Remote name')

    # fetch
    fetch_parser = subparsers.add_parser('fetch', help='Download from Spotify')
    fetch_parser.add_argument('remote', nargs='?', default='origin', help='Remote name')

    # remote
    remote_parser = subparsers.add_parser('remote', help='Manage remotes')
    remote_parser.add_argument('-v', '--verbose', action='store_true', help='Show URLs')
    remote_parser.add_argument('--add', nargs=2, metavar=('NAME', 'URL'), help='Add remote')
    remote_parser.add_argument('--remove', help='Remove remote')

    # reset
    reset_parser = subparsers.add_parser('reset', help='Reset current HEAD')
    reset_parser.add_argument('commit', nargs='?', default='HEAD', help='Commit to reset to')
    reset_parser.add_argument('--soft', action='store_true', help='Soft reset')
    reset_parser.add_argument('--mixed', action='store_true', help='Mixed reset (default)')
    reset_parser.add_argument('--hard', action='store_true', help='Hard reset')

    # revert
    revert_parser = subparsers.add_parser('revert', help='Revert a commit')
    revert_parser.add_argument('commit', help='Commit to revert')

    # stash
    stash_parser = subparsers.add_parser('stash', help='Stash changes')
    stash_parser.add_argument('action', nargs='?', choices=['save', 'list', 'pop', 'apply', 'drop'], default='save', help='Stash action')
    stash_parser.add_argument('--message', '-m', help='Stash message')
    stash_parser.add_argument('stash', nargs='?', help='Stash to apply/drop')

    # tag
    tag_parser = subparsers.add_parser('tag', help='Create, list, or delete tags')
    tag_parser.add_argument('tag_name', nargs='?', help='Tag name to create')
    tag_parser.add_argument('commit', nargs='?', help='Commit to tag')
    tag_parser.add_argument('-d', '--delete', help='Delete tag')

    # show
    show_parser = subparsers.add_parser('show', help='Show commit details')
    show_parser.add_argument('commit', nargs='?', help='Commit to show')

    # cherry-pick
    cherrypick_parser = subparsers.add_parser('cherry-pick', help='Apply changes from a specific commit')
    cherrypick_parser.add_argument('commit', help='Commit to cherry-pick')

    # rebase
    rebase_parser = subparsers.add_parser('rebase', help='Reapply commits on top of another branch')
    rebase_parser.add_argument('branch', help='Branch to rebase onto')

    # blame
    blame_parser = subparsers.add_parser('blame', help='Show when track was added')
    blame_parser.add_argument('track', help='Track URI')

    # reflog
    reflog_parser = subparsers.add_parser('reflog', help='Show reference logs')
    reflog_parser.add_argument('ref', nargs='?', default='HEAD', help='Reference to show')

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Route to appropriate command
    commands = {
        'init': init_command,
        'clone': clone_command,
        'fork': fork_command,
        'config': config_command,
        'add': add_command,
        'commit': commit_command,
        'status': status_command,
        'diff': diff_command,
        'compare': compare_command,
        'log': log_command,
        'branch': branch_command,
        'checkout': checkout_command,
        'merge': merge_command,
        'pull': pull_command,
        'push': push_command,
        'fetch': fetch_command,
        'remote': remote_command,
        'reset': reset_command,
        'revert': revert_command,
        'stash': stash_command,
        'tag': tag_command,
        'show': show_command,
        'cherry-pick': cherrypick_command,
        'rebase': rebase_command,
        'blame': blame_command,
        'reflog': reflog_command,
    }

    command_func = commands.get(args.command)
    if command_func:
        try:
            return command_func(args)
        except KeyboardInterrupt:
            print("\nInterrupted")
            return 130
        except Exception as e:
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
