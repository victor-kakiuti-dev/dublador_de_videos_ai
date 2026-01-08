from .downloader import download_video
from .extract_audio import extract_audio
from .vad import vad
from .preprocess_timestamps import pre_process
from .asr import asr_on
from .dub import dubbing
from .final import end_pipeline
from .chunks import cut_audio_by_timestamps
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEO_DIR = BASE_DIR / "output" / 'video_input'
AUDIO_DIR = BASE_DIR / 'output' / 'audio_input'
output_json = BASE_DIR / 'output' / 'timestamps' 
audio_path = BASE_DIR / 'output' / 'audio_input'/'audio_original.wav'

vad_path = BASE_DIR/'output'/'timestamps'/ 'timestamps.json'
chunks_dir = BASE_DIR/'output'/'chuncks'
asr_output = BASE_DIR/'output'/ 'asr' / 'asr_timestamps.json'

JSON_TS = BASE_DIR / "output" / "asr" / "timestamps_final.json"
OUT_DIR = BASE_DIR / "output" / "dub"

VIDEO = BASE_DIR / "output" / "video_input" / "video.mp4"
JSON_TS = BASE_DIR / "output" / "asr" / "asr_timestamps.json"
AUDIO_DIR_CHUNK = BASE_DIR / "output" / "dub"
OUT = BASE_DIR / "video_final.mp4"
output = BASE_DIR/ 'output'

def resetar_diretorio(diretorio: Path):
    shutil.rmtree(diretorio)


def main(url: str):

    video = download_video(
        url=url,
        output_dir=VIDEO_DIR
    )

    audio = extract_audio(
        video_path=video,
        output_dir=AUDIO_DIR
    )

    vad(BASE_DIR)

    pre_process(output_json)

    cut_audio_by_timestamps(audio_path,
    vad_path,
    chunks_dir)

    

    

    asr_on(vad_path, chunks_dir, asr_output)

    dubbing(JSON_TS, OUT_DIR, output_json)

    end_pipeline(VIDEO, JSON_TS, AUDIO_DIR_CHUNK, OUT)



    print("Pipeline concluído")

    resetar_diretorio(output)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    main(args.url)




# python -m pipeline.run_pipeline --url "https://www.youtube.com/watch?v=p7XRPGzL6kk"



