from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL
import os
import re
import glob

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API Running"}

@app.get("/transcript")
def get_transcript(url: str):

    output_dir = "subtitles"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": os.path.join(output_dir, "%(id)s"),
        "quiet": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        title = info.get("title", "Unknown Title")

        files = glob.glob(os.path.join(output_dir, "*.en.vtt"))

        if not files:
            raise HTTPException(status_code=404, detail="No English subtitles found.")

        subtitle_file = files[0]

        transcript = ""

        with open(subtitle_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if (
                    not line
                    or line.startswith("WEBVTT")
                    or "-->" in line
                    or re.match(r"^\d+$", line)
                ):
                    continue

                line = re.sub(r"<.*?>", "", line)
                transcript += line + " "

        os.remove(subtitle_file)

        return {
            "title": title,
            "transcript": transcript.strip()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
