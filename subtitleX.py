import whisperx
import torch
import sys
import os

# Ensure correct usage
if len(sys.argv) != 3:
    print("❌ Usage: python subtitleX.py input.mp4 output.srt")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]
device = "cpu"

print("📂 Input Path:", input_path)
print("📂 Output Path:", output_path)

try:
    print("🔧 Step 1: Loading WhisperX ASR model...")
    model = whisperx.load_model("large-v2", device)

    print("🎧 Step 2: Loading audio...")
    audio = whisperx.load_audio(input_path)

    print("🧠 Step 3: Transcribing with WhisperX...")
    result = model.transcribe(audio)

    if not result.get("segments"):
        print("❌ No segments returned from transcription.")
        sys.exit(1)

    print("📐 Step 4: Loading alignment model...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    print("🧩 Step 5: Performing alignment...")
    try:
        aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device)
    except Exception as e:
        print("❌ WhisperX alignment failed:", e)
        sys.exit(1)

    if not aligned_result.get("segments"):
        print("❌ Alignment succeeded but no segments returned.")
        sys.exit(1)

    print("💾 Step 6: Writing SRT file...")
    try:
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
        print("❌ Failed to write subtitle file:", e)
        sys.exit(1)

except Exception as e:
    print("❌ Fatal WhisperX error:", e)
    sys.exit(1)
