
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
    filtered_category = []
    try:
        all_categories = Category.query.all()
        if type:
            for category in all_categories:
                if category.type == type:
                    filtered_category.append(category)
            return get_serialized_data(filtered_category)
        return get_serialized_data(all_categories)
    except:
        db.session.rollback()
    return Response(status=404, response=json.dumps({'message': 'No categories at the moment'}))


@categories.route('/categories/add',  methods=['POST'])
@cross_origin()
def addCategory():
    data = json.loads(request.data)
    if not data['categories']:
        return Response(status=404, response=json.dumps({'message': 'No category provided'}))
    categories_data = data['categories'].split(',')
    for category in categories_data:
        names = get_image_names(category)
        if names == 'Failure':
            return Response(status=404, response=json.dumps({'message': 'Category May be Invalid'}))
        category_exits = Category.query.filter_by(name=category).first()
        if category_exits:
            continue
        new_category = Category(
            name=category,
            type=data['type']
        )
        db.session.add(new_category)
        if not commit_changes_to_db():
            return Response(status=404, response=json.dumps({'message':'Category could not be added'}))
        for image in names:
            if 'imageinfo' in image:
                image = Image(filename=image['title'],
                            url=image['imageinfo'][0]['url'],
                            category_id=new_category.id,
                            description=image['imageinfo'][0]['descriptionurl'])
                db.session.add(image)
        if not commit_changes_to_db():
            return Response(status=404, response={'message': 'Category images could not be added'})
    return Response(status=200, response={'message': 'success'})
