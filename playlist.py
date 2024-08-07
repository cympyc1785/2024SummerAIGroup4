from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# load .env
load_dotenv()

API_KEY = os.environ.get('API_KEY')

def call():
    print("hello")

# Replace with your Spotify Developer credentials
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000'

# Spotify scope for accessing user's playlists
SCOPE = 'playlist-read-private playlist-read-collaborative'

def get_user_playlists():
    # Initialize Spotipy client with OAuth
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                   client_secret=CLIENT_SECRET,
                                                   redirect_uri=REDIRECT_URI,
                                                   scope=SCOPE))

    # Get current user's playlists
    playlists = sp.current_user_playlists()

    print(playlists)

    # Extract and print playlist names and their URLs
    for playlist in playlists['items']:
        print(f"Playlist Name: {playlist['name']}")
        print(f"Playlist URL: {playlist['external_urls']['spotify']}")
        print(f"Total Tracks: {playlist['tracks']['total']}")
        print('-' * 30)

if __name__ == "__main__":
    get_user_playlists()