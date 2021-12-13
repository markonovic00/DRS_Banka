from flask import Blueprint, json, render_template,request,session,jsonify
from flask.helpers import url_for
import requests	
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

bank = Blueprint('bank', __name__, template_folder="templates")

@bank.route('/bank')
def dashboard():

    return render_template("bank_dashboard.html")

@bank.route('/verifyOACC', methods=['POST'])
def addCard():
    _card_number = request.form['cardNum']
    _user_name = request.form['userName']
    _pin_code = request.form['pinCode']
    _expiration_date = request.form['expDate']
    _session_id=session.get('session')
    verified='not verified'
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
        if _card_number and _user_name and _pin_code and _expiration_date:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
            body=json.dumps({"card_number":_card_number,"user_name":_user_name,"pin_code":_pin_code,
                            "expiration_date":_expiration_date,"session_id":_session_id})                 # Zahtev za api
            res=requests.post("http://127.0.0.1:5000/api/verifyOACC", data=body,headers=headers) #-----
            _json_res=res.json()
            verified=_json_res['card']
            

    return json.dumps({'html':'<span>'+verified+'</span>'})