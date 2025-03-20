from youtube_search import YoutubeSearch
import webbrowser

class YouTubeController:
    def play_video(self, query):
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            if results:
                video_url = f"https://youtube.com{results[0]['url_suffix']}"
                webbrowser.open(video_url)
                return f"Playing {results[0]['title']} on YouTube"
            return "Video not found"
        except Exception as e:
            return f"Error playing video: {str(e)}"
