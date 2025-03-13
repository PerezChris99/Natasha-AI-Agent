"""
Spotify API configuration settings
"""

# Spotify API credentials
# Replace with your actual credentials from https://developer.spotify.com/dashboard
SPOTIPY_CLIENT_ID = "your_spotify_client_id"
SPOTIPY_CLIENT_SECRET = "your_spotify_client_secret"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

# Default playback settings
DEFAULT_DEVICE_NAME = "Your Speaker Device"  # Change to your preferred playback device
VOLUME_PERCENT = 50  # Default volume level (0-100)
