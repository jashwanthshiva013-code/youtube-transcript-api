from fastapi import FastAPI
from yt_dlp import YoutubeDL

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API Running"}


@app.get("/transcript")
def transcript(url: str):

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "description": info.get("description"),
        "duration": info.get("duration"),
    }
