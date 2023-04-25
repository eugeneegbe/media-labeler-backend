
from flask import Blueprint, request

from flask_cors import cross_origin

from server import app, db
from server.main.utils import get_serialized_data
from server.models import Image, Category


images = Blueprint('images', __name__)


@images.route('/images')
@cross_origin()
def getImages():
    category_name = request.args.get('category')
    category = Category.query.filter_by(name=category_name).first()
    all_images = Image.query.filter_by(category_id=category.id).all()
    return get_serialized_data(all_images)
