from flask import Blueprint, render_template,jsonify,session,json
import flask
from .models.db import connect,check_session,insert_card,insert_online_ACC,insert_online_balance
from ..classes.user import User
from ..classes.credit_card import Credit_Card,Online_ACC,Online_ACC_Balance

online_acc = Blueprint('online_acc', __name__, template_folder="templates")

@online_acc.route('/verifyOACC', methods=["POST"])
def verifyCard():
    content_ret={'card':'not verified'}
    succ_card=False
    succ_balance=False
    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong verifyCard: {}".format(err))

    _session_id=content['session_id']
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1: 
        new_credit_card= Credit_Card(content['card_number'],content['user_name'],content['pin_code'],
                        content['expiration_date'],user_id)
        succ_card=insert_card(new_credit_card)
    
    new_online_ACC = Online_ACC(user_id)
    new_online_ACC_ID=-1
    if succ_card:
        new_online_ACC_ID=insert_online_ACC(new_online_ACC)
    #kada se vrati id accounta koji je ubacen tada se u online acc ubaci njegov ID
    if new_online_ACC_ID!=-1 and succ_card:
        new_ACC_balance = Online_ACC_Balance(new_online_ACC_ID,0,"$")
        succ_balance=insert_online_balance(new_ACC_balance)

    if succ_balance and succ_card:
        content_ret={'card':'verified'}
    
    return content_ret
    #uraditi dodavanje kartice