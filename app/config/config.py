import os
from app import app
from flask_cors import CORS

CORS(app)

app.debug = True
UPLOAD_FOLDER = './images/'
BASE_APP_URL = "https://flask-api6389.herokuapp.com/api/image?file="
SITE_ID = '62cecd2cf858d8026c165bfe'
PUBLISH_DOMAIN = ['https://swipefiled.webflow.io']
# <meta http-equiv="refresh" content="90" > auto refresh front end


# ENV = 'PROD'
ENV = 'DEV'

if ENV == 'PROD':
    app.debug = False
    BASE_APP_URL = "https://flask-api6389.herokuapp.com/api/image?file="


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BASE_APP_URL'] = BASE_APP_URL
app.config['SITE_ID'] = SITE_ID
app.config['PUBLISH_DOMAIN'] = PUBLISH_DOMAIN