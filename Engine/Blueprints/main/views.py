from flask import Blueprint, render_template,jsonify,session,json
import flask
from .models.db import connect,check_session,get_user_by_id,check_user_login, insert_session_id, insert_user,check_if_exists,delete_session, update_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..classes.user import User
from multiprocessing import Process, Queue

main = Blueprint('main', __name__, template_folder="templates")

@main.route("/")
def index():
    return render_template("home.html")
    
    
@main.route("/getProfileInfo", methods=['POST'])
def getProfile():
    user_data={"none":"none"}
    content=flask.request.json
    _session_id=content['session_id']
    user_id=check_session(_session_id)#vraca -1 ako ne moze da nadje korisnika, u suprotnom vraca id korisnika koji je ulogovan
    if user_id!=-1: 
        user_data=get_user_by_id(user_id) # vraca jsonify verziju, tako da return ide obican
    return jsonify(user_data)

@main.route("/logInUser", methods=['GET', 'POST'])
def logIn():
    content = {'none':'none'}
    try:
        content= flask.request.json
    except ValueError as err:
        print ("Content no json {}".format(err))
    _email = content['email']
    _password= content['password'] # Prime se parametri sa posta

    _user_id=check_user_login(_email,_password) # Proveravamo u bazi za logovanje
    
    data={"user_id":"-1",
        "session_id":"-1"} #inicijalni podatak koji se vraca u slucaju greske pri logovanju

    if _user_id != -1:
        _session_id=generate_password_hash(_email+_password) # kreiramo neki unikatni session id
        insert_session_id(_user_id,_session_id)
        data={
                "user_id":_user_id,
                "session_id":_session_id
            }

    return data


def register_user_thread(content,q):
    ret_con={'none','none'}
    new_user = User(-1,content['first_name'],content['last_name'],content['address'],content['city'],content['country'],content['phone_number']
        ,content['email'],content['password'])
    
    exists=check_if_exists(content['email'])
    inserted=-1
    if exists==-1:
        inserted = insert_user(new_user)
    else:
        ret_con={'registered':'unsuccessfully, user with this email exists'}
    if inserted!=-1:
        ret_con={'registered':'successfully'}
    
    q.put(ret_con)

@main.route("/registerUser", methods=['POST'])
def register():
    content = {'none' : 'none'}
    try:
        content=flask.request.json
    except ValueError as err:
        print("Register content error {}".format(err))
    
    """new_user = User(-1,content['first_name'],content['last_name'],content['address'],content['city'],content['country'],content['phone_number']
        ,content['email'],content['password'])
    
    exists=check_if_exists(content['email'])
    inserted=-1
    if exists==-1:
        inserted = insert_user(new_user)
    else:
        content={'registered':'unsuccessfully, user with this email exists'}
    if inserted!=-1:
        content={'registered':'successfully'}"""

    q = Queue()
    p = Process(target=register_user_thread, args=(content,q,))
    p.start()
    p.join()
    content=q.get()    # prints "[42, None, 'hello']"
    return jsonify(content)


@main.route('/logOut',methods=['POST'])
def logOut():
    content ={'none':'none'}
    content=flask.request.json
    _session_id=content['session_id']
    succ = delete_session(_session_id)
    if succ:
        content={'none':'logedOut'}

    return jsonify(content)

@main.route('/updateUser',methods=['POST'])
def updateUser():
    content = {'none' : 'none'}
    try:
        content=flask.request.json
    except ValueError as err:
        print("Register content error {}".format(err))
    
    new_user = User(-1,content['first_name'],content['last_name'],content['address'],content['city'],content['country'],content['phone_number']
        ,content['email'],content['password'])
    
    inserted=update_user(new_user)
    if inserted:
        content={'updated':'successfully'}
    else:
        content={'updated':'unsuccessfully'}

    return jsonify(content)

#https://auth0.com/blog/developing-restful-apis-with-python-and-flask/ 
#Api funkcionalnost
#https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
# user id kako identifikovati od koga stize zahtev
    