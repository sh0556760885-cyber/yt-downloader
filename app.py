from flask import Flask, request, jsonify
import subprocess
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get("url")

    if not url:
        return jsonify({"error": "No URL"}), 400

    filename = "video.mp4"

    # הורדה
    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", filename,
        url
    ])

    # התחברות לדרייב
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # העלאה
    file = drive.CreateFile({'title': filename})
    file.SetContentFile(filename)
    file.Upload()

    # קישור
    link = file['alternateLink']

    return jsonify({
        "status": "done",
        "link": link
    })

app.run(host="0.0.0.0", port=8080)
