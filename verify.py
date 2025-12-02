#!/usr/bin/env python3
"""
Verification script for spgit installation and functionality.
Run this to verify that spgit is properly installed and working.
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path


def print_header(text):
    """Print section header."""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def test_imports():
    """Test that all modules can be imported."""
    print_header("Testing Module Imports")

    try:
        import spgit
        print(f"✓ spgit version: {spgit.__version__}")

        from spgit.core import repository
        print("✓ spgit.core.repository")

        from spgit.core import objects
        print("✓ spgit.core.objects")

        from spgit.core import spotify
        print("✓ spgit.core.spotify")

        from spgit.utils import colors
        print("✓ spgit.utils.colors")

        from spgit.utils import helpers
        print("✓ spgit.utils.helpers")

        from spgit import cli
        print("✓ spgit.cli")

        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_repository():
    """Test repository operations."""
    print_header("Testing Repository Operations")

    try:
        from spgit.core.repository import Repository

        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        print(f"Created temp directory: {temp_dir}")

        # Initialize repository
        repo = Repository(temp_dir)
        repo.init()
        print("✓ Repository initialized")

        # Check structure
        assert repo.spgit_dir.exists(), "Missing .spgit directory"
        assert repo.objects_dir.exists(), "Missing objects directory"
        assert repo.refs_dir.exists(), "Missing refs directory"
        assert repo.head_path.exists(), "Missing HEAD file"
        print("✓ Directory structure correct")

        # Check HEAD
        head_content = repo.head_path.read_text().strip()
        assert head_content == "ref: refs/heads/main", "Incorrect HEAD"
        print("✓ HEAD points to main branch")

        # Check initial commit
        commit_hash = repo.get_head_commit()
        assert commit_hash is not None, "No initial commit"
        print(f"✓ Initial commit: {commit_hash[:7]}")

        # Test branching
        repo.create_branch("test-branch", commit_hash)
        assert repo.branch_exists("test-branch"), "Branch not created"
        print("✓ Branch creation works")

        # Test checkout
        repo.checkout_branch("test-branch")
        assert repo.get_current_branch() == "test-branch", "Checkout failed"
        print("✓ Branch checkout works")

        # Cleanup
        shutil.rmtree(temp_dir)
        print("✓ Cleanup successful")

        return True
    except Exception as e:
        print(f"✗ Repository test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_objects():
    """Test object database."""
    print_header("Testing Object Database")

    try:
        from spgit.core.repository import Repository
        from spgit.core.objects import Track, Blob, Commit, write_object, read_object

        # Create temporary repository
        temp_dir = tempfile.mkdtemp()
        repo = Repository(temp_dir)
        repo.init()

        # Create track
        track = Track(
            uri="spotify:track:test123",
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration_ms=180000
        )
        print(f"✓ Created track: {track.name} - {track.artist}")

        # Create and write blob
        blob = Blob(track)
        blob_hash = write_object(repo, blob)
        print(f"✓ Wrote blob: {blob_hash[:7]}")

        # Read blob back
        blob2 = read_object(repo, blob_hash)
        assert blob2.track.uri == track.uri, "Track URI mismatch"
        assert blob2.track.name == track.name, "Track name mismatch"
        print("✓ Read blob successfully")

        # Create and write commit
        commit = Commit(
            tree={track.uri: blob_hash},
            parent=None,
            message="Test commit",
            author="Test",
            committer="Test"
        )
        commit_hash = write_object(repo, commit)
        print(f"✓ Wrote commit: {commit_hash[:7]}")

        # Read commit back
        commit2 = read_object(repo, commit_hash)
        assert commit2.message == "Test commit", "Commit message mismatch"
        print("✓ Read commit successfully")

        # Cleanup
        shutil.rmtree(temp_dir)
        print("✓ Cleanup successful")

        return True
    except Exception as e:
        print(f"✗ Object test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_utils():
    """Test utility functions."""
    print_header("Testing Utilities")

    try:
        from spgit.utils.helpers import format_duration, truncate, pluralize
        from spgit.utils.colors import red, green, colorize

        # Test helpers
        assert format_duration(0) == "0:00"
        assert format_duration(60000) == "1:00"
        assert format_duration(125000) == "2:05"
        print("✓ Duration formatting works")

        assert truncate("hello world", 8) == "hello..."
        print("✓ Text truncation works")

        assert pluralize(1, "track") == "1 track"
        assert pluralize(2, "track") == "2 tracks"
        print("✓ Pluralization works")

        # Test colors (just ensure they don't crash)
        text = red("test")
        text = green("test")
        text = colorize("test", "\033[31m")
        print("✓ Color functions work")

        return True
    except Exception as e:
        print(f"✗ Utility test failed: {e}")
        return False


def test_cli():
    """Test CLI argument parsing."""
    print_header("Testing CLI")

    try:
        from spgit.cli import create_parser

        parser = create_parser()

        # Test init command
        args = parser.parse_args(['init'])
        assert args.command == 'init'
        print("✓ init command parsing")

        # Test clone command
        args = parser.parse_args(['clone', 'https://example.com/playlist/xyz'])
        assert args.command == 'clone'
        assert args.url == 'https://example.com/playlist/xyz'
        print("✓ clone command parsing")

        # Test commit command
        args = parser.parse_args(['commit', '-m', 'Test message'])
        assert args.command == 'commit'
        assert args.message == 'Test message'
        print("✓ commit command parsing")

        # Test branch command
        args = parser.parse_args(['branch', 'test-branch'])
        assert args.command == 'branch'
        print("✓ branch command parsing")

        return True
    except Exception as e:
        print(f"✗ CLI test failed: {e}")
        return False


def main():
    """Run all tests."""
    print_header("spgit Verification Script")
    print("This script will verify that spgit is properly installed")
    print("and all core functionality is working.")

    results = {
        "Imports": test_imports(),
        "Repository": test_repository(),
        "Objects": test_objects(),
        "Utilities": test_utils(),
        "CLI": test_cli(),
    }

    # Summary
    print_header("Test Summary")

    passed = sum(results.values())
    total = len(results)

    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! spgit is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
