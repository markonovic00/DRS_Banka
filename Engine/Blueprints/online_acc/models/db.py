import mysql.connector
import sys
from flask import jsonify
from mysql.connector.errors import Error

def connect():
    connection=None
    try:
        connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="drs_banka"
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