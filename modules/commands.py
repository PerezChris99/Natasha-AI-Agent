import webbrowser
import subprocess
import os

def perform_web_search(query):
    """Perform a Google search."""
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def open_application(app_name):
    """Open an application based on the user's command."""
    try:
        if app_name.lower() == "browser":
            # Example: Open the default web browser
            subprocess.run(["open", "-a", "Safari"])  # macOS example
            # For Windows, use: subprocess.run(["start", "chrome"]) or whatever app
        elif app_name.lower() == "music player":
            # Example: Open a media player (can customize to specific apps)
            subprocess.run(["open", "-a", "VLC"])  # Example for VLC on macOS
        else:
            print(f"Application '{app_name}' not recognized.")
    except Exception as e:
        print(f"Error opening application: {e}")

def play_media(media_name):
    """Play media from local files or streaming services."""
    media_file = f"/path/to/media/{media_name}.mp4"  # Adjust path based on file location
    if os.path.exists(media_file):
        subprocess.run(["open", media_file])  # Open the media file on macOS
        # For Windows: subprocess.run(["start", media_file])
    else:
        print("Media file not found.")
