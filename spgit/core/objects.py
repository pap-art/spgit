"""
Object database implementation for spgit.
Handles commits, trees, and blobs with SHA-1 hashing.
"""

import hashlib
import json
import zlib
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path


class SpgitObject:
    """Base class for spgit objects."""

    def __init__(self, obj_type: str):
        self.obj_type = obj_type

    def serialize(self) -> bytes:
        """Serialize object to bytes."""
        raise NotImplementedError

    @classmethod
    def deserialize(cls, data: bytes):
        """Deserialize object from bytes."""
        raise NotImplementedError

    def hash(self) -> str:
        """Calculate SHA-1 hash of object."""
        data = self.serialize()
        return hashlib.sha1(data).hexdigest()


class Track:
    """Represents a Spotify track."""

    def __init__(
        self,
        uri: str,
        name: str,
        artist: str,
        album: str,
        duration_ms: int,
        added_at: Optional[str] = None,
        added_by: Optional[str] = None
    ):
        self.uri = uri
        self.name = name
        self.artist = artist
        self.album = album
        self.duration_ms = duration_ms
        self.added_at = added_at or datetime.utcnow().isoformat()
        self.added_by = added_by

    def to_dict(self) -> Dict[str, Any]:
        """Convert track to dictionary."""
        return {
            "uri": self.uri,
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "duration_ms": self.duration_ms,
            "added_at": self.added_at,
            "added_by": self.added_by
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Track":
        """Create track from dictionary."""
        return cls(**data)

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)

    def __repr__(self):
        return f"Track(uri={self.uri}, name={self.name}, artist={self.artist})"


class Blob(SpgitObject):
    """Represents a blob object (track data)."""

    def __init__(self, track: Track):
        super().__init__("blob")
        self.track = track

    def serialize(self) -> bytes:
        """Serialize blob to bytes."""
        data = {
            "type": self.obj_type,
            "track": self.track.to_dict()
        }
        return json.dumps(data, sort_keys=True).encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> "Blob":
        """Deserialize blob from bytes."""
        obj = json.loads(data.decode("utf-8"))
        return cls(Track.from_dict(obj["track"]))


class Tree(SpgitObject):
    """Represents a tree object (collection of tracks)."""

    def __init__(self, tracks: Dict[str, str]):
        """
        Initialize tree.

        Args:
            tracks: Dictionary mapping track URI to blob hash
        """
        super().__init__("tree")
        self.tracks = tracks  # {uri: blob_hash}

    def serialize(self) -> bytes:
        """Serialize tree to bytes."""
        data = {
            "type": self.obj_type,
            "tracks": self.tracks
        }
        return json.dumps(data, sort_keys=True).encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> "Tree":
        """Deserialize tree from bytes."""
        obj = json.loads(data.decode("utf-8"))
        return cls(obj["tracks"])


class Commit(SpgitObject):
    """Represents a commit object."""

    def __init__(
        self,
        tree: Dict[str, str],
        parent: Optional[str],
        message: str,
        author: str,
        committer: str,
        timestamp: Optional[str] = None,
        parents: Optional[List[str]] = None
    ):
        """
        Initialize commit.

        Args:
            tree: Dictionary mapping track URI to blob hash
            parent: Parent commit hash (for single parent)
            message: Commit message
            author: Author name
            committer: Committer name
            timestamp: ISO format timestamp
            parents: List of parent commit hashes (for merges)
        """
        super().__init__("commit")
        self.tree = tree
        self.parents = parents if parents is not None else ([parent] if parent else [])
        self.message = message
        self.author = author
        self.committer = committer
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def serialize(self) -> bytes:
        """Serialize commit to bytes."""
        data = {
            "type": self.obj_type,
            "tree": self.tree,
            "parents": self.parents,
            "message": self.message,
            "author": self.author,
            "committer": self.committer,
            "timestamp": self.timestamp
        }
        return json.dumps(data, sort_keys=True).encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> "Commit":
        """Deserialize commit from bytes."""
        obj = json.loads(data.decode("utf-8"))
        return cls(
            tree=obj["tree"],
            parent=None,
            message=obj["message"],
            author=obj["author"],
            committer=obj["committer"],
            timestamp=obj["timestamp"],
            parents=obj["parents"]
        )


