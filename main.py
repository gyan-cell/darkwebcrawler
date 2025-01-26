from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5511)
