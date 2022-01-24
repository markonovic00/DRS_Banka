from flask import Blueprint, render_template,jsonify,session,json
import flask
import requests
from .models.db import connect,check_session,insert_card,insert_online_ACC,insert_online_balance,get_online_acc_id,get_funds_by_currency,insert_funds,update_funds,get_funds,get_card_by_id,get_currencies
from ..classes.user import User
from ..classes.credit_card import Credit_Card,Online_ACC,Online_ACC_Balance

online_acc = Blueprint('online_acc', __name__, template_folder="templates")

@online_acc.route('/dashboardData', methods=['POST'])
def dashboard():
    content_ret={'card':{'':''}, 'verified':'no','balance':{'':''}}
    content={'none':'none'}
    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong dashboardData: {}".format(err))
    
    _session_id=content['session_id']
    user_id=check_session(_session_id)
    if user_id!=-1:
        online_acc=get_online_acc_id(user_id)
        if len(online_acc)!=0:
            content_ret={'card':{'':''}, 'verified':'yes','balance':{'':''}}
            online_acc_id=online_acc[0][0]
            online_acc_balane=get_funds(online_acc_id)
            nested={}
            for item in online_acc_balane:
                nested[item[2]]=item[1]
            content_ret['balance']=nested
            card=get_card_by_id(user_id)
            content_ret['card']={'card_number':card[0][0],'user_name':card[0][1],'exp_date':card[0][3]}

    return content_ret

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
        new_ACC_balance = Online_ACC_Balance(new_online_ACC_ID,0,"USD")
        succ_balance=insert_online_balance(new_ACC_balance)

    if succ_balance and succ_card:
        content_ret={'card':'verified'}

    return content_ret
    #uraditi dodavanje kartice

@online_acc.route('/addFunds', methods=['POST'])
def addFunds():
    content_ret={'card':'funds not added'}
    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong addFunds: {}".format(err))

    _session_id=content['session_id']
    _currency=content['currency']
    _ammount=content['amount']
    succ=False
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1:
        online_acc=get_online_acc_id(user_id)
        online_acc_id=online_acc[0][0]
        online_acc_balane=get_funds_by_currency(online_acc_id,_currency) # nalazi se accaount sa zeljenom
        if len(online_acc_balane)==0:
            #insert fund
            new_balance=Online_ACC_Balance(online_acc_id,_ammount,_currency)
            succ=insert_funds(new_balance)
        else:
            #update fund
            new_balance=Online_ACC_Balance(online_acc_balane[0][0],online_acc_balane[0][1],online_acc_balane[0][2])
            balance_am=float(new_balance.account_balance)+float(_ammount)
            new_balance.account_balance=str(balance_am)
            succ= update_funds(new_balance)
        if succ:
            content_ret={'card':'funds added'}
        

    return content_ret

@online_acc.route('/getCurrenciesAddFunds', methods=['POST'])
def getCurrenciesAddFunds():
    content_ret={'curr':'none'}
    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong getCurrencies: {}".format(err))

    _session_id=content['session_id']
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1:
        _base_currency='USD'
        res=requests.get('https://freecurrencyapi.net/api/v2/latest?apikey=c8823dc0-76bf-11ec-8f59-dd6de8678be4&base_currency='+_base_currency)
        if(res.text):
            print("Api Call Successful")
            res=json.loads(res.text)
            content_ret={
                'curr':json.dumps(list(res['data'].keys()))
            }
            #content_ret['from']=online_currencies
            #print(res['data'].keys())
            return content_ret
        else:
            print("Error")
        
    return content_ret

    