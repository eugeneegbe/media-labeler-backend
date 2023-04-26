
from flask import abort, Blueprint, request, jsonify
import json
from flask_cors import cross_origin

from server import app, db
from server.main.utils import commit_changes_to_db, get_serialized_data
from server.models import User, Contribution
from server.contributions.utils import create_contribution


contributions = Blueprint('contributions', __name__)


@contributions.route('/contributions',  methods=['GET'])
@cross_origin()
def getContributions():
    contributions_of_type = []
    contrib_type = request.args.get('type')
    all_contributions = Contribution.query.all()
    if contrib_type:
        for contribution in  all_contributions:
            if contribution.type == contrib_type:
                contributions_of_type.append(contribution)
        return get_serialized_data(contributions_of_type)

    return get_serialized_data(all_contributions)


@contributions.route('/contributions', methods=['POST'])
@cross_origin()
def addContribution():
    data = json.loads(request.data)
    contribution = create_contribution(data)
    if not contribution:
        abort(400, 'Contribution was not created')
    db.session.add(contribution)
    if commit_changes_to_db():
        return "success"
    return "Failure"
