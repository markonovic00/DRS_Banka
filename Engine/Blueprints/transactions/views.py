from flask import Blueprint, render_template,jsonify,session,json
import flask
from .models.db import connect,check_session,update_funds,get_online_acc_id,get_funds_by_currency,insert_transaction,get_all_transactions,get_acc_by_email,insert_funds
from ..classes.user import User
from ..classes.credit_card import Credit_Card,Online_ACC,Online_ACC_Balance

transactions = Blueprint('transactions', __name__, template_folder="templates")

@transactions.route('/transfer', methods=['POST'])
def transfer():
    content_ret={'status':'canceled'}

    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong addFunds: {}".format(err))

    _session_id=content['session_id']
    _transfer_to = content['transfer']
    _currency=content['currency']
    _ammount=content['amount']
    succ=False
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1:
        online_acc=get_online_acc_id(user_id)
        online_acc_id=online_acc[0][0]
        online_acc_balane=get_funds_by_currency(online_acc_id,_currency) 
        new_balance=Online_ACC_Balance(online_acc_balane[0][0],online_acc_balane[0][1],online_acc_balane[0][2])
        balance_am=int(new_balance.account_balance)-int(_ammount)
        if(balance_am>=0):
            new_balance.account_balance=str(balance_am)
            succ= update_funds(new_balance)
        else:
            content_ret={'status':'not enough funds'}
        if succ:
            insert_transaction(user_id,_transfer_to,_ammount,_currency)
            content_ret={'status':'accepted, waiting 2min'}

        if '@' in _transfer_to:
            send_to_id= get_acc_by_email(_transfer_to.strip())
            rec_online_acc =get_online_acc_id(send_to_id[0][0])
            rec_online_acc_id=rec_online_acc[0][0]
            rec_online_acc_balane=get_funds_by_currency(rec_online_acc_id,_currency) # nalazi se accaount sa zeljenom
        if len(rec_online_acc_balane)==0:
            #insert fund
            new_balance=Online_ACC_Balance(rec_online_acc_id,_ammount,_currency)
            succ=insert_funds(new_balance)
        else:
            #update fund
            new_balance=Online_ACC_Balance(rec_online_acc_balane[0][0],rec_online_acc_balane[0][1],rec_online_acc_balane[0][2])
            balance_am=int(new_balance.account_balance)+int(_ammount)
            new_balance.account_balance=str(balance_am)
            succ= update_funds(new_balance)
        
        if succ:
            insert_transaction(user_id,_transfer_to,_ammount,_currency)
            content_ret={'status':'accepted, waiting 2min'}

    return content_ret

@transactions.route('/getAllTransactions',methods=['POST'])
def getAllTransactions():
    content={'none':'none'}
    content_ret=[0]
    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong addFunds: {}".format(err))

    _session_id=content['session_id']
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1:
        content_ret=get_all_transactions(user_id)

    return jsonify(content_ret)