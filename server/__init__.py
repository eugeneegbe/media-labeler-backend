import os
from glob import glob
import logging

import yaml
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_cors import CORS, cross_origin
# from flask_login import LoginManager


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = Flask(__name__)

# Load configuration from YAML file
__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.safe_load(open(os.path.join(__dir__, 'config.yaml'))))

# Another secret key will be generated later
app.config['SQLALCHEMY_DATABASE_URI']
app.config['SECRET_KEY']
app.config['TEMPLATES_AUTO_RELOAD']

# We hook babel to our app


def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

cors = CORS(app)
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)


@app.before_request
def before_request():
    # Update session language
    get_locale()

    if "SERVER_DEV" in app.config and app.config["SERVER_DEV"]:
        session['username'] = "Dev"


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers','Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'main.home'
# login_manager.login_message = 'You Need to Login to Access This Page!'
# login_manager.login_message_category = 'danger'

# we import all our blueprint routes here
from server.main.routes import main
from server.users.routes import users

# Here we register the various blue_prints of our app
app.register_blueprint(main)
app.register_blueprint(users)

app.app_context().push()
