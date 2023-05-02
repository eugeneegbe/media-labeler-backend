import requests
from flask import Blueprint, request, Response 
import json
from flask_cors import cross_origin

from server import app, db
from server.main.utils import get_serialized_data
from server.models import Image, Category


images = Blueprint("images", __name__)


@images.route("/images")
@cross_origin()
def getImages():
    category_name = request.args.get("category")
    if not category_name:
        return Response(status=404, response=json.dumps({"message": "Category May be Invalid"}))
    category = Category.query.filter_by(name=category_name).first()
    all_images = Image.query.all()
    filtered_images = []

    for image in all_images:
        if image.category_id == category.id:
            filtered_images.append(image)
    return get_serialized_data(filtered_images)


@images.route("/images/describe")
@cross_origin()
def getImageDescription():
    print('were hit')
    filename = request.args.get("filename")
    if not filename:
        return Response(status=404, response=json.dumps({"message": "Please provide a file name"}))
    commons_url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "imageinfo",
        "iiprop": "extmetadata",
        "titles": filename,
        "format": "json"
    }
    session = requests.Session()
    resp = session.get(commons_url, params=params).json()
    if not resp:
        return Response(status=404, response=json.dumps({"message": "Could not get file descrription"}))
    pages = resp['query']['pages']
    if not pages.keys():
        return ''
    page_id = list(resp['query']['pages'].keys())[0]
    if not resp['query']['pages'][page_id].keys():
        return ''
    imageinfo = pages[page_id]['imageinfo'][0]
    if not imageinfo.keys():
        return ''
    extmetadata = imageinfo['extmetadata']
    if not extmetadata.keys():
        return ''
    imagedesc = extmetadata['ImageDescription']
    if not imagedesc:
        return ''
    return imagedesc['value']
