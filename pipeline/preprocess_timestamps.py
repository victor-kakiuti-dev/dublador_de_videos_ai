from pathlib import Path
import json

# 4 pre-processamento das timestamps para juntar intervalos menores que 0.5 segundos


# 1️⃣ Ler
def pre_process(output_json):
    
    output_json.mkdir(parents=True, exist_ok=True)

    with open(output_json, 'r', encoding='utf-8') as f:
        segments = json.load(f)

    # (opcional, mas recomendado)
    segments = sorted(segments, key=lambda x: x['start'])

    # 2️⃣ Processar
    max_gap = 0.5
    merged = []
    i = 0

    while i < len(segments):
        current = segments[i].copy()
        j = i + 1

        while j < len(segments):
            next_seg = segments[j]
            gap = next_seg['start'] - current['end']

            if gap <= max_gap:
                current['end'] = next_seg['end']
                j += 1
            else:
                break

        merged.append(current)
        i = j

    # 3️⃣ Escrever
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    
    print('PREPROCESS COMPLETE')

        