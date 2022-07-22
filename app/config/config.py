import os
from app import app
from flask_cors import CORS

CORS(app)

app.debug = True
UPLOAD_FOLDER = os.getcwd() + '\\images\\'
BASE_APP_URL = "http://127.0.0.1:5000/api/Image?file="


# ENV = 'PROD'
ENV = 'DEV'

if ENV == 'PROD':
    app.debug = False
    UPLOAD_FOLDER = os.getcwd() + '\\images\\'
    BASE_APP_URL = "https://flask-api6389.herokuapp.com/api/Image?file="


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BASE_APP_URL'] = BASE_APP_URL