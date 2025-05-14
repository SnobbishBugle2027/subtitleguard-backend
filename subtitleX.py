print("🚀 subtitleX.py has started...")

import sys
import os
import traceback

def exit_with_error(stage, error):
    print(f"❌ ERROR during {stage}:\n{error}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("📦 Importing whisperx...")
    import whisperx
    print("✅ whisperx imported successfully.")
except Exception as e:
    exit_with_error("import whisperx", e)

if len(sys.argv) != 3:
    print("❌ Usage: python subtitleX.py input.mp4 output.srt")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

try:
    print("🧠 Loading WhisperX model...")
    model = whisperx.load_model("large-v2", device="cpu")
    print("✅ Model loaded successfully.")
except Exception as e:
    exit_with_error("load_model", e)

try:
    print("🎧 Loading audio from:", input_path)
    audio = whisperx.load_audio(input_path)
    print("✅ Audio loaded.")
except Exception as e:
    exit_with_error("load_audio", e)

try:
    print("💬 Transcribing audio...")
    result = model.transcribe(audio)
    print("✅ Transcription complete.")
except Exception as e:
    exit_with_error("transcribe", e)

try:
    print("📐 Loading alignment model...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device="cpu")
    print("✅ Alignment model loaded.")
except Exception as e:
    exit_with_error("load_align_model", e)

try:
    print("🔄 Aligning segments...")
    aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device="cpu")
    print("✅ Alignment complete.")
except Exception as e:
    exit_with_error("align", e)

try:
    print("💾 Writing to SRT file:", output_path)
    with open(output_path, "w", encoding="utf-8") as srt:
        for i, seg in enumerate(aligned_result["segments"], 1):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()

            start_time = f"{int(start//3600):02}:{int((start%3600)//60):02}:{int(start%60):02},{int((start%1)*1000):03}"
            end_time = f"{int(end//3600):02}:{int((end%3600)//60):02}:{int(end%60):02},{int((end%1)*1000):03}"

            srt.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")
    print("✅ Subtitle file written successfully.")
except Exception as e:
    exit_with_error("write_srt", e)
