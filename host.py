from flask import Flask, request, jsonify, send_file
import subprocess
import os
import glob

app = Flask(__name__)

DOWNLOAD_PATH = "/tmp"  # use temp folder on cloud server

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get("url")
    quality = data.get("quality")

    if not url:
        return jsonify({"status": "error", "msg": "No URL provided"})

    # Unique filename
    filename = f"{DOWNLOAD_PATH}/file_%(id)s.%(ext)s"

    # MUSIC
    if quality == "mp3":
        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "-o", filename,
            url
        ]
    else:
        if quality == "720":
            fmt = "bestvideo[height<=720]+bestaudio/best"
        elif quality == "360":
            fmt = "bestvideo[height<=360]+bestaudio/best"
        else:
            fmt = "best"

        cmd = [
            "yt-dlp",
            "-f", fmt,
            "-o", filename,
            url
        ]

    try:
        subprocess.run(cmd, check=True)

        # Find downloaded file
        files = glob.glob(f"{DOWNLOAD_PATH}/file_*")
        latest = max(files, key=os.path.getctime)

        return send_file(latest, as_attachment=True)

    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
