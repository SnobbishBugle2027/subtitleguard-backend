from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import uuid
import shutil
import subprocess

app = FastAPI()

@app.get("/")
def health():
    return {"status": "SubtitleGuard backend is running"}

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    print("🚀 Received file:", file.filename)

    os.makedirs("temp", exist_ok=True)
    uid = str(uuid.uuid4())
    input_path = f"temp/{uid}.mp4"
    output_path = f"temp/{uid}.srt"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("⚙️ Running subtitleX.py...")

    result = subprocess.run(
        ["python", "subtitleX.py", input_path, output_path],
        capture_output=True,
        text=True
    )

    print("📤 STDOUT:\n", result.stdout)
    print("⚠️ STDERR:\n", result.stderr)

    if not os.path.exists(output_path):
        raise RuntimeError("❌ Subtitle file not generated.")

    return FileResponse(output_path, filename="subtitles.srt", media_type="application/x-subrip")
