from flask import Flask

app = Flask(__name__)

# config
from app.config import config

# routes
from app.routes import route