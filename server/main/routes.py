import os

from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import current_user


main = Blueprint('main', __name__)


@main.route('/')
def home():
    username = session.get('username', None)
    session_language = session.get('lang', None)
    if not session_language:
        session_language = 'en'

    session['next_url'] = request.url
    return render_template('main/home.html',
                           title='Home',
                           session_language=session_language,
                           username=username,
                           current_user=current_user)

