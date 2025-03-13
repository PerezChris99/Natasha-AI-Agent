import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Import credentials from config or environment variables
from config.spotify_config import (
    SPOTIPY_CLIENT_ID, 
    SPOTIPY_CLIENT_SECRET, 
    SPOTIPY_REDIRECT_URI,
    DEFAULT_DEVICE_NAME,
    VOLUME_PERCENT
)

# Override with environment variables if available
client_id = os.environ.get('SPOTIPY_CLIENT_ID', SPOTIPY_CLIENT_ID)
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET', SPOTIPY_CLIENT_SECRET)
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI', SPOTIPY_REDIRECT_URI)

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-read-playback-state,user-modify-playback-state"
))

def play_spotify_track(track_name, artist_name=None):
    """
    Play a track on Spotify
    
    Args:
        track_name (str): Name of the track to play
        artist_name (str, optional): Artist name to refine search
    
    Returns:
        bool: True if playback started successfully, False otherwise
    """
    try:
        # Build search query
        query = f"track:{track_name}"
        if artist_name:
            query += f" artist:{artist_name}"
        
        # Search for the track
        results = sp.search(q=query, type="track", limit=1)
        
        if not results['tracks']['items']:
            print(f"No track found for '{track_name}'")
            return False
        
        # Get the first track URI
        track_uri = results['tracks']['items'][0]['uri']
        
        # Get available devices
        devices = sp.devices()
        
        # Try to find the default device
        device_id = None
        for device in devices['devices']:
            if DEFAULT_DEVICE_NAME.lower() in device['name'].lower():
                device_id = device['id']
                break
        
        # Start playback on the found device or default device
        sp.start_playback(device_id=device_id, uris=[track_uri])
        sp.volume(volume_percent=VOLUME_PERCENT, device_id=device_id)
        
        track_info = results['tracks']['items'][0]
        print(f"Now playing: {track_info['name']} by {track_info['artists'][0]['name']}")
        return True
        
    except Exception as e:
        print(f"Error playing Spotify track: {e}")
        return False
