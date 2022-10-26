import pandas as pd
import data
from flask import Flask, jsonify

app = Flask("wdb_api")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/tracks")
def get_tracks():
    result = data.get_tracks()
    return jsonify(result)


app.run(debug=True)
