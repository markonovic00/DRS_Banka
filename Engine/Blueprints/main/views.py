from flask import Blueprint, render_template,jsonify
import flask
from mysql.connector import connection
from requests.api import request
from .models.db import connect

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():
    return render_template("home.html")

@main.route("/getUsers")
def getUsers():
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()
    return  jsonify(myresult)
    

@main.route("/logInUser", methods=['GET', 'POST'])
def logIn():

    content= flask.request.json
    _email = content['email']
    _password= content['password']
    print(content)
    mydb=connect()
    mycursor = mydb.cursor()
    sql="SELECT * FROM users WHERE email = %s AND password = %s"
    parameters=(_email,_password)
    mycursor.execute(sql,parameters)
    myresult = mycursor.fetchall()
    mycursor.close()
    mydb.close()

    data={"user_id":"-1",
        "session_id":"-1"}
    if myresult:
        data={"user_id":myresult[0][0],
        "session_id":"0000"}

    return data

    #https://auth0.com/blog/developing-restful-apis-with-python-and-flask/ 
    #Api funkcionalnost
    #https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
    # user id kako identifikovati od koga stize zahtev
    