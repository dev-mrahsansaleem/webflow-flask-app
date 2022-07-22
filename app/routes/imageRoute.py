import os
from pprint import pprint
from app import app
from datetime import datetime
import json
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
import re
from PIL import Image
from io import BytesIO
from os import mkdir
from os.path import isdir, join, exists

@app.route("/")
def test():
    return jsonify(app.config['UPLOAD_FOLDER'])



@app.route("/api/Image", methods=['POST'])
def sendImage():
    if not isdir(app.config['UPLOAD_FOLDER']):
        mkdir(app.config['UPLOAD_FOLDER'])

    url = request.args.get('url')

    get_resp = requests.get(url = url)
    # data = re.sub('\s+',"",data) # remove all spaces
    arrData = re.split('<\/?script>',get_resp.text) # split by script open close tags
    data = [x for x in arrData if "props" in x]
    data = '{'+data[0][data[0].find('"require"'):data[0].rfind(',"contexts')]+'}'
    data = re.sub('\\"',"\"",data) # replace \qoutes with qoutes
    dataJson = json.loads(data)
    props = dataJson['require'][10][3][0]['props']
    
    data = {
        "fields": {
            "name": props['deeplinkAdID'], #need to change to find ad title always
            "ad-id": props['deeplinkAdID'],
            "ad-title": props['deeplinkAdCard']['snapshot']["cards"][0]["title"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
            "ad-body": props['deeplinkAdCard']['snapshot']["cards"][0]["body"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
            "ad-caption": props['deeplinkAdCard']['snapshot']["cards"][0]["caption"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
            "ad-resized-image": "",
            "ad-original-image": "",
            "ad-page-creation-time": datetime.fromtimestamp(props['deeplinkAdCard']['snapshot']["creation_time"]).strftime("%d-%b-%Y"), # (%H:%M:%S.%f)
            "ad-page-like-count": str(props['deeplinkAdCard']['snapshot']["page_like_count"]),
            "ad-type": props['adType'],
            "is-active": str(props['deeplinkAdCard']['isActive']),
            "link-url": props['deeplinkAdCard']['snapshot']["link_url"],
            "page-id": str(props['deeplinkAdCard']['pageID']),
            "page-name": props['deeplinkAdCard']['pageName'],
            "page-profile-picture": "",
            "page-categories": " ".join([item for item in props['deeplinkAdCard']['snapshot']['page_categories'].values()]),
            "page-url": props['deeplinkAdCard']['snapshot']["page_profile_uri"],
            "media-type": props['mediaType'],
            "publisher-platform": " ".join([item for item in props['deeplinkAdCard']['publisherPlatform']]),
            "_archived": False,
            "_draft": False,
            },
        }
    # profile picture store
    imagObj = Image.open(BytesIO(requests.get(props['deeplinkAdCard']['snapshot']['page_profile_picture_url']).content))
    data['fields']['page-profile-picture']  = app.config['BASE_APP_URL'] + 'profile_' + props['deeplinkAdID'] + "."+ imagObj.format.lower()
    imagObj.save(app.config['UPLOAD_FOLDER'] + data['fields']['page-profile-picture'])

    if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0:
        # resized image
        imagObj = Image.open(BytesIO(requests.get(props['deeplinkAdCard']['snapshot']["cards"][0]["resized_image_url"]).content))
        data['fields']['ad-resized-image']  = app.config['BASE_APP_URL'] + 'resized_' + props['deeplinkAdID'] + "."+ imagObj.format.lower()
        imagObj.save(app.config['UPLOAD_FOLDER'] + data['fields']['ad-resized-image'])
            
        # orignal image
        imagObj = Image.open(BytesIO(requests.get(props['deeplinkAdCard']['snapshot']["cards"][0]["original_image_url"]).content))
        data['fields']['ad-original-image']  = app.config['BASE_APP_URL'] + 'orignal_' + props['deeplinkAdID'] + "."+ imagObj.format.lower()
        imagObj.save(app.config['UPLOAD_FOLDER'] + data['fields']['ad-original-image'] )

    # return jsonify(data)

    # pprint(params)
    headers = {
    'content-type': 'application/json',
    "Authorization":"Bearer f789b409bf0afe37e052522a4df7cdc1f99fe908d20ac4043df7e831d629a97e"
    }
    dump = json.dumps(data)
    post_resp = requests.post(url = "https://api.webflow.com/collections/62daf04048a18d41dc374c6f/items?live=true",data=dump,headers=headers)
    pprint(post_resp)
    return jsonify({
        "code":post_resp.status_code,
        "msg":'created',
        "data":post_resp.text
        })



@app.route("/api/Image", methods=['GET'])
def getImage():
    fileName = request.args.get('file') # "profile_796673148185972.JPEG" 
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], fileName))
    pass
