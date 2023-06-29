
from flask import abort, Blueprint, request, send_file, Response
import json
import csv
from flask_cors import cross_origin

from server import app, db
from server.main.utils import commit_changes_to_db, get_serialized_data
from server.models import User, Contribution
from server.contributions.utils import create_contribution


contributions = Blueprint('contributions', __name__)


@contributions.route('/contributions',  methods=['GET'])
@cross_origin()
def getContributions():
    try:
        contributions_of_type = []
        contrib_type = request.args.get('type')
        all_contributions = Contribution.query.all()
        if contrib_type:
            for contribution in  all_contributions:
                if contribution.type == contrib_type:
                    contributions_of_type.append(contribution)
            return get_serialized_data(contributions_of_type)
        return get_serialized_data(all_contributions)
    except:
        db.session.rollback()
    return Response(status=404, response=json.dumps({"data": "There is no contribution yet"}))


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



@contributions.route('/contributions/download', methods=['GET'])
@cross_origin()
def downloadContribution():
    all_contributions = Contribution.query.all()
    if len(all_contributions) == 0:
        abort(400, 'No contributions to download')
    with open('contributions.csv', 'w', newline='') as csvfile:
        csv_writter = csv.writer(csvfile, delimiter=',')
        csv_writter.writerow(["id", "type" ,"username", "filename", "clarity", "identity_type",
                               "depict_accuracy", "subject_relevance", "accuracy", "region", "region_alt",
                               "representation", "created_at"])
        for contribution in all_contributions:
            csv_writter.writerow([contribution.id, contribution.type,
                                 contribution.username, contribution.filename,
                                 contribution.clarity, contribution.identity_type,
                                 contribution.depict_accuracy, contribution.subject_relevance,
                                 contribution.accuracy, contribution.region,
                                 contribution.region_alt, contribution.representation, contribution.created_at])
    return send_file('../contributions.csv',
                     mimetype='text/csv',
                     as_attachment=True)