def write_object(repo, obj: SpgitObject) -> str:
    """
    Write an object to the repository's object database.

    Args:
        repo: Repository instance
        obj: Object to write

    Returns:
        SHA-1 hash of the object
    """
    data = obj.serialize()
    obj_hash = hashlib.sha1(data).hexdigest()

    # Store object in subdirectory based on first 2 chars of hash
    obj_dir = repo.objects_dir / obj_hash[:2]
    obj_dir.mkdir(exist_ok=True)

    obj_path = obj_dir / obj_hash[2:]

    # Compress data with zlib
    compressed = zlib.compress(data)

    with open(obj_path, "wb") as f:
        f.write(compressed)

    return obj_hash


def read_object(repo, obj_hash: str) -> SpgitObject:
    """
    Read an object from the repository's object database.

    Args:
        repo: Repository instance
        obj_hash: SHA-1 hash of the object

    Returns:
        Deserialized object
    """
    obj_path = repo.objects_dir / obj_hash[:2] / obj_hash[2:]

    if not obj_path.exists():
        raise ValueError(f"Object {obj_hash} not found")

    with open(obj_path, "rb") as f:
        compressed = f.read()

    # Decompress data
    data = zlib.decompress(compressed)

    # Determine object type
    obj = json.loads(data.decode("utf-8"))
    obj_type = obj["type"]

    if obj_type == "blob":
        return Blob.deserialize(data)
    elif obj_type == "tree":
        return Tree.deserialize(data)
    elif obj_type == "commit":
        return Commit.deserialize(data)
    else:
        raise ValueError(f"Unknown object type: {obj_type}")


def get_commit_tree(repo, commit_hash: str) -> Dict[str, Track]:
    """
    Get all tracks from a commit.

    Args:
        repo: Repository instance
        commit_hash: Commit hash

    Returns:
        Dictionary mapping track URI to Track object
    """
    commit = read_object(repo, commit_hash)
    if not isinstance(commit, Commit):
        raise ValueError(f"{commit_hash} is not a commit")

    tracks = {}
    for uri, blob_hash in commit.tree.items():
        blob = read_object(repo, blob_hash)
        if isinstance(blob, Blob):
            tracks[uri] = blob.track

    return tracks


def create_tree_from_tracks(repo, tracks: List[Track]) -> Dict[str, str]:
    """
    Create a tree from a list of tracks.

    Args:
        repo: Repository instance
        tracks: List of Track objects

    Returns:
        Dictionary mapping track URI to blob hash
    """
    tree = {}
    for track in tracks:
        blob = Blob(track)
        blob_hash = write_object(repo, blob)
        tree[track.uri] = blob_hash

    return tree


def get_commit_history(repo, commit_hash: str) -> List[str]:
    """
    Get the commit history from a commit.

    Args:
        repo: Repository instance
        commit_hash: Starting commit hash

    Returns:
        List of commit hashes in chronological order (oldest first)
    """
    history = []
    visited = set()
    queue = [commit_hash]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue

        visited.add(current)
        history.append(current)

        try:
            commit = read_object(repo, current)
            if isinstance(commit, Commit):
                queue.extend(commit.parents)
        except ValueError:
            # Object not found, skip
            pass

    return list(reversed(history))


def find_common_ancestor(repo, commit1: str, commit2: str) -> Optional[str]:
    """
    Find the common ancestor of two commits.

    Args:
        repo: Repository instance
        commit1: First commit hash
        commit2: Second commit hash

    Returns:
        Common ancestor commit hash, or None if no common ancestor
    """
    history1 = set(get_commit_history(repo, commit1))
    history2 = get_commit_history(repo, commit2)

    for commit in reversed(history2):
        if commit in history1:
            return commit

    return None
