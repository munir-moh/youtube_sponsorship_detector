import os
import requests
from dotenv import load_dotenv

load_dotenv()

class YouTubeAPI:
    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("No API key found in environment variables")

    def get_youtube_videos(self, publication_ids: str) -> dict:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part" : "snippet,statistics",
            "id" : publication_ids,
            "key" : self.api_key
        }
        r = requests.get(url, params=params)
        return r.json()