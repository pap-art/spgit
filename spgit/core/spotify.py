"""
Spotify API integration for spgit.
Handles authentication and playlist operations.
"""

import os
import json
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse, parse_qs

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    SPOTIPY_AVAILABLE = True
except ImportError:
    SPOTIPY_AVAILABLE = False

from .objects import Track


class SpotifyClient:
    """Wrapper for Spotify API operations."""

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        """
        Initialize Spotify client.

        Args:
            client_id: Spotify client ID
            client_secret: Spotify client secret
        """
        if not SPOTIPY_AVAILABLE:
            raise ImportError("spotipy is not installed. Install it with: pip install spotipy")

        self.client_id = client_id or os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIPY_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not configured. Run 'spgit config' to set them up.")

        # Use a reasonable cache path
        cache_path = Path.home() / ".spgit" / ".cache-spotipy"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri="http://localhost:8888/callback",
                scope="playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private",
                cache_path=str(cache_path)
            )
        )

    def get_playlist_id(self, url_or_id: str) -> str:
        """
        Extract playlist ID from URL or return ID if already an ID.

        Args:
            url_or_id: Playlist URL or ID

        Returns:
            Playlist ID
        """
        if url_or_id.startswith("http"):
            parsed = urlparse(url_or_id)
            # URL format: https://open.spotify.com/playlist/PLAYLIST_ID
            parts = parsed.path.split("/")
            if "playlist" in parts:
                return parts[parts.index("playlist") + 1].split("?")[0]
        return url_or_id

    def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """
        Get playlist metadata.

        Args:
            playlist_id: Playlist ID

        Returns:
            Playlist metadata
        """
        return self.sp.playlist(playlist_id)

    def get_playlist_tracks(self, playlist_id: str) -> List[Track]:
        """
        Get all tracks from a playlist.

        Args:
            playlist_id: Playlist ID

        Returns:
            List of Track objects
        """
        tracks = []
        offset = 0
        limit = 100

        while True:
            results = self.sp.playlist_items(
                playlist_id,
                offset=offset,
                limit=limit,
                fields="items(track(uri,name,artists,album,duration_ms),added_at,added_by.id),next"
            )

            for item in results["items"]:
                if not item["track"]:
                    continue

                track_data = item["track"]
                artists = ", ".join([artist["name"] for artist in track_data.get("artists", [])])

                track = Track(
                    uri=track_data["uri"],
                    name=track_data["name"],
                    artist=artists,
                    album=track_data.get("album", {}).get("name", "Unknown"),
                    duration_ms=track_data.get("duration_ms", 0),
                    added_at=item.get("added_at"),
                    added_by=item.get("added_by", {}).get("id")
                )
                tracks.append(track)

            if not results["next"]:
                break

            offset += limit

        return tracks

    def create_playlist(self, name: str, description: str = "", public: bool = True) -> str:
        """
        Create a new playlist.

        Args:
            name: Playlist name
            description: Playlist description
            public: Whether playlist is public

        Returns:
            Playlist ID
        """
        user_id = self.sp.current_user()["id"]
        playlist = self.sp.user_playlist_create(
            user_id,
            name,
            public=public,
            description=description
        )
        return playlist["id"]

    def update_playlist(self, playlist_id: str, tracks: List[Track]) -> None:
        """
        Update a playlist with new tracks (replaces all tracks).

        Args:
            playlist_id: Playlist ID
            tracks: List of Track objects
        """
        # Clear existing tracks
        self.sp.playlist_replace_items(playlist_id, [])

        # Add tracks in batches of 100 (Spotify API limit)
        track_uris = [track.uri for track in tracks]
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i + 100]
            self.sp.playlist_add_items(playlist_id, batch)
            time.sleep(0.1)  # Rate limiting

    def add_tracks(self, playlist_id: str, tracks: List[Track]) -> None:
        """
        Add tracks to a playlist.

        Args:
            playlist_id: Playlist ID
            tracks: List of Track objects to add
        """
        track_uris = [track.uri for track in tracks]
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i + 100]
            self.sp.playlist_add_items(playlist_id, batch)
            time.sleep(0.1)

    def remove_tracks(self, playlist_id: str, tracks: List[Track]) -> None:
        """
        Remove tracks from a playlist.

        Args:
            playlist_id: Playlist ID
            tracks: List of Track objects to remove
        """
        track_uris = [track.uri for track in tracks]
        for i in range(0, len(track_uris), 100):
            batch = track_uris[i:i + 100]
            self.sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)
            time.sleep(0.1)

    def search_track(self, query: str, limit: int = 10) -> List[Track]:
        """
        Search for tracks.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of Track objects
        """
        results = self.sp.search(q=query, type="track", limit=limit)
        tracks = []

        for item in results["tracks"]["items"]:
            artists = ", ".join([artist["name"] for artist in item["artists"]])
            track = Track(
                uri=item["uri"],
                name=item["name"],
                artist=artists,
                album=item["album"]["name"],
                duration_ms=item["duration_ms"]
            )
            tracks.append(track)

        return tracks


def get_spotify_client(repo=None) -> SpotifyClient:
    """
    Get a Spotify client instance using credentials from config.

    Args:
        repo: Repository instance (optional)

    Returns:
        SpotifyClient instance
    """
    # Try to get credentials from global config
    global_config_path = Path.home() / ".spgit" / "config"
    client_id = None
    client_secret = None

    if global_config_path.exists():
        with open(global_config_path, "r") as f:
            config = json.load(f)
            client_id = config.get("spotify", {}).get("client_id")
            client_secret = config.get("spotify", {}).get("client_secret")

    # Try repo config if available
    if repo and not (client_id and client_secret):
        repo_config = repo.read_config()
        client_id = client_id or repo_config.get("spotify", {}).get("client_id")
        client_secret = client_secret or repo_config.get("spotify", {}).get("client_secret")

    return SpotifyClient(client_id, client_secret)
