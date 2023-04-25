
from flask import Blueprint

from flask_cors import cross_origin

from server import app, db
from server.main.utils import get_serialized_data
from server.models import Image


images = Blueprint('images', __name__)


@images.route('/images')
@cross_origin()
def getImages():
    all_images = Image.query.all()
    return get_serialized_data(all_images)