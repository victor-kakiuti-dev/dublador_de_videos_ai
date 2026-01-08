import json
import subprocess
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import wave


# =========================
# ÁUDIO — UTILIDADES
# =========================

def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        return frames / float(rate)


def to_pcm_wav(src: Path, dst: Path):
    """
    Converte qualquer áudio para WAV PCM (mono, 16kHz)
    """
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(src),
            "-ac", "1",
            "-ar", "16000",
            "-sample_fmt", "s16",
            str(dst)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


def speedup_audio(src: Path, dst: Path, speed: float):
    """
    Acelera áudio mantendo pitch (ffmpeg atempo)
    """
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(src),
            "-filter:a", f"atempo={speed}",
            str(dst)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


# =========================
# DUBLAGEM PRINCIPAL
# =========================

def dubbing(json_ts: Path, out_dir: Path, output_json: Path):
    load_dotenv()

    out_dir.mkdir(parents=True, exist_ok=True)
    output_json.mkdir(parents=True, exist_ok=True)

    client = OpenAI()

    # -------------------------
    # Carrega timestamps ASR
    # -------------------------
    with open(json_ts, encoding="utf-8") as f:
        segments = json.load(f)

    timeline = 0.0
    fixed_segments = []

    for i, seg in enumerate(segments):
        text = seg.get("text", "").strip()

        if not text:
            continue

        orig_start = seg.get("start", timeline)
        orig_end = seg.get("end", orig_start)
        orig_dur = max(orig_end - orig_start, 0.1)

        print(f"🎙️ [{i:03d}] Gerando TTS")

        # -------------------------
        # Arquivos
        # -------------------------
        raw_audio = out_dir / f"{i:03d}.tmp"
        wav_audio = out_dir / f"{i:03d}.wav"

        # -------------------------
        # Gera TTS
        # -------------------------
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )

        response.stream_to_file(raw_audio)

        # -------------------------
        # Normaliza para WAV PCM
        # -------------------------
        to_pcm_wav(raw_audio, wav_audio)
        raw_audio.unlink(missing_ok=True)

        tts_dur = wav_duration(wav_audio)

        # -------------------------
        # Ajuste de velocidade se não couber
        # -------------------------
        if tts_dur > orig_dur:
            speed = tts_dur / orig_dur

            # limites humanos
            speed = min(max(speed, 1.0), 1.25)

            print(
                f"⚠️  [{i:03d}] TTS longo ({tts_dur:.2f}s) → "
                f"acelerando {speed:.2f}x para caber em {orig_dur:.2f}s"
            )

            sped_audio = out_dir / f"{i:03d}_spd.wav"
            speedup_audio(wav_audio, sped_audio, speed)

            wav_audio.unlink()
            sped_audio.rename(wav_audio)

            tts_dur = wav_duration(wav_audio)

        # -------------------------
        # Registra timeline FINAL
        # -------------------------
        fixed_segments.append({
            "index": i,
            "text": text,
            "audio": wav_audio.name,
            "start": timeline,
            "end": timeline + tts_dur
        })

        timeline += tts_dur + 0.08  # pausa segura

    # -------------------------
    # Salva timestamps finais
    # -------------------------
    final_json = output_json / "timestamps_final.json"
    with open(final_json, "w", encoding="utf-8") as f:
        json.dump(fixed_segments, f, ensure_ascii=False, indent=2)

    print("\n✔ DUBLAGEM FINALIZADA COM SUCESSO")
    print(f"📄 Timeline final: {final_json}")

