import os
from hashlib import sha256
from flask import Flask, render_template, url_for, request, flash, redirect, abort, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "/home/theo/test"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
app.secret_key = os.urandom(16)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
            ["png", "jpg", "jpeg", "gif", "ico", "tif"]

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if allowed_file(file.filename) == False:
            return "Invalid file type"
        if file:
            tmpname = os.path.join("/home/theo/test/tmp", file.filename)
            extension = "." + file.filename.split(".")[1]
            file.save(tmpname)
            with open(tmpname, "rb") as f:
                filename = sha256(f.read()).hexdigest() + extension
            os.rename(tmpname, os.path.join(app.config["UPLOAD_FOLDER"], filename))
            url = "https://photohost.tech/view" + filename
                
            return redirect(url)
        else:
            return "An unknown error occurred"
    return render_template("index.html")

@app.route("/image/<filename>")
def return_image(filename):
    return send_from_directory("/home/theo/test/", filename, as_attachment=True)

@app.route("/view/<image>")
def view(image):
    return render_template("view.html", image=image)
