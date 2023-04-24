
from flask import Blueprint, flash, redirect, request, session, url_for, make_response
from flask_login import current_user, login_user, logout_user
import mwoauth

from flask_cors import cross_origin

from server import app
# from isa.main.utils import commit_changes_to_db
from server.models import User


users = Blueprint('users', __name__)


@users.route('/api/set-login-url')
@cross_origin()
def setLoginUrl():
    session['next_url'] = request.args.get('url')
    return "success"

@users.route('/login')
@cross_origin()
def login():
    """Initiate an OAuth login.
    
    Call the MediaWiki server to get request secrets and then redirect the
    user to the MediaWiki server to sign the request.
    """
    consumer_token = mwoauth.ConsumerToken(
        app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    try:
        redirect_string, request_token = mwoauth.initiate(
            app.config['OAUTH_MWURI'], consumer_token)
    except Exception:
        app.logger.exception('mwoauth.initiate failed')
        return redirect(request.referrer)
    else:
        session['request_token'] = dict(zip(
            request_token._fields, request_token))
        return redirect(redirect_string)


@users.route('/auth/mediawiki/callback')
@cross_origin()
def oauth_callback():
    """OAuth handshake callback."""
    if 'request_token' not in session:
        flash(u'OAuth callback failed. Are cookies disabled?')
        return redirect(url_for('main.home'))

    consumer_token = mwoauth.ConsumerToken(
        app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])

    try:
        access_token = mwoauth.complete(
            app.config['OAUTH_MWURI'],
            consumer_token,
            mwoauth.RequestToken(**session['request_token']),
            request.query_string)

        identity = mwoauth.identify(
            app.config['OAUTH_MWURI'], consumer_token, access_token)    
    except Exception:
        app.logger.exception('OAuth authentication failed')
    
    else:
        session['access_token'] = dict(zip(
            access_token._fields, access_token))
        session['username'] = identity['username']
    return redirect(url_for('users.take_me_home'))


@users.route('/current-user', methods=['GET'])
@cross_origin()
def get_current_user():
    data = {}
    data["username"] = "Anonymous"
    if session['username']: 
        data["username"] = session['username']
    return data


@users.route('/take-me-back', methods=['GET'])
@cross_origin()
def take_me_home():
    return redirect(app.config['FE_BASE_URL'])


@users.route('/logout')
@cross_origin()
def logout():
    """Log the user out by clearing their session."""
    try:
        session.clear()
        return "sucess"
    except Exception as e:
        raise e