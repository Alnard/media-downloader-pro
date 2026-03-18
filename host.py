from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

DOWNLOAD_PATH = "/tmp"  # Railway won't allow writing to /sdcard

progress = {"percent": 0, "status": "idle"}

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    global progress
    data = request.json
    url = data.get("url")
    quality = data.get("quality")

    if not url:
        return jsonify({"status": "error", "msg": "No URL provided"})

    progress = {"percent": 0, "status": "downloading"}

    if quality == "mp3":
        cmd = f'yt-dlp -x --audio-format mp3 -o "{DOWNLOAD_PATH}/%(title)s.%(ext)s" "{url}"'
    else:
        fmt = "bestvideo[height<=720]+bestaudio/best" if quality=="720" else "bestvideo[height<=360]+bestaudio/best" if quality=="360" else "best"
        cmd = f'yt-dlp -f "{fmt}" -o "{DOWNLOAD_PATH}/%(title)s.%(ext)s" "{url}"'

    os.system(cmd)
    progress["status"] = "done"
    return jsonify({"status": "done"})

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
