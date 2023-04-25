import requests

def get_image_names(category):
    session = requests.Session()
    url = 'https://commons.wikimedia.org/w/api.php'
    params = {
        'action': 'query',
        'prop': 'imageinfo|description',
        'iiprop': 'url',
        'generator': 'categorymembers',
        'gcmtitle': category,
        'format': 'json',
        'gcmlimit': 500,
        'formatversion': 2,  # only if the target wiki is running mediawiki 1.25 or above
    }
    resp = session.get(url, params=params).json()

    if 'error' in resp:
        return 'Failure'

    return resp['query']['pages']

