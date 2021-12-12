from flask import Blueprint, json, render_template,request,session,jsonify,redirect
from flask.helpers import url_for
import requests	
from werkzeug.security import generate_password_hash, check_password_hash


main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():

    return render_template("home.html")


@main.route('/profile',methods=['GET', 'POST'])
def profile():
    user_data=None
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None: #provera da li uopse nesto postoji u session id
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body = json.dumps({"session_id":_session_id})
        response=requests.post("http://127.0.0.1:5000/api/getProfileInfo",data=body,headers=headers)
        print(response.text)
        if response.text:
            user_data=json.loads(response.text)
    return render_template("profile.html",data=user_data) #prihvatat cemo session id u post methodi da ne dodje do prikazivanja i zloupotrebe


@main.route('/logIn',methods=['POST'])
def logIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _email and _password: #Proveri da li su prazni
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} #-----------------
        body=json.dumps({"email":_email,"password":_password})                 # Zahtev za api
        res=requests.post("http://127.0.0.1:5000/api/logInUser", data=body,headers=headers) #-----
        _json_res=res.json() # Pretvorimo podatke u json
        _user_id = _json_res['user_id']
        _session_id=_json_res['session_id']
        if _user_id != '-1' and _session_id != '-1': # Provera da li je vracen dobar user 
            session['session']=_session_id # Ako je ok sve ubacujemo session
        else:
            session['session']= None # U suprotnom postavljamo na null
            return json.dumps({'html':'<span>Invalid!!</span>'}) # Ispraviti da se pojavi na stranici da je nevalidno
        #if redirect.endpoint != 'bank.dashboard':  # baca 302 error koji je problem redirect na browser
        #resenje je https://stackoverflow.com/questions/15175965/why-i-get-302-error-on-flask-redirect
        return redirect(url_for('bank.dashboard')) # vracamo neku stranicu na koju se ide posle login
    else:
        session['session']= None # Ispisati da se polja popune
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
