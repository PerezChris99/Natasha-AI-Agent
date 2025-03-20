import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            scope="user-modify-playback-state user-read-playback-state"
        ))

    def play_song(self, song_name):
        try:
            results = self.sp.search(q=song_name, type='track', limit=1)
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                self.sp.start_playback(uris=[track_uri])
                return f"Playing {results['tracks']['items'][0]['name']}"
            return "Song not found"
        except Exception as e:
            return f"Error playing song: {str(e)}"
