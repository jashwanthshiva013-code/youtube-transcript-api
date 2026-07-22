from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/")
def home():
    return {"message": "YouTube Transcript API is running"}

@app.get("/transcript")
def transcript(videoId: str):
    api = YouTubeTranscriptApi()
    transcript = api.fetch(videoId)

    text = " ".join([item.text for item in transcript])

    return {
        "videoId": videoId,
        "transcript": text
    }
