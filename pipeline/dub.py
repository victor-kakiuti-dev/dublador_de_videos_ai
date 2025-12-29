import json
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# 6 faz dublagem dos timestamps e gera chunks de audio

def dubbing(json_ts, out_dir):
    load_dotenv()

    out_dir.mkdir(parents=True, exist_ok=True)

    client = OpenAI()
    

    # =========================
    # CARREGA TIMESTAMPS
    # =========================
    with open(json_ts, encoding="utf-8") as f:
        segments = json.load(f)


    # =========================
    # GERA TTS POR SEGMENTO
    # =========================
    for i, seg in enumerate(segments):
        text = seg.get("text", "").strip()

        if not text:
            print(f"[{i:03d}] texto vazio — pulando")
            continue


        out_audio = out_dir / f"{i:03d}.wav"


        print(f"🎙️ Gerando TTS {out_audio.name}")


        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",          # pode trocar depois
            input=text
        )

        # salva o áudio no disco
        try:
            response.stream_to_file(out_audio)
        except Exception as e:
            print(e)
        print('salvei')

    print("\n✔ TTS gerado com sucesso em output/chuncks/")
