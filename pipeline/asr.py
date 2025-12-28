from pathlib import Path
from openai import OpenAI
import json
from pathlib import Path
from dotenv import load_dotenv

# 5 Coloca o texto nas timestamps

def asr_on(vad_path, chunks_dir, asr_output):
    load_dotenv()

    client = OpenAI()

    def transcribe_chunk(chunk_path: Path) -> str:
        with open(chunk_path, "rb") as f:
            result = client.audio.transcriptions.create(
                file=f,
                model="whisper-1",
                language="pt"
            )
        return result.text.strip()


    # caminhos


    asr_output.parent.mkdir(parents=True, exist_ok=True)

    # carregar VAD final
    with open(vad_path, "r", encoding="utf-8") as f:
        merged = json.load(f)

    asr_results = []

    chunks_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        for i, seg in enumerate(merged):
            chunk_path = chunks_dir / f"chunk_{i:03d}.wav"

            if not chunk_path.exists():
                print('parei aqui')
                continue

            text = transcribe_chunk(chunk_path)

            if not text:
                continue

            asr_results.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": text
            })
    except Exception as e:
        print(e)

    # salvar resultado final do ASR
    with open(asr_output, "w", encoding="utf-8") as f:
        json.dump(asr_results, f, ensure_ascii=False, indent=2)

    print('ASR COMPLETE')
