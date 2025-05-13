from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid
import shutil
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "SubtitleGuard backend is running"}

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    print(f"🚀 Received file: {file.filename}")

    # Create temp directory
    os.makedirs("temp", exist_ok=True)

    # Generate unique filenames
    uid = str(uuid.uuid4())
    input_path = f"temp/{uid}.mp4"
    output_path = f"temp/{uid}.srt"

    # Save uploaded file to disk
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("📁 Saved video to:", input_path)

    # Log working directory and file structure
    print("📂 Current directory:", os.getcwd())
    print("📄 Files in directory:", os.listdir())

    # Build command to run subtitleX.py
    command = ["python", "subtitleX.py", input_path, output_path]
    print("🧪 Running command:", command)

    # Run the subtitleX script and capture output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Log all subprocess output
    print("📤 STDOUT:\n", result.stdout)
    print("⚠️ STDERR:\n", result.stderr)

    # Check if subtitle file was created
    if not os.path.exists(output_path):
        print("❌ subtitleX.py did not create an .srt file.")
        raise RuntimeError("❌ Subtitle file not generated.")

    print(f"✅ Returning subtitle file: {output_path}")
    return FileResponse(path=output_path, filename="subtitles.srt", media_type="application/x-subrip")
