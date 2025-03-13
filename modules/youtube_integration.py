import youtube_dl
import os

def play_youtube_video(video_url):
    """Play a YouTube video using youtube-dl"""
    ydl_opts = {
        'format': 'bestaudio/best',  # Highest quality audio
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Save downloaded videos
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        video_url = info_dict.get("formats", [])[0].get("url", None)
        
        if video_url:
            os.system(f"vlc {video_url}")  # You can change this to use another media player
        else:
            print("Failed to find video URL")
