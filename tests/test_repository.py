"""Tests for repository functionality"""

import pytest
import tempfile
import shutil
from pathlib import Path
from spgit.core.repository import Repository, find_repository


class TestRepository:
    """Test repository operations."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    def test_init_creates_structure(self, temp_dir):
        """Test that init creates proper directory structure."""
        repo = Repository(temp_dir)
        repo.init()

        assert repo.spgit_dir.exists()
        assert repo.objects_dir.exists()
        assert repo.refs_dir.exists()
        assert repo.heads_dir.exists()
        assert repo.tags_dir.exists()
        assert repo.logs_dir.exists()
        assert repo.head_path.exists()
        assert repo.config_path.exists()
        assert repo.index_path.exists()

    def test_init_sets_head(self, temp_dir):
        """Test that init sets HEAD to main branch."""
        repo = Repository(temp_dir)
        repo.init()

        head_content = repo.head_path.read_text().strip()
        assert head_content == "ref: refs/heads/main"

    def test_init_twice_fails(self, temp_dir):
        """Test that init fails if repository already exists."""
        repo = Repository(temp_dir)
        repo.init()

        with pytest.raises(ValueError):
            repo.init()

    def test_find_repository(self, temp_dir):
        """Test finding repository in parent directories."""
        repo = Repository(temp_dir)
        repo.init()

        # Create subdirectory
        subdir = temp_dir / "subdir" / "nested"
        subdir.mkdir(parents=True)

        # Find from subdirectory
        found = find_repository(subdir)
        assert found is not None
        assert found.work_dir == temp_dir

    def test_branch_operations(self, temp_dir):
        """Test branch creation and listing."""
        repo = Repository(temp_dir)
        repo.init()

        # Get initial commit
        head_commit = repo.get_head_commit()

        # Create branch
        repo.create_branch("feature", head_commit)
        assert repo.branch_exists("feature")

        # List branches
        branches = repo.list_branches()
        assert "main" in branches
        assert "feature" in branches

        # Delete branch
        repo.delete_branch("feature")
        assert not repo.branch_exists("feature")

    def test_checkout_branch(self, temp_dir):
        """Test checking out branches."""
        repo = Repository(temp_dir)
        repo.init()

        head_commit = repo.get_head_commit()
        repo.create_branch("feature", head_commit)

        # Checkout branch
        repo.checkout_branch("feature")
        assert repo.get_current_branch() == "feature"

        # Checkout main
        repo.checkout_branch("main")
        assert repo.get_current_branch() == "main"

    def test_config_operations(self, temp_dir):
        """Test configuration read/write."""
        repo = Repository(temp_dir)
        repo.init()

        # Update config
        repo.update_config("test", "key", "value")

        # Read config
        config = repo.read_config()
        assert config["test"]["key"] == "value"

    def test_remote_operations(self, temp_dir):
        """Test remote management."""
        repo = Repository(temp_dir)
        repo.init()

        # Add remote
        repo.add_remote("origin", "https://example.com/playlist")

        # Get remote URL
        url = repo.get_remote_url("origin")
        assert url == "https://example.com/playlist"

        # List remotes
        remotes = repo.list_remotes()
        assert "origin" in remotes

        # Remove remote
        repo.remove_remote("origin")
        remotes = repo.list_remotes()
        assert "origin" not in remotes
