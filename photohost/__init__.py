import os
from flask import Flask, render_template, url_for, request, flash, redirect
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
            alert("No selected file")
            return "No selected file"
        if allowed_file(file.filename) == False:
            return "Invalid file type"
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return "Success"
        else:
            return "An unknown error occurred"
    return render_template("index.html")

