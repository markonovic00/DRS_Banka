from flask import Blueprint, render_template,jsonify,session,json
import flask
from .models.db import connect,check_session,update_funds,get_online_acc_id,get_funds_by_currency,insert_transaction,get_all_transactions,get_acc_by_email,insert_funds
from ..classes.user import User
from ..classes.credit_card import Credit_Card,Online_ACC,Online_ACC_Balance

exchange = Blueprint('exchange', __name__, template_folder="templates")

@exchange.route('/exchange', methods=['POST'])
def transfer():
    content_ret={'status':'canceled'}

    try:
        content=flask.request.json
    except ValueError as err:
        print("Something went wrong addFunds: {}".format(err))

    exchange_rate=1 # trenutno jedan posle sa api cemo resiti
    _session_id=content['session_id']
    _currency_from = content['currencyfrom']
    _currency_to=content['currencyto']
    _ammount=content['amount']
    succ=False
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1:
        online_acc=get_online_acc_id(user_id)
        online_acc_id=online_acc[0][0]
        online_acc_balane=get_funds_by_currency(online_acc_id,_currency_from) 
        from_balance=Online_ACC_Balance(online_acc_balane[0][0],online_acc_balane[0][1],online_acc_balane[0][2])
        if(int(from_balance.account_balance)>=int(_ammount)): # znaci da je moguce izvrsiti promenu, jer postoji dovoljno sredstava
            balance_am=int(from_balance.account_balance)- int(_ammount) # skinemo kolicinu zamenjenih para
            from_balance.account_balance=str(balance_am) # zabelezimo novu situaciju
            succ= update_funds(from_balance) # upisemo stanje u bazu
            # zatim treba dodati novo stanje sa novom valutom ili azurirati postojecu
            online_acc_balane=get_funds_by_currency(online_acc_id,_currency_to) 
            if len(online_acc_balane)==0:
                #insert fund
                new_ammount = int(_ammount)*exchange_rate # uradimo zamenu valute po nekom kursu
                new_balance=Online_ACC_Balance(online_acc_id,str(new_ammount),_currency_to)
                succ=insert_funds(new_balance)
            else:
                #update fund
                new_balance=Online_ACC_Balance(online_acc_balane[0][0],online_acc_balane[0][1],online_acc_balane[0][2])
                balance_am=int(new_balance.account_balance)+(int(_ammount) * exchange_rate) # zamena valute po kursu
                new_balance.account_balance=str(balance_am)
                succ= update_funds(new_balance)
            if succ:
                content_ret={'status':'exhanged'}
            else:
                content_ret={'status':'failed'}
        else:
            content_ret={'status':'not enough funds'}

    return content_ret