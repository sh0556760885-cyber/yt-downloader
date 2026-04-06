from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL"}), 400

    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", "video.mp4",
        url
    ])

    return jsonify({"status": "done"})

app.run(host="0.0.0.0", port=8080)
