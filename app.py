import os
from datetime import datetime
import json
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
import re
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/")
def test():
    return jsonify("working")

@app.route("/store")
def storeData():
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
            "_archived": False,
            "_draft": False,
            "name": props['deeplinkAdID'], #need to change to find ad title always
            "ad_id": props['deeplinkAdID'],
            "ad_title": props['deeplinkAdCard']['snapshot']["cards"][0]["title"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
            "ad_body": props['deeplinkAdCard']['snapshot']["cards"][0]["body"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
            "ad_caption": props['deeplinkAdCard']['snapshot']["cards"][0]["caption"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
            "ad_resized_image": "",
            "ad_original_image": "",
            "ad_page_creation_time": datetime.fromtimestamp(props['deeplinkAdCard']['snapshot']["creation_time"]),
            "ad_page_like_count": props['deeplinkAdCard']['snapshot']["page_like_count"],
            "ad_type": props['adType'],
            "is_active": props['deeplinkAdCard']['isActive'],
            "link_url": props['deeplinkAdCard']['snapshot']["link_url"],
            "page_id": props['deeplinkAdCard']['pageID'],
            "page_name": props['deeplinkAdCard']['pageName'],
            "page_profile_picture": "",
            "page_categories": " ".join([item for item in props['deeplinkAdCard']['snapshot']['page_categories'].values()]),
            "page_profile_uri": props['deeplinkAdCard']['snapshot']["page_profile_uri"],
            "media_type": props['mediaType'],
            "publisher_platform": " ".join([item for item in props['deeplinkAdCard']['publisherPlatform']]),
            },
        }
    # profile picture store
    imagObj = Image.open(BytesIO(requests.get(props['deeplinkAdCard']['snapshot']['page_profile_picture_url']).content))
    data['fields']['page_profile_picture']  = './images/profile_' + props['deeplinkAdID'] + "."+ imagObj.format
    # imagObj.save(data['fields']['page_profile_picture'])

    if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0:
        # resized image
        imagObj = Image.open(BytesIO(requests.get(props['deeplinkAdCard']['snapshot']["cards"][0]["resized_image_url"]).content))
        data['fields']['ad_resized_image']  = './images/resized_' + props['deeplinkAdID'] + "."+ imagObj.format
        # imagObj.save(data['fields']['ad_resized_image'])
            
        # orignal image
        imagObj = Image.open(BytesIO(requests.get(props['deeplinkAdCard']['snapshot']["cards"][0]["original_image_url"]).content))
        data['fields']['ad_original_image']  = './images/orignal_' + props['deeplinkAdID'] + "."+ imagObj.format
        # imagObj.save(data['fields']['ad_original_image'] )

    return jsonify(data)

    pprint(params)
    headers = {
    'content-type': 'application/json',
    "Authorization":"Bearer f789b409bf0afe37e052522a4df7cdc1f99fe908d20ac4043df7e831d629a97e"
    }

    post_resp = requests.post(url = "collenction/link",data=json.dumps(data),headers=headers)

    # return jsonify(post_resp)



@app.route("/get_image")
def getImage():
    fileName = request.args.get('file')
    return send_file("../images/"+fileName)
    pass