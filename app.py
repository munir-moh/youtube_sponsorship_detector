from typing import Optional
from flask import Flask, request
from markupsafe import Markup
import traceback
from youtube import get_youtube_videos
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel 
from datetime import datetime
import xml.etree.ElementTree as ET

app = Flask(__name__)

@CrewBase
class YoutubeSponsorshipDetector():
    """YoutubeSponsorshipDetector crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def sponsorship_detector(self) -> Agent:
        return Agent(
            config=self.agents_config['sponsorship_detector'],
            verbose=True, 
        )
    
    @task
    def sponsorship_detecting_task(self) -> Task:
        return Task(
            config=self.tasks_config['sponsorship_detecting_task'],
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=True,
        )

@app.route('/')
def home():
    YoutubeSponsorshipDetector().crew().kickoff(inputs={
        "description": "@nala.money - sure update for FX transfer this period and beyond. Download @nala.money app with my code SABINUS. use to send love home and get the “investor”.",
    })
    return "Hello, Flask!"

@app.route('/channels', methods=['GET'])
def confirm_channel_subscription():
    # Store channel from args, subscription time, expiry date into dynamodb table
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
        # print('doc', doc)
        publication = Publication.from_xml(doc)
        print(publication.id, publication.title, publication.publishedAt, publication.channel_id, publication.description)
        result = get_youtube_videos(publication.id)
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
    result = get_youtube_videos(publication_ids)
    return result, 200

class Publication(BaseModel): 
    id: str 
    title: str 
    publishedAt: datetime 
    channel_id: str
    description: Optional[str] = None

    @classmethod
    def from_xml(cls, xml_string: str) -> 'Publication':
        root = ET.fromstring(xml_string)
        entry = root.find("{http://www.w3.org/2005/Atom}entry")
        
        publication_data = {
            "id": entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text,
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
            "publishedAt": datetime.strptime(entry.find("{http://www.w3.org/2005/Atom}published").text, "%Y-%m-%dT%H:%M:%S%z"),
            "channel_id": entry.find("{http://www.youtube.com/xml/schemas/2015}channelId").text,
            "description": None  # Description is not available in the provided XML
        }
        return cls(**publication_data)

if __name__ == "__main__":
    app.run(debug=True)