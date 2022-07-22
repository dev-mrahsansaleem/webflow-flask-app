from fileinput import filename
import os
from datetime import datetime
import json
from pprint import pprint
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import re
from PIL import Image
from io import BytesIO


    
# get_resp = requests.get(url = 'https://www.facebook.com/ads/library/?id=575190780933772')

page_profile_picture = Image.open(BytesIO(requests.get("https://storage.googleapis.com/adison-foreplay.appspot.com/575190780933772/e3ae714f179a76b0f5529d90cf03ea2f.jpg").content))
fileName = './images/' + "11111111." + page_profile_picture.format
page_profile_picture.save(fileName)
# data = {
#     "fields": {
#         "_archived": False,
#         "_draft": False,
#         "name": props['deeplinkAdID'], #need to change to find ad title always
#         "ad_id": props['deeplinkAdID'],
#         "ad_title": props['deeplinkAdCard']['snapshot']["cards"][0]["title"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
#         "ad_body": props['deeplinkAdCard']['snapshot']["cards"][0]["body"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
#         "ad_caption": props['deeplinkAdCard']['snapshot']["cards"][0]["caption"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
#         "ad_image_url": props['deeplinkAdCard']['snapshot']["cards"][0]["resized_image_url"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
#         "ad_image": props['deeplinkAdCard']['snapshot']["cards"][0]["original_image_url"] if len(props['deeplinkAdCard']['snapshot']["cards"]) > 0 else "",
#         "ad_page_creation_time": datetime.fromtimestamp(props['deeplinkAdCard']['snapshot']["creation_time"]),
#         "ad_page_like_count": props['deeplinkAdCard']['snapshot']["page_like_count"],
#         "ad_type": props['adType'],
#         "is_active": props['deeplinkAdCard']['isActive'],
#         "link_url": props['deeplinkAdCard']['snapshot']["link_url"],
#         "page_id": props['deeplinkAdCard']['pageID'],
#         "page_name": props['deeplinkAdCard']['pageName'],
#         "page_profile_picture_url": r"https://flask-api6389.herokuapp.com/"+ fileName[1:],
#         "page_categories": " ".join([item for item in props['deeplinkAdCard']['snapshot']['page_categories'].values()]),
#         "page_profile_uri": props['deeplinkAdCard']['snapshot']["page_profile_uri"],
#         "media_type": props['mediaType'],
#         "publisher_platform": " ".join([item for item in props['deeplinkAdCard']['publisherPlatform']]),
#         },
#     }

    
pprint(filename)
# headers = {
# 'content-type': 'application/json',
# "Authorization":"Bearer f789b409bf0afe37e052522a4df7cdc1f99fe908d20ac4043df7e831d629a97e"
# }

# post_resp = requests.post(url = "collenction/link",data=json.dumps(data),headers=headers)
