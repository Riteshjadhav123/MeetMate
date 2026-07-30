import sys
import argparse
from pathlib import Path
import whisper

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def transcribe(input_file: str, model_size: str = "small", translate: bool = False, out_file: str = "outputs/meeting_transcript.txt"):
    audio_path = Path(input_file)
    if not audio_path.exists():
        raise FileNotFoundError(f"Input file not found: {audio_path}")

    print(f"Loading Whisper model: {model_size} (this may take a minute the first time)...")
    model = whisper.load_model(model_size)  # tiny/base/small/medium/large

    print(f"Transcribing {audio_path.name} ...")
    # fp16=False ensures CPU compatibility
    result = model.transcribe(str(audio_path), fp16=False, task="translate" if translate else "transcribe")

    text = result.get("text", "").strip()

    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")

    print(f"✅ Transcript saved to: {out_path.resolve()}")
    print("\n--- Transcript Preview ---")
    print(text[:500] + ("..." if len(text) > 500 else ""))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MeetMate (free) transcription with Whisper")
    parser.add_argument("--input", "-i", required=True, help="Path to audio file (mp3/wav/m4a/etc.)")
    parser.add_argument("--model", "-m", default="small", help="Whisper model: tiny/base/small/medium/large (default: small)")
    parser.add_argument("--translate", "-t", action="store_true", help="Translate to English (useful for Hindi/Marathi/Hinglish)")
    parser.add_argument("--out", "-o", default="outputs/meeting_transcript.txt", help="Output .txt file path")
    args = parser.parse_args()

    transcribe(args.input, model_size=args.model, translate=args.translate, out_file=args.out)
