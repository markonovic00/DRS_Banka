from flask import Blueprint, json, render_template,request
import requests

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():
    users=None
    users = requests.get("http://127.0.0.1:5000/api/getUsers")
    if users!=None:
        uList=json.loads(users.text)
    else:
        uList=['No users found.']
    return render_template("home.html",users=uList)


@main.route('/logIn',methods=['POST'])
def logIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _email and _password:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body=json.dumps({"email":_email,"password":_password})
        res=requests.post("http://127.0.0.1:5000/api/logInUser", data=body,headers=headers)
        print(res.text)
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})