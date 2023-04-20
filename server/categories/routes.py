
from flask import Blueprint
from flask_cors import cross_origin

# from isa.main.utils import commit_changes_to_db
from server.models import Category


categories = Blueprint('categories', __name__)


@categories.route('/categories')
@cross_origin()
def getCategoies():
    all_categories = Category.query.all()
    return all_categories