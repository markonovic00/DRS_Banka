import os
from flask import Flask
import sys

from flask.helpers import url_for


# blueprint import
from Blueprints.main.views import main
from Blueprints.online_acc.views import online_acc
from Blueprints.transactions.views import transactions
from Blueprints.exchange.views import exchange

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided by the user / environment
    #app.config.from_object(os.environ['APP_SETTINGS'])
    
    # setup all our dependencies
    #database.init_app(app)
    #commands.init_app(app)
    
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'GDtfDCFYjD'
    #app.config['DEBUG'] = False  # actually I want debug to be off now

    # register blueprint
    app.register_blueprint(main,url_prefix="/api")
    app.register_blueprint(online_acc,url_prefix="/api")
    app.register_blueprint(transactions, url_prefix="/api")
    app.register_blueprint(exchange,url_prefix="/api")
    

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0',port=5000)