
from flask import Blueprint, flash, redirect, request, session, url_for

from flask_cors import cross_origin

from server import app, db
# from isa.main.utils import commit_changes_to_db
from server.models import User, Contribution


contributions = Blueprint('contributions', __name__)


@contributions.route('/contributions')
@cross_origin()
def getContributions():
    contrib_type = request.args.get('type')
    if type:
        contributions_of_type = []
        contributions_of_type = Contribution.query.filter_by(type=contrib_type).all()
        return contributions_of_type

    all_contributions = Contribution.query.all()
    return all_contributions