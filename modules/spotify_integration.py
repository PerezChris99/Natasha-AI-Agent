import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Setup for Spotify Authentication
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                client_secret=SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                                scope="user-library-read user-read-playback-state user-modify-playback-state"))

def play_spotify_track(track_name):
    """Search and play a track on Spotify"""
    results = sp.search(q=track_name, limit=1, type='track')
    track_uri = results['tracks']['items'][0]['uri']
    sp.start_playback(uris=[track_uri])
    print(f"Now playing: {track_name}")
