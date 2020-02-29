from flask import Flask, render_template, url_for, request
app = Flask(__name__, static_folder='static', static_url_path='')

@app.route("/")
def index():
    return render_template("index.html")
