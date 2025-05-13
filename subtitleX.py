print("🔧 Starting subtitleX.py...")

print("📦 Importing whisperx...")
import whisperx
print("📦 whisperx imported.")

import torch
import sys
import os

print("📁 Parsing command-line arguments...")
if len(sys.argv) != 3:
    print("❌ Usage: python subtitleX.py input.mp4 output.srt")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

print("📂 Input path:", input_path)
print("📂 Output path:", output_path)

device = "cpu"

try:
    print("🔧 Step 1: Loading WhisperX model (large-v2)...")
    model = whisperx.load_model("large-v2", device)
    print("✅ WhisperX model loaded.")

    print("🎧 Step 2: Loading audio...")
    audio = whisperx.load_audio(input_path)
    print("✅ Audio loaded.")

    print("🧠 Step 3: Transcribing...")
    result = model.transcribe(audio)
    print("✅ Transcription complete.")

    if not result.get("segments"):
        print("❌ No transcription segments found.")
        sys.exit(1)

    print("📐 Step 4: Loading alignment model...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    print("✅ Alignment model loaded.")

    print("🧩 Step 5: Aligning segments...")
    aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device)
    print("✅ Alignment complete.")

    if not aligned_result.get("segments"):
        print("❌ No aligned segments found after alignment.")
        sys.exit(1)

    print("💾 Step 6: Writing SRT file...")
    with open(output_path, "w", encoding="utf-8") as srt:
        for i, seg in enumerate(aligned_result["segments"], 1):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()

            start_time = f"{int(start//3600):02}:{int((start%3600)//60):02}:{int(start%60):02},{int((start%1)*1000):03}"
            end_time = f"{int(end//3600):02}:{int((end%3600)//60):02}:{int(end%60):02},{int((end%1)*1000):03}"

            srt.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

    print(f"✅ Subtitle file successfully written to: {output_path}")

except Exception as e:
    print("❌ Exception caught in subtitleX.py:", str(e))
    sys.exit(1)
