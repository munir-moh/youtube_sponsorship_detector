from flask import Flask, request
from markupsafe import Markup
import traceback
from youtube import YouTubeAPI
from dataclass.publication import Publication
from agents.detector.detector import YoutubeSponsorshipDetector

app = Flask(__name__)

youtube_api = YouTubeAPI()

@app.route('/')
def home():
    # YoutubeSponsorshipDetector().crew().kickoff(inputs={
    #     "description": "@nala.money - sure update for FX transfer this period and beyond. Download @nala.money app with my code SABINUS. use to send love home and get the “investor”.",
    # })
    return "Hello, Flask!"

@app.route('/channels', methods=['GET'])
def confirm_channel_subscription():
    channel_id = request.args.get('hub.topic').split("channel_id=")[1]
    lease_seconds = request.args.get('hub.lease_seconds')
    challenge = request.args.get('hub.challenge')
    challenge_escaped = str(Markup.escape(challenge))
    return challenge_escaped

@app.route('/channels', methods=['POST'])
def detect_publication():
    doc = request.data
    doc = doc.decode('utf-8')
    try:
        publication = Publication.from_xml(doc)
        print(publication.id, publication.title, publication.publishedAt, publication.channel_id, publication.description)
        result = youtube_api.get_youtube_videos(publication.id)
        description = result['items'][0]['snippet']['description']
        publication.description = description
        print(publication.id, publication.title, publication.publishedAt, publication.channel_id, publication.description)
        YoutubeSponsorshipDetector().crew().kickoff(inputs={
            "description": publication.description,
    })
    except AttributeError:
        print('Failed to unpack attributes')
        print(traceback.format_exc())
        print('request', doc)
    except Exception:
        print("* captured exception *")
        print(traceback.format_exc())
        return "exception", 500

    return "", 200

@app.route('/youtube-pubications', methods=['GET'])
def publications():
    publication_ids = request.args.get('publication_ids')
    result = youtube_api.get_youtube_videos(publication_ids)
    return result, 200

if __name__ == "__main__":
    app.run(debug=True)