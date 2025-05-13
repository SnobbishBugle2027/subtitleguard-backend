import whisperx
import torch
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]

device = "cpu"  # Render only supports CPU

try:
    print("🔧 Step 1: Loading WhisperX model...")
    model = whisperx.load_model("large-v2", device)

    print("🎵 Step 2: Loading audio...")
    audio = whisperx.load_audio(input_path)

    print("📝 Step 3: Transcribing...")
    result = model.transcribe(audio, batch_size=16)

    print("🧩 Step 4: Loading align model...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)

    print("📐 Step 5: Aligning...")
    aligned_result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False
    )

    print("💾 Step 6: Writing SRT...")
    with open(output_path, "w", encoding="utf-8") as srt:
        for i, seg in enumerate(aligned_result["segments"], 1):
            start = seg["start"]
            end = seg["end"]
            text = seg["text"].strip()

            start_time = f"{int(start//3600):02}:{int((start%3600)//60):02}:{int(start%60):02},{int((start%1)*1000):03}"
            end_time = f"{int(end//3600):02}:{int((end%3600)//60):02}:{int(end%60):02},{int((end%1)*1000):03}"

            srt.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

    print("✅ Subtitle generation complete:", output_path)

except Exception as e:
    print("❌ ERROR:", e)
    raise
