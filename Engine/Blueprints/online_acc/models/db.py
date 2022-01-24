import mysql.connector
import sys
from flask import jsonify
from mysql.connector.errors import Error

def connect():
    connection=None
    try:
        connection = mysql.connector.connect(
                    host="host.docker.internal",
                    user="root",
                    password="root",
                    database="drs_banka",
                    port="6033"
                    )
    except Error as err:
        print("Something went wrong connect: {}".format(err))

    return connection

def check_session(_session_id):
    user_id=-1 # Postavljamo na -1 jer ako ne nadjemo trazeni session znaci da nije ulogovan
    try:       # Ili ako dodje do greske vracamo -1
        sessiondb = connect()
        sessioncursor = sessiondb.cursor()
        sql="SELECT * FROM user_sessions WHERE session_id=%s"
        parameters=(_session_id,)
        sessioncursor.execute(sql,parameters)
        myresult = sessioncursor.fetchall()
        sessioncursor.close()
        sessiondb.close()
        if myresult:
            user_id=myresult[0][1]
    except Error as err:
        print("Something went wrong check_session: {}".format(err))

    return user_id

def insert_card(_credit_card):
    successfully=False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql="INSERT INTO credit_card (card_number,user_name,pin_code,expiration_date,user_id) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE user_id= %s"
        parametes=(_credit_card.card_number,_credit_card.user_name,int(_credit_card.pin_code),_credit_card.expiration_date,_credit_card.user_id,_credit_card.user_id)
        mycursor.execute(sql,parametes)
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_card: {}".format(err))

    return successfully

def insert_online_ACC(_online_acc):
    id=-1
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql="INSERT INTO online_account (user_id) VALUES (%s)"
        parametes=(_online_acc.user_id,)
        mycursor.execute(sql,parametes)
        mydb.commit()
        if mycursor.rowcount>0:
            id=mycursor.lastrowid # vraca id poslednjeg dodatog
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_online_ACC: {}".format(err))

    return id

def insert_online_balance(_online_balance):
    successfully=False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql="INSERT INTO online_account_balance (online_account_id,account_balance,currency) VALUES (%s,%s,%s)"
        parametes=(_online_balance.online_ACC_id,_online_balance.account_balance,_online_balance.currency)
        mycursor.execute(sql,parametes)
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_card: {}".format(err))

    return successfully

def get_online_acc_id(_user_id):
    myresult=[] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT * FROM online_account WHERE user_id=%s"
        parameters=(_user_id,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_online_acc_id: {}".format(err))

    return myresult

def get_funds_by_currency(_online_acc_id, _currency):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT * FROM online_account_balance WHERE online_account_id=%s AND currency=%s"
        parameters=(_online_acc_id,_currency)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_funds_by_currency: {}".format(err))

    return myresult

def get_funds(_online_acc_id):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT * FROM online_account_balance WHERE online_account_id=%s"
        parameters=(_online_acc_id,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_funds: {}".format(err))

    return myresult

def get_card_by_id(_user_id):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT * FROM credit_card WHERE user_id=%s"
        parameters=(_user_id,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_card_by_id: {}".format(err))

    return myresult

def insert_or_update_funds(_online_balance):
    successfully=False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql ="UPDATE online_account_balance SET account_balance=%s WHERE online_account_id=%s AND currency=%s"
        parametes=(_online_balance.account_balance,_online_balance.online_ACC_id,_online_balance.currency)
        mycursor.execute(sql,parametes) # pokusaj update
        if mycursor.rowcount==0: #ako nije uspesan update dodaj novu valutu
            sql="INSERT INTO online_account_balance (online_account_id,account_balance,currency) VALUES (%s,%s,%s)"
            parametes=(_online_balance.online_ACC_id,_online_balance.account_balance,_online_balance.currency)
            mycursor.execute(sql,parametes)
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_funds: {}".format(err))

    return successfully

def insert_funds(_online_balance):
    successfully=False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql="INSERT INTO online_account_balance (online_account_id,account_balance,currency) VALUES (%s,%s,%s)"
        parametes=(_online_balance.online_ACC_id,_online_balance.account_balance,_online_balance.currency)
        mycursor.execute(sql,parametes)
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_card: {}".format(err))

    return successfully

def get_currencies(_online_acc_id):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT currency FROM online_account_balance WHERE online_account_id=%s "
        parameters=(_online_acc_id,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_funds_by_currency: {}".format(err))

    return myresult

def update_funds(_online_balance):
    successfully=False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql ="UPDATE online_account_balance SET account_balance=%s WHERE online_account_id=%s AND currency=%s"
        parametes=(_online_balance.account_balance,_online_balance.online_ACC_id,_online_balance.currency)
        mycursor.execute(sql,parametes) # pokusaj update
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_funds: {}".format(err))

    return successfully

