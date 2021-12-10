from flask import Blueprint, render_template,jsonify
from mysql.connector import connection
from .db import connect

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():
    mydb=connect()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    return  jsonify(myresult)
    #return render_template("home.html")


    #https://auth0.com/blog/developing-restful-apis-with-python-and-flask/