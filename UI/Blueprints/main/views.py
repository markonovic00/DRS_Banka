from flask import Blueprint, json, render_template
import requests

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():
    users = requests.get("http://127.0.0.1:5000/")
    uList=json.loads(users.text)
    return render_template("home.html",users=uList)