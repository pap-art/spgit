"""Tests for object database"""

import pytest
import tempfile
import shutil
from pathlib import Path
from spgit.core.repository import Repository
from spgit.core.objects import (
    Track, Blob, Tree, Commit, write_object, read_object,
    create_tree_from_tracks, get_commit_tree, find_common_ancestor
)


class TestObjects:
    """Test object database operations."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    @pytest.fixture
    def repo(self, temp_dir):
        """Create initialized repository."""
        repo = Repository(temp_dir)
        repo.init()
        return repo

    def test_track_serialization(self):
        """Test track to/from dict."""
        track = Track(
            uri="spotify:track:xyz",
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration_ms=180000
        )

        data = track.to_dict()
        track2 = Track.from_dict(data)

        assert track.uri == track2.uri
        assert track.name == track2.name
        assert track.artist == track2.artist

    def test_blob_operations(self, repo):
        """Test blob write/read."""
        track = Track(
            uri="spotify:track:xyz",
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration_ms=180000
        )

        blob = Blob(track)
        blob_hash = write_object(repo, blob)

        # Read back
        blob2 = read_object(repo, blob_hash)
        assert isinstance(blob2, Blob)
        assert blob2.track.uri == track.uri
        assert blob2.track.name == track.name

    def test_commit_operations(self, repo):
        """Test commit write/read."""
        commit = Commit(
            tree={},
            parent=None,
            message="Test commit",
            author="Test Author",
            committer="Test Committer"
        )

        commit_hash = write_object(repo, commit)

        # Read back
        commit2 = read_object(repo, commit_hash)
        assert isinstance(commit2, Commit)
        assert commit2.message == "Test commit"
        assert commit2.author == "Test Author"

    def test_create_tree_from_tracks(self, repo):
        """Test creating tree from tracks."""
        tracks = [
            Track("spotify:track:1", "Song 1", "Artist 1", "Album 1", 180000),
            Track("spotify:track:2", "Song 2", "Artist 2", "Album 2", 200000),
        ]

        tree = create_tree_from_tracks(repo, tracks)

        assert len(tree) == 2
        assert "spotify:track:1" in tree
        assert "spotify:track:2" in tree

    def test_get_commit_tree(self, repo):
        """Test getting tracks from commit."""
        tracks = [
            Track("spotify:track:1", "Song 1", "Artist 1", "Album 1", 180000),
            Track("spotify:track:2", "Song 2", "Artist 2", "Album 2", 200000),
        ]

        tree = create_tree_from_tracks(repo, tracks)
        commit = Commit(
            tree=tree,
            parent=None,
            message="Test",
            author="Test",
            committer="Test"
        )
        commit_hash = write_object(repo, commit)

        # Get tracks
        retrieved_tracks = get_commit_tree(repo, commit_hash)

        assert len(retrieved_tracks) == 2
        assert "spotify:track:1" in retrieved_tracks
        assert "spotify:track:2" in retrieved_tracks

    def test_find_common_ancestor(self, repo):
        """Test finding common ancestor."""
        # Create commit chain
        commit1 = Commit(tree={}, parent=None, message="C1", author="A", committer="A")
        hash1 = write_object(repo, commit1)

        commit2 = Commit(tree={}, parent=hash1, message="C2", author="A", committer="A")
        hash2 = write_object(repo, commit2)

        commit3 = Commit(tree={}, parent=hash2, message="C3", author="A", committer="A")
        hash3 = write_object(repo, commit3)

        # Branch from hash2
        commit4 = Commit(tree={}, parent=hash2, message="C4", author="A", committer="A")
        hash4 = write_object(repo, commit4)

        # Find common ancestor
        ancestor = find_common_ancestor(repo, hash3, hash4)
        assert ancestor == hash2
