from flask import Flask, render_template, request, send_file, redirect, url_for
import subprocess
import os
from pathlib import Path
import threading
from threading import Thread
import uuid
import shutil

jobs = {}


app = Flask(__name__)

FINAL_VIDEO_NAME = "video_final.mp4"

BASE_DIR = Path(__file__).resolve().parent


def run_pipeline_bg(job_id, video_url):
    try:
        jobs[job_id] = "processing"

        subprocess.run(
            ["python", "-m", "pipeline.run_pipeline", "--url", video_url],
            check=True
        )

        jobs[job_id] = "done"

    except Exception as e:
        jobs[job_id] = "error"
        print("Erro no pipeline:", e)


@app.route("/")
def index():
    video_path = BASE_DIR / FINAL_VIDEO_NAME
    output_path = BASE_DIR/'output'

    if output_path.exists():
        shutil.rmtree(output_path)

    if video_path.exists():
        try:
            video_path.unlink()
        except Exception as e:
            print("Erro ao apagar vídeo antigo:", e)
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    video_url = request.form["video_url"]
    job_id = str(uuid.uuid4())

    Thread(
        target=run_pipeline_bg,
        args=(job_id, video_url),
        daemon=True
    ).start()

    return redirect(url_for("status", job_id=job_id))

@app.route("/status/<job_id>")
def status(job_id):
    status = jobs.get(job_id, "unknown")

    return render_template(
        "status.html",
        status=status,
        job_id=job_id
    )

@app.route("/download/<filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=False)
