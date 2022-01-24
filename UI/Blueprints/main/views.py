from flask import Blueprint, json, render_template,request,session,jsonify,redirect
from flask.helpers import url_for
import requests	
from werkzeug.security import generate_password_hash, check_password_hash
from ..classes.user import User


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
        response=requests.post("http://host.docker.internal:5000/api/getProfileInfo",data=body,headers=headers)
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
        res=requests.post("http://host.docker.internal:5000/api/logInUser", data=body,headers=headers) #-----
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


@main.route('/register')
def register():

    return render_template("register.html",span="")

@main.route('/registerCall',methods=['POST'])
def registerCall():
    _first_name = request.form['firstName']
    _last_name=request.form['lastName']
    _address = request.form['address']
    _city = request.form['city']
    _country = request.form['country']
    _phone_num = request.form['phoneNum']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _email and _password and _first_name and _last_name and _address and _city and _country:
        new_user= User(-1,_first_name,_last_name,_address,_city,_country,_phone_num,_email,_password)

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body = json.dumps(new_user.__dict__)
        res=requests.post("http://host.docker.internal:5000/api/registerUser", data=body,headers=headers)
        print(json.loads(res.text))
        _json_res=res.json() # Pretvorimo podatke u json
        _successfully = _json_res['registered']
        if _successfully=="successfully":
            return redirect(url_for('main.index'))
        else:
            return render_template("register.html", span=_successfully)
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@main.route('/logOut')
def logOut():
    _session_id=session.get('session')
    if _session_id and session.get('session')!='-1' and session.get('session')!=None: #provera da li uopse nesto postoji u session id
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body = json.dumps({"session_id":_session_id})
        response=requests.post("http://host.docker.internal:5000/api/logOut",data=body,headers=headers)
        _json_res=response.json() # Pretvorimo podatke u json
        _successfully = _json_res['none']
        if _successfully=="logedOut":
            session['session']=None
            return redirect(url_for('main.index'))

    return redirect(url_for('main.index'))


@main.route('/updateUser',methods=['POST'])
def updateUser():
    _first_name = request.form['firstName']
    _last_name=request.form['lastName']
    _address = request.form['address']
    _city = request.form['city']
    _country = request.form['country']
    _phone_num = request.form['phoneNum']
    _email = request.form['inputEmail']

    if _email and _first_name and _last_name and _address and _city and _country:
        new_user= User(-1,_first_name,_last_name,_address,_city,_country,_phone_num,_email,"")

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body = json.dumps(new_user.__dict__)
        res=requests.post("http://host.docker.internal:5000/api/updateUser", data=body,headers=headers)
        print(json.loads(res.text))
        _json_res=res.json() # Pretvorimo podatke u json
        _successfully = _json_res['updated']
        if _successfully=="successfully":
            return redirect(url_for('bank.dashboard'))
        else:
            return render_template("profile.html", span=_successfully)
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})