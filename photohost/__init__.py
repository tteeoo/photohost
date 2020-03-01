import os
from hashlib import sha256
from flask import Flask, render_template, url_for, request, flash, redirect, abort, send_from_directory
from werkzeug.exceptions import HTTPException

app = Flask(__name__, static_folder="static")
app.config["UPLOAD_FOLDER"] = "/media/drive/uploads"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024
app.secret_key = os.urandom(16)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in \
            ["png", "jpg", "jpeg", "gif", "ico", "tif", "svg"]

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
            tmpname = os.path.join(app.config["UPLOAD_FOLDER"]+"/tmp", file.filename)
            extension = "." + file.filename.split(".")[1]
            file.save(tmpname)
            with open(tmpname, "rb") as f:
                filename = sha256(f.read()).hexdigest() + extension
            os.rename(tmpname, os.path.join(app.config["UPLOAD_FOLDER"], filename))
            url = "https://photohost.tech/view/" + filename
                
            return redirect(url)
        else:
            return render_template("error.html", errno="An unkown error occurred.")
    return render_template("index.html")

@app.route("/image/<filename>")
def return_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)

@app.route("/view/<image>")
def view(image):
    return render_template("view.html", image=image)

@app.errorhandler(Exception)
def error(e):                                    
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template("error.html", errno="HTTP Error: "+str(code))

if __name__ == "__main__":
    app.run(debug=True)
