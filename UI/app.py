import os
from flask import Flask


# blueprint import
from Blueprints.main.views import main
from Blueprints.bank.views import bank
#from blueprints.contact.views import contact
#from blueprints.about.views import about

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided by the user / environment
    #app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'development'
    app.config['SECRET_KEY'] = 'GDtfDCFYjD'
    #app.config['DEBUG'] = False  # actually I want debug to be off now
    # setup all our dependencies
    #database.init_app(app)
    #commands.init_app(app)
    
    # register blueprint
    app.register_blueprint(main)
    app.register_blueprint(bank)
    #app.register_blueprint(contact)
    #app.register_blueprint(about)
    

    return app


if __name__ == "__main__":
    create_app().run(host='0.0.0.0',port=5001) #port=5001