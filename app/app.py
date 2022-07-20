from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/")
def test():
    return jsonify("working")

@app.route("/")
def storeData():
    url = request.args.get('url')
    r = requests.get(url = url)
    
    # extracting data in json format
    data = r.json()
    return jsonify(data)