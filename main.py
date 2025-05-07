from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app.mount("/indirilenler", StaticFiles(directory="indirilenler"), name="indirilenler")
templates = Jinja2Templates(directory=".")

@app.get("/", response_class=HTMLResponse)
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Video indirici sitesi çalışıyor!"}

from fastapi import Form
from fastapi.responses import FileResponse
import yt_dlp

@app.post("/indir")
def indir(url: str = Form(...), format: str = Form(...)):
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
    elif format == "video":
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'indirilenler/%(title)s.%(ext)s',
        }
    else:
        return {"error": "Geçersiz format seçildi."}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        # mp3 formatı için uzantıyı düzeltelim
        if format == "mp3":
            filename = filename.rsplit('.', 1)[0] + '.mp3'

    return FileResponse(path=filename, filename=filename.split('/')[-1], media_type='application/octet-stream')
