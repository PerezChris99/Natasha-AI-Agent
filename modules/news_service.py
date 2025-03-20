import requests
import os

class NewsService:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def get_news_brief(self, category="general", count=5):
        try:
            params = {
                'category': category,
                'apiKey': self.api_key,
                'language': 'en',
                'pageSize': count
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                news_items = data['articles'][:count]
                brief = "Here are the top headlines:\n"
                for idx, item in enumerate(news_items, 1):
                    brief += f"{idx}. {item['title']}\n"
                return brief
            return "Sorry, I couldn't fetch the news."
        except Exception as e:
            return f"Error getting news: {str(e)}"
