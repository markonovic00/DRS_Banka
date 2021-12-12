import mysql.connector
import sys
from flask import jsonify
from mysql.connector.errors import Error
from werkzeug.exceptions import PreconditionFailed

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


def check_user_login(_email,_password):
    user_id=-1
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT * FROM users WHERE email = %s AND password = %s"
        parameters=(_email,_password)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        if myresult:
            user_id=myresult[0][0]
    except Error as err:
        print("Something went wrong check_user_login: {}".format(err))
    return user_id

def get_user_by_id(_user_id):
    myresult=[-1] 
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="SELECT * FROM users WHERE id=%s"
        parameters=(_user_id,)
        mycursor.execute(sql,parameters)
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong get_user_by_id: {}".format(err))

    return myresult

def insert_session_id(_user_id,_session_id):
    successfully=False
    try:
        mydb=connect()
        mycursor = mydb.cursor()
        sql="INSERT INTO user_sessions (session_id , user_id) VALUES (%s , %s) ON DUPLICATE KEY UPDATE session_id= %s"
        parameters=(_session_id,_user_id,_session_id)
        mycursor.execute(sql,parameters)
        mydb.commit()
        if mycursor.rowcount>0:
            successfully=True
        mycursor.close()
        mydb.close()
    except Error as err:
        print("Something went wrong insert_session_id: {}".format(err))

    return successfully