import whisperx
import torch
import sys
import os

input_path = sys.argv[1]
output_path = sys.argv[2]

device = "cpu"

try:
    print("🔧 Loading model...")
    model = whisperx.load_model("large-v2", device)

    print("📥 Loading audio...")
    audio = whisperx.load_audio(input_path)

    print("🧠 Transcribing...")
    result = model.transcribe(audio)

    if "segments" not in result or not result["segments"]:
        print("❌ No segments found — skipping subtitle generation.")
        sys.exit(1)

    print("📐 Aligning...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result_aligned = whisperx.align(result["segments"], model_a, metadata, audio, device)

    print("💾 Writing SRT...")
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(result_aligned["segments"], 1):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            start_time = f"{int(start//3600):02}:{int((start%3600)//60):02}:{int(start%60):02},{int((start%1)*1000):03}"
            end_time = f"{int(end//3600):02}:{int((end%3600)//60):02}:{int(end%60):02},{int((end%1)*1000):03}"

            f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

    print("✅ Subtitle generation complete.")

except Exception as e:
    print("❌ WhisperX crashed:", e)
    sys.exit(1)
