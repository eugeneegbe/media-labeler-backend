
from flask import Blueprint

from flask_cors import cross_origin

from server import app, db
# from isa.main.utils import commit_changes_to_db
from server.models import Image


images = Blueprint('images', __name__)


@images.route('/images')
@cross_origin()
def getImages():
    all_images = Image.query.all()
    return all_images