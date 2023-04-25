
from flask import Blueprint, request, abort, Response
import json
from flask_cors import cross_origin
from server import db

from server.main.utils import commit_changes_to_db, get_serialized_data
from server.categories.utils import get_image_names
from server.models import Category, Image


categories = Blueprint('categories', __name__)


@categories.route('/categories',  methods=['GET'])
@cross_origin()
def getCategoies():
    type = request.args.get('type')
    all_categories = Category.query.filter_by(type=type).all()
    print(all_categories)
    return get_serialized_data(all_categories)


@categories.route('/categories/add',  methods=['POST'])
@cross_origin()
def addCategory():
    data = json.loads(request.data)
    category_exits = Category.query.filter_by(name=data['category']).first()
    if category_exits:
        return Response(status=400, response='Category exists already')
    if not data['category']:
        return Response(status=404, response=json.dumps({'message': 'Category May be Invalid'}))
    names = get_image_names(data['category'])
    if names == 'Failure':
        return Response(status=404, response=json.dumps({'message': 'Category May be Invalid'}))

    category = Category(
        name=data['category'],
        type=data['type']
    )
    db.session.add(category)
    if not commit_changes_to_db():
        return Response(status=404, response=json.dumps({'message':'Category could not be added'}))
    for image in names:
        if 'imageinfo' in image:
            image = Image(filename=image['title'],
                        url=image['imageinfo'][0]['url'],
                        category_id=category.id,
                        description=image['imageinfo'][0]['descriptionurl'])
            db.session.add(image)
    if not commit_changes_to_db():
        return Response(status=404, response={'message': 'Category images could not be added'})
    return Response(status=200, response={'message': 'success'})
