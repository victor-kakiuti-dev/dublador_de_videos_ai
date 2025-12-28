import json
import subprocess
from pathlib import Path

def end_pipeline(video, json_ts, audio_dir, out):
    if not video.exists():
        raise FileNotFoundError(f"Vídeo não encontrado: {video}")

    if not json_ts.exists():
        raise FileNotFoundError(f"Timestamps não encontrados: {json_ts}")

    if not audio_dir.exists():
        raise FileNotFoundError(f"Pasta de áudios não encontrada: {audio_dir}")

    # =========================
    # CARREGA TIMESTAMPS
    # =========================
    with open(json_ts, encoding="utf-8") as f:
        segments = json.load(f)

    # =========================
    # CARREGA ÁUDIOS (chunks)
    # =========================
    audio_files = sorted(
        list(audio_dir.glob("*.wav")) + list(audio_dir.glob("*.mp3"))
    )

    if len(audio_files) == 0:
        raise RuntimeError("Nenhum áudio encontrado em output/chuncks")

    if len(audio_files) != len(segments):
        raise ValueError(
            f"Quantidade de áudios ({len(audio_files)}) "
            f"≠ quantidade de timestamps ({len(segments)})"
        )

    # =========================
    # MONTA COMANDO FFMPEG
    # =========================
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", video.as_posix()
    ]

    filter_parts = []

    # 🔉 Abaixa áudio original do vídeo
    filter_parts.append("[0:a]volume=0.3[aorig]")
    amix_inputs = ["[aorig]"]

    # 🔊 Processa cada chunk de dublagem
    for i, (seg, audio_file) in enumerate(zip(segments, audio_files)):
        start = float(seg["start"])
        delay_ms = int(start * 1000)

        ffmpeg_cmd += ["-i", audio_file.as_posix()]

        filter_parts.append(
            f"[{i+1}:a]adelay={delay_ms}|{delay_ms},volume=2.1[a{i}]"
        )
        amix_inputs.append(f"[a{i}]")

    # 🔀 Mixagem final
    filter_complex = (
        ";".join(filter_parts)
        + ";"
        + "".join(amix_inputs)
        + f"amix=inputs={len(amix_inputs)}:normalize=0[aout]"
    )

    ffmpeg_cmd += [
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        out.as_posix()
    ]

    # =========================
    # EXECUÇÃO
    # =========================
    print("\nExecutando FFmpeg:\n")
    print(" ".join(ffmpeg_cmd), "\n")

    subprocess.run(ffmpeg_cmd, check=True)

    print("✔ Vídeo final gerado com dublagem alinhada:")
    print(out)

