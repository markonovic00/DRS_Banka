from flask import Blueprint, json, render_template,request,session,jsonify
from flask.helpers import url_for
import requests	
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

bank = Blueprint('bank', __name__, template_folder="templates")

@bank.route('/bank')
def dashboard():

    _balance={'':''}
    _card={'':''}
    _verified={'':''}
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
        body=json.dumps({"session_id":_session_id})                 # Zahtev za api
        res=requests.post("http://host.docker.internal:5000/api/dashboardData", data=body,headers=headers) #-----
        _json_res = res.json()  
        if _json_res:
            _balance=_json_res['balance']
            _card = _json_res['card']
            _verified=_json_res['verified']

    return render_template("bank_dashboard.html",balance=_balance,card=_card,verified=_verified)

@bank.route('/card')
def card():
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
        body=json.dumps({"session_id":_session_id})                 # Zahtev za api
        res=requests.post("http://host.docker.internal:5000/api/getCurrenciesAddFunds", data=body,headers=headers) #-----
        _json_res = res.json()
        _currenc = _json_res['curr']
    return render_template("card.html",  curr=json.loads(_currenc))

@bank.route('/transactions')
def transactions():
    _session_id=session.get('session')
    _data=[0]
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
        body=json.dumps({"session_id":_session_id})                 # Zahtev za api
        res=requests.post("http://host.docker.internal:5000/api/getAllTransactions", data=body,headers=headers) #-----
        _data=json.loads(res.text)
    return render_template("transactions.html", data=_data)

@bank.route('/transfer')
def transfer():
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
        body=json.dumps({"session_id":_session_id})                 # Zahtev za api
        res=requests.post("http://host.docker.internal:5000/api/getOwnCurrencies", data=body,headers=headers) #-----
        _json_res = res.json()
        _currenc = _json_res['curr']
    return render_template("transfer_money.html", curr=json.loads(_currenc))

@bank.route('/exhange')
def exchange():
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
        body=json.dumps({"session_id":_session_id})                 # Zahtev za api
        res=requests.post("http://host.docker.internal:5000/api/getCurrencies", data=body,headers=headers) #-----
        _json_res = res.json()
        _from = _json_res['from']
        _to = _json_res['to']
    return render_template("exchange.html", _from=json.loads(_from),_to=json.loads(_to))

@bank.route('/transferInitiate', methods=['POST'])
def transferInitiate():
    content_ret={'non':'non'}
    _currency = request.form['currency']
    _amount = request.form['amount']
    _transfer_to = request.form['trTo']
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
         if _currency and _amount:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
            body=json.dumps({"transfer":_transfer_to,"currency":_currency,"amount":_amount,"session_id":_session_id})                 # Zahtev za api
            res=requests.post("http://host.docker.internal:5000/api/transfer", data=body,headers=headers) #-----
            _json_res=res.json()
            content_ret=_json_res['status']

    return content_ret

@bank.route('/exchangeInitiate',methods=['POST'])
def exhangeInitiate():
    content_ret={'non':'non'}
    _currency_from = request.form['currencyFrom']
    _amount = request.form['amount']
    _currency_to = request.form['currencyTo']
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
         if _currency_from and _amount and _currency_to:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
            body=json.dumps({"currencyfrom":_currency_from,"currencyto":_currency_to,"amount":_amount,"session_id":_session_id})                 # Zahtev za api
            res=requests.post("http://host.docker.internal:5000/api/exchange", data=body,headers=headers) #-----
            _json_res=res.json()
            content_ret=_json_res['status']

    return content_ret


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
            res=requests.post("http://host.docker.internal:5000/api/verifyOACC", data=body,headers=headers) #-----
            _json_res=res.json()
            verified=_json_res['card']
            

    return json.dumps(verified)

@bank.route('/addFunds',methods=['POST'])
def addFunds():
    _currency = request.form['currency']
    _amount = request.form['amount']
    _session_id=session.get('session')
    verified='not verified'
    if _session_id and session.get('session')!='-1' and session.get('session')!=None:
         if _currency and _amount:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
            body=json.dumps({"currency":_currency,"amount":_amount,"session_id":_session_id})                 # Zahtev za api
            res=requests.post("http://host.docker.internal:5000/api/addFunds", data=body,headers=headers) #-----
            _json_res=res.json()
            verified=_json_res['card']
    
    return json.dumps(verified)


    #host.docker.internal pre bilo 127.0.0.1 !!!!!!!!!!