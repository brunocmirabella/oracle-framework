#!/usr/bin/env python3
"""
oracle_tts.py — Voice reply generator for Oracle
Converts text to OGG Opus audio for Telegram voice messages.

Requirements:
    pip install edge-tts
    ffmpeg (system install — must be in PATH)

Usage:
    python oracle_tts.py "Text to speak"
    python oracle_tts.py "Hello" --voice en-US-AriaNeural --out /tmp/reply.ogg

Output:
    Prints the absolute path to the generated OGG file (for use in Telegram reply).

Full voice list:
    edge-tts --list-voices

Common voices:
    English:  en-US-AriaNeural, en-US-GuyNeural, en-GB-SoniaNeural
    Italian:  it-IT-IsabellaNeural, it-IT-DiegoNeural
    Spanish:  es-ES-ElviraNeural, es-MX-DaliaNeural
    French:   fr-FR-DeniseNeural
    German:   de-DE-KatjaNeural
"""

import asyncio
import sys
import subprocess
import argparse
import tempfile
from pathlib import Path

# --- Default configuration (override via CLI args or edit here) ---
DEFAULT_VOICE = "en-US-AriaNeural"   # change to match your language
DEFAULT_OUTPUT = Path(__file__).parent / "audio" / "oracle_reply.ogg"
# -----------------------------------------------------------------


async def _synthesize(text: str, voice: str, mp3_path: Path) -> None:
    try:
        import edge_tts
    except ImportError:
        print("edge-tts not installed. Run: pip install edge-tts", file=sys.stderr)
        sys.exit(1)

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(mp3_path))


def text_to_ogg(text: str, voice: str = DEFAULT_VOICE, output: Path = DEFAULT_OUTPUT) -> Path:
    """Convert text to OGG Opus audio file. Returns the output path."""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        mp3_path = Path(tmp.name)

    try:
        asyncio.run(_synthesize(text, voice, mp3_path))

        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(mp3_path),
                "-c:a", "libopus",
                "-b:a", "64k",
                str(output),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"ffmpeg error: {result.stderr}", file=sys.stderr)
            sys.exit(1)
    finally:
        mp3_path.unlink(missing_ok=True)

    return output.resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Oracle TTS — text to OGG Opus")
    parser.add_argument("text", nargs="+", help="Text to synthesize")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Edge TTS voice name")
    parser.add_argument("--out", default=str(DEFAULT_OUTPUT), help="Output OGG file path")
    args = parser.parse_args()

    text = " ".join(args.text)
    output = text_to_ogg(text, voice=args.voice, output=Path(args.out))
    print(str(output))


if __name__ == "__main__":
    main()
