import os
from flask import Flask

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/app')

app = Flask(__name__, template_folder=ASSETS_DIR, static_folder=ASSETS_DIR)