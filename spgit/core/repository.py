"""
Core repository management for spgit.
Implements git-like storage structure with .spgit directory.
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Repository:
    """Represents a spgit repository."""

    def __init__(self, path: str = "."):
        """Initialize repository at the given path."""
        self.work_dir = Path(path).resolve()
        self.spgit_dir = self.work_dir / ".spgit"

    @property
    def head_path(self) -> Path:
        """Path to HEAD file."""
        return self.spgit_dir / "HEAD"

    @property
    def config_path(self) -> Path:
        """Path to config file."""
        return self.spgit_dir / "config"

    @property
    def index_path(self) -> Path:
        """Path to index (staging area) file."""
        return self.spgit_dir / "index"

    @property
    def objects_dir(self) -> Path:
        """Path to objects directory."""
        return self.spgit_dir / "objects"

    @property
    def refs_dir(self) -> Path:
        """Path to refs directory."""
        return self.spgit_dir / "refs"

    @property
    def heads_dir(self) -> Path:
        """Path to refs/heads directory."""
        return self.refs_dir / "heads"

    @property
    def tags_dir(self) -> Path:
        """Path to refs/tags directory."""
        return self.refs_dir / "tags"

    @property
    def remotes_dir(self) -> Path:
        """Path to refs/remotes directory."""
        return self.refs_dir / "remotes"

    @property
    def logs_dir(self) -> Path:
        """Path to logs directory."""
        return self.spgit_dir / "logs"

    @property
    def stash_path(self) -> Path:
        """Path to stash file."""
        return self.spgit_dir / "stash"

    def exists(self) -> bool:
        """Check if repository exists."""
        return self.spgit_dir.exists() and self.spgit_dir.is_dir()

    def init(self, playlist_name: Optional[str] = None) -> None:
        """
        Initialize a new repository.

        Args:
            playlist_name: Optional name for the playlist
        """
        if self.exists():
            raise ValueError(f"Repository already exists at {self.work_dir}")

        # Create directory structure
        self.spgit_dir.mkdir(parents=True, exist_ok=True)
        self.objects_dir.mkdir(exist_ok=True)
        self.refs_dir.mkdir(exist_ok=True)
        self.heads_dir.mkdir(exist_ok=True)
        self.tags_dir.mkdir(exist_ok=True)
        self.remotes_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        (self.logs_dir / "refs" / "heads").mkdir(parents=True, exist_ok=True)

        # Initialize HEAD to point to main branch
        self.head_path.write_text("ref: refs/heads/main")

        # Initialize config
        config = {
            "core": {
                "repositoryformatversion": 0,
                "filemode": True,
                "bare": False
            },
            "playlist": {
                "name": playlist_name or self.work_dir.name
            }
        }
        self._write_config(config)

        # Initialize empty index
        self._write_index({})

        # Create initial empty commit on main branch
        from .objects import Commit
        initial_commit = Commit(
            tree={},
            parent=None,
            message="Initial commit",
            author="spgit",
            committer="spgit"
        )
        commit_hash = self._write_object(initial_commit)
        self._update_ref("refs/heads/main", commit_hash)
        self._update_reflog("refs/heads/main", None, commit_hash, "commit (initial): Initial commit")

    def get_current_branch(self) -> Optional[str]:
        """Get the current branch name."""
        if not self.head_path.exists():
            return None

        head_content = self.head_path.read_text().strip()
        if head_content.startswith("ref: refs/heads/"):
            return head_content[16:]  # Remove "ref: refs/heads/"
        return None  # Detached HEAD

    def get_head_commit(self) -> Optional[str]:
        """Get the commit hash that HEAD points to."""
        if not self.head_path.exists():
            return None

        head_content = self.head_path.read_text().strip()

        if head_content.startswith("ref: "):
            # HEAD points to a branch
            ref_path = self.spgit_dir / head_content[5:]  # Remove "ref: "
            if ref_path.exists():
                return ref_path.read_text().strip()
            return None
        else:
            # Detached HEAD
            return head_content

    def get_branch_commit(self, branch: str) -> Optional[str]:
        """Get the commit hash for a branch."""
        branch_path = self.heads_dir / branch
        if branch_path.exists():
            return branch_path.read_text().strip()
        return None

    def _update_ref(self, ref: str, commit_hash: str) -> None:
        """Update a reference to point to a commit."""
        ref_path = self.spgit_dir / ref
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_text(commit_hash)

    def _update_reflog(self, ref: str, old_hash: Optional[str], new_hash: str, message: str) -> None:
        """Update the reflog for a reference."""
        reflog_path = self.logs_dir / ref
        reflog_path.parent.mkdir(parents=True, exist_ok=True)

        old = old_hash or "0" * 40
        entry = f"{old} {new_hash} {message}\n"

        with open(reflog_path, "a") as f:
            f.write(entry)

    def _write_config(self, config: Dict[str, Any]) -> None:
        """Write configuration to disk."""
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    def read_config(self) -> Dict[str, Any]:
        """Read configuration from disk."""
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r") as f:
            return json.load(f)

    def update_config(self, section: str, key: str, value: Any) -> None:
        """Update a configuration value."""
        config = self.read_config()
        if section not in config:
            config[section] = {}
        config[section][key] = value
        self._write_config(config)

    def _write_index(self, index: Dict[str, Any]) -> None:
        """Write index to disk."""
        with open(self.index_path, "w") as f:
            json.dump(index, f, indent=2)

    def read_index(self) -> Dict[str, Any]:
        """Read index from disk."""
        if not self.index_path.exists():
            return {}
        with open(self.index_path, "r") as f:
            return json.load(f)

    def update_index(self, index: Dict[str, Any]) -> None:
        """Update the index."""
        self._write_index(index)

    def _write_object(self, obj) -> str:
        """Write an object to the object database and return its hash."""
        from .objects import write_object
        return write_object(self, obj)

    def read_object(self, obj_hash: str):
        """Read an object from the object database."""
        from .objects import read_object
        return read_object(self, obj_hash)

    def list_branches(self) -> list:
        """List all branches."""
        if not self.heads_dir.exists():
            return []
        return [f.name for f in self.heads_dir.iterdir() if f.is_file()]

    def list_tags(self) -> list:
        """List all tags."""
        if not self.tags_dir.exists():
            return []
        return [f.name for f in self.tags_dir.iterdir() if f.is_file()]

    def branch_exists(self, branch: str) -> bool:
        """Check if a branch exists."""
        return (self.heads_dir / branch).exists()

    def create_branch(self, branch: str, commit_hash: str) -> None:
        """Create a new branch pointing to a commit."""
        if self.branch_exists(branch):
            raise ValueError(f"Branch '{branch}' already exists")
        self._update_ref(f"refs/heads/{branch}", commit_hash)

    def delete_branch(self, branch: str) -> None:
        """Delete a branch."""
        branch_path = self.heads_dir / branch
        if not branch_path.exists():
            raise ValueError(f"Branch '{branch}' does not exist")
        branch_path.unlink()

    def checkout_branch(self, branch: str) -> None:
        """Switch to a branch."""
        if not self.branch_exists(branch):
            raise ValueError(f"Branch '{branch}' does not exist")

        old_commit = self.get_head_commit()
        self.head_path.write_text(f"ref: refs/heads/{branch}")
        new_commit = self.get_head_commit()

        if new_commit:
            self._update_reflog("HEAD", old_commit, new_commit, f"checkout: moving from {self.get_current_branch() or 'detached'} to {branch}")

    def checkout_detached(self, commit_hash: str) -> None:
        """Checkout a specific commit (detached HEAD)."""
        old_commit = self.get_head_commit()
        self.head_path.write_text(commit_hash)
        self._update_reflog("HEAD", old_commit, commit_hash, f"checkout: moving to {commit_hash[:7]}")

    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get the URL for a remote."""
        config = self.read_config()
        return config.get("remote", {}).get(remote, {}).get("url")

    def add_remote(self, name: str, url: str) -> None:
        """Add a remote."""
        config = self.read_config()
        if "remote" not in config:
            config["remote"] = {}
        if name in config["remote"]:
            raise ValueError(f"Remote '{name}' already exists")
        config["remote"][name] = {"url": url}
        self._write_config(config)

    def remove_remote(self, name: str) -> None:
        """Remove a remote."""
        config = self.read_config()
        if "remote" not in config or name not in config["remote"]:
            raise ValueError(f"Remote '{name}' does not exist")
        del config["remote"][name]
        self._write_config(config)

    def list_remotes(self) -> Dict[str, str]:
        """List all remotes."""
        config = self.read_config()
        return {name: info["url"] for name, info in config.get("remote", {}).items()}


def find_repository(path: str = ".") -> Optional[Repository]:
    """
    Find a repository by searching up the directory tree.

    Args:
        path: Starting path to search from

    Returns:
        Repository object if found, None otherwise
    """
    current = Path(path).resolve()

    while True:
        repo = Repository(current)
        if repo.exists():
            return repo

        if current.parent == current:
            # Reached root
            return None

        current = current.parent
