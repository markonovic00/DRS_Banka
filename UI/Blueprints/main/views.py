from flask import Blueprint, json, render_template,request,session,jsonify
from flask.helpers import url_for
import requests	
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():
    print(session.get('session'))
    users=None
    if session.get('session')!='-1' and session.get('session')!=None:
        users = requests.get("http://127.0.0.1:5000/api/getUsers")
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
        #print(res.json())
        _json_res=res.json()

        _user_id = _json_res['user_id']
        _session_id=_json_res['session_id']
        
        if _user_id != '-1' and _session_id != '-1': 
            session['session']=_session_id
        else:
            #session.pop('session', None)
            session['session']= None
            return json.dumps({'html':'<span>Invalid!!</span>'})
        #return json.dumps({'html':'<span>All fields good !!</span>'})
        return redirect(url_for('main.index'))
    else:
        session['session']= None
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@main.route('/register',methods=['POST'])
def register():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _email and _password:
        hashed_password = generate_password_hash(_password)
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
