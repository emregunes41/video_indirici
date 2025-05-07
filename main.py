from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import yt_dlp
import os

app = FastAPI()

app.mount("/indirilenler", StaticFiles(directory="indirilenler"), name="indirilenler")
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/indir")
def indir(request: Request, video_url: str = Form(...), format: str = Form(...)):
    ydl_opts = {}
    if format == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'indirilenler/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    elif format == "mp4":
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'indirilenler/%(title)s.%(ext)s',
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
        if format == "mp3":
            filename = ydl.prepare_filename(info_dict)
            filename = os.path.splitext(filename)[0] + ".mp3"
        else:
            filename = ydl.prepare_filename(info_dict)

    return FileResponse(path=filename, filename=os.path.basename(filename), media_type='application/octet-stream')
