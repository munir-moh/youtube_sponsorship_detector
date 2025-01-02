import requests

API_KEY = "AIzaSyDRwxYpoHkaYyHuePOsajLUrCHe-OVJs9M" 

# url = "https://www.googleapis.com/youtube/v3/videos"
# params = {
#     "part" : "snippet",
#     "id" : "3w3uuvkEakY",
#     # "maxResults" : 25,
#     "key" : API_KEY
# }

# r = requests.get(url, params=params)

# print(r.json())

def get_youtube_videos(publication_ids: str) -> dict:
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part" : "snippet,statistics",
        "id" : publication_ids,
        "key" : API_KEY
    }
    r = requests.get(url, params=params)
    return r.json()