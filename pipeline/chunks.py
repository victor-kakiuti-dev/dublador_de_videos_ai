import json
from pathlib import Path
from pydub import AudioSegment


def cut_audio_by_timestamps(
    audio_path: Path,
    timestamps_path: Path,
    chunks_dir: Path,
    prefix: str = "chunk"
):
    """
    Lê timestamps (start/end em segundos) e
    corta o áudio original em chunks WAV.
    """

    # carregar áudio
    audio = AudioSegment.from_file(audio_path)

    # carregar timestamps
    with open(timestamps_path, "r", encoding="utf-8") as f:
        segments = json.load(f)

    # garantir diretório
    chunks_dir.mkdir(parents=True, exist_ok=True)

    for i, seg in enumerate(segments):
        start_ms = int(seg["start"] * 1000)
        end_ms = int(seg["end"] * 1000)

        if end_ms <= start_ms:
            print(f"Segmento inválido {i}, pulando")
            continue

        chunk = audio[start_ms:end_ms]

        out_path = chunks_dir / f"{prefix}_{i:03d}.wav"
        chunk.export(out_path, format="wav")

        print(f"Gerado: {out_path}")
