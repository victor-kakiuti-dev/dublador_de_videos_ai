from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
from pathlib import Path
import json   # 3 cria o arquivo com timestamps sem legenda



def vad(base_dir):
  model = load_silero_vad()
  wav = read_audio(base_dir / 'output' / 'audio_input'/ 'audio_original.wav')
  speech_timestamps = get_speech_timestamps(
    wav,
    model,
    return_seconds=True,  # Return speech timestamps in seconds (default is samples)
  )

  print(speech_timestamps)



  output = base_dir/ 'output' / 'timestamps'

  output.mkdir(parents=True, exist_ok=True)

  output_json = output / "timestamps.json"



  with open(output_json, "w", encoding="utf-8") as f:
          json.dump(speech_timestamps, f, indent=2, ensure_ascii=False)
  
  print('VAD COMPLETE')



  