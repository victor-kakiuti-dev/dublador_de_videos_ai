import subprocess     # 1
from pathlib import Path


def download_video(url: str, output_dir: Path) -> Path:
    """
    Baixa um vídeo em MP4 usando yt-dlp, renomeia para video.mp4
    e retorna o caminho final.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = output_dir / "%(title)s.%(ext)s"

    command = [
        "yt-dlp",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "-o", str(output_template),
        url,
    ]

    subprocess.run(command, check=True)

    videos = list(output_dir.glob("*.mp4"))
    if not videos:
        raise RuntimeError("Nenhum vídeo MP4 foi baixado.")
    if len(videos) > 1:
        raise RuntimeError("Mais de um vídeo encontrado. Pipeline espera apenas um.")

    final_path = output_dir / "video.mp4"

    # remove arquivo antigo se existir (decisão explícita)
    if final_path.exists():
        final_path.unlink()

    videos[0].rename(final_path)

    return final_path

