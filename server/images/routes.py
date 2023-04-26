
from flask import Blueprint, request, Response
import json
from flask_cors import cross_origin

from server import app, db
from server.main.utils import get_serialized_data
from server.models import Image, Category


images = Blueprint('images', __name__)


@images.route('/images')
@cross_origin()
def getImages():
    category_name = request.args.get('category')
    if not category_name:
        return Response(status=404, response=json.dumps({'message': 'Category May be Invalid'}))
    category = Category.query.filter_by(name=category_name).first()
    all_images = Image.query.all()
    filtered_images = []

    for image in all_images:
        if image.category_id == category.id:
            filtered_images.append(image)
    return get_serialized_data(filtered_images)

