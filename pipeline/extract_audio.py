import subprocess
from pathlib import Path    #2


def extract_audio(
    video_path: Path,
    output_dir: Path,
    sample_rate: int = 16000
) -> Path:
    """
    Extrai áudio mono WAV 16kHz a partir de um vídeo.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / "audio_original.wav"

    command = [
        "ffmpeg",
        "-i", str(video_path),
        "-ac", "1",
        "-ar", str(sample_rate),
        "-sample_fmt", "s16",
        str(audio_path),
        "-y"
    ]

    subprocess.run(command, check=True)

    if not audio_path.exists():
        raise RuntimeError("Falha ao extrair áudio.")

    return audio_path
