import os
import shutil
import zipfile
import pathlib
from hashlib import sha256
from flask import Flask, render_template, url_for, request, flash, redirect, abort, send_from_directory
from werkzeug.exceptions import HTTPException
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "/media/drive/uploads"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
app.secret_key = os.urandom(16)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
            ["png", "jpg", "jpeg", "gif", "ico", "tif", "svg", "zip"]

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if allowed_file(file.filename) == False:
            return render_template("error.html", errno="Error: Invalid file type, please upload an image.")
        if file:
            extension = "." + file.filename.split(".")[1]
            if extension != ".zip": 
                tmpname = os.path.join(app.config["UPLOAD_FOLDER"]+"/tmp", secure_filename(file.filename))
                file.save(tmpname)
                with open(tmpname, "rb") as f:
                    filename = sha256(f.read()).hexdigest() + extension
                os.rename(tmpname, os.path.join(app.config["UPLOAD_FOLDER"], filename))
                url = "https://photohost.tech/view/" + filename
            else:
                zip = zipfile.ZipFile(file)
                tmpname = os.path.join(app.config["UPLOAD_FOLDER"]+"/tmp", secure_filename(file.filename))
                file.save(tmpname)
                with open(tmpname, "rb") as f:
                    foldername = "/"+sha256(f.read()).hexdigest()
                os.remove(tmpname)
                pathlib.Path(app.config["UPLOAD_FOLDER"]+foldername).mkdir(exist_ok=True)
                for i in zip.namelist():
                    if allowed_file(i) and i.split(".")[1] != "zip":
                        zip.extract(i,app.config["UPLOAD_FOLDER"]+foldername)

                url = "https://photohost.tech/multi" + foldername
                
            return redirect(url)
        else:
            return render_template("error.html", errno="An unkown error occurred.")
    return render_template("index.html")

@app.route("/image/<filename>")
def return_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)

@app.route("/multi/<folder>/<filename>")
def return_image_folder(folder, filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"]+"/"+folder, filename, as_attachment=False)

@app.route("/view/<image>")
def view(image):
    return render_template("view.html", image=image)

@app.route("/multi/<folder>")
def multi(folder):
    try:
        images = os.listdir(app.config["UPLOAD_FOLDER"]+"/"+folder)
    except FileNotFoundError:
        abort(404)
    return render_template("multi.html", folder=folder, images=images)

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.errorhandler(Exception)
def error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template("error.html", errno="HTTP Error: "+str(code))

if __name__ == "__main__":
    app.run(debug=True)
