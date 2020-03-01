import os
from hashlib import sha256
from flask import Flask, render_template, url_for, request, flash, redirect, abort, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "/home/theo/test"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
            ["png", "jpg", "jpeg", "gif", "ico", "tif"]

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if allowed_file(file.filename) == False:
            return "Invalid file type"
        if file:
            filesplit = file.filename.split(".")
            filename = sha256(secure_filename(filesplit[0]).encode("utf8")).hexdigest() + "." + filesplit[1]
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return filename
        else:
            return "An unknown error occurred"
    return render_template("index.html")

@app.route("/<image>")
def view(image):
    try:
        return send_from_directory("/home/theo/test/", filename=image)
    except FileNotFoundError:
        abort(404)
