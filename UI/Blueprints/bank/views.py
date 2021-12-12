from flask import Blueprint, json, render_template,request,session,jsonify
from flask.helpers import url_for
import requests	
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

bank = Blueprint('bank', __name__, template_folder="templates")

@bank.route('/bank')
def dashboard():

    return render_template("bank_dashboart.html")