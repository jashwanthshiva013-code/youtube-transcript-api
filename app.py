from fastapi import FastAPI
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

@app.get("/")
def home():
    return {"message": "YouTube Transcript API is running"}

@app.get("/transcript")
def transcript(videoId: str):
    data = YouTubeTranscriptApi.get_transcript(videoId)
    text = " ".join([item["text"] for item in data])
    return {
        "videoId": videoId,
        "transcript": text
    }
