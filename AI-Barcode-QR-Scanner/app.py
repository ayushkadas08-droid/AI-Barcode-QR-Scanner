import os
import sys
import subprocess
import time

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from scanner import scan_image
from ai import explain_scan
from config import DATA_FOLDER, DEBUG, UPLOAD_FOLDER
from services.history_service import get_recent_scans, init_history_db, save_scan_results

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "bmp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATA_FOLDER, exist_ok=True)
init_history_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    image = request.files.get("image")

    if not image or image.filename == "":
        return "No file selected."

    if not _is_allowed_file(image.filename):
        return "Please upload a valid image file."

    filename = _build_upload_filename(image.filename)
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(filepath)

    try:
        results = scan_image(filepath)
    except ValueError as error:
        return str(error)

    results = explain_scan(results)
    save_scan_results(filename, results)

    return render_template(
        "result.html",
        image=filename,
        results=results
    )


@app.route("/history")
def history():
    scans = get_recent_scans()
    return render_template("history.html", scans=scans)


@app.route("/webcam")
def webcam():

    subprocess.Popen([sys.executable, "webcam.py"])

    return render_template("webcam.html")


def _build_upload_filename(original_filename):
    filename = secure_filename(original_filename)

    if not filename:
        filename = "uploaded-image"

    timestamp = int(time.time())
    name, extension = os.path.splitext(filename)

    return f"{name}_{timestamp}{extension}"


def _is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=DEBUG)
