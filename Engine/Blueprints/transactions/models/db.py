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

def get_acc_by_email(_email):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT ID FROM users WHERE email=%s"
        parameters=(_email,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_acc_by_email: {}".format(err))

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

def insert_transaction(_from,_to,_amount,_currency,_date_time):
    successfully=False
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        sql="INSERT INTO transactions (oa_from_ID,oa_to_ID,amount,currency,date_time) VALUES (%s,%s,%s,%s,%s)"
        parametes=(_from,_to,_amount,_currency,_date_time)
        mycursor.execute(sql,parametes)
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_transaction: {}".format(err))

    return successfully

def get_all_transactions(_user_id):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT oa_to_ID, amount, currency, date_time FROM transactions WHERE oa_from_ID=%s"
        parameters=(_user_id,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_all_transactions: {}".format(err))

    return myresult