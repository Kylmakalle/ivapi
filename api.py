import flask
from flask import request, Response
import json
import os
import uuid
from yattag import Doc

from credentials import iv_path

app = flask.Flask(__name__)


def checkJson(s):
    try:
        return json.loads(s)
    except:
        return False


def checkattrs(info):
    if info.get('title'):
        if info.get('photos') and isinstance(info['photos'], list):
            for photo in info['photos']:
                if photo.get('url'):
                    continue
                else:
                    return False  # missing photo url
        elif info.get('audios') and isinstance(info['audios'], list):
            for audio in info['audios']:
                if audio.get('url'):
                    continue
                else:
                    return False  # missing audio url
        else:
            return False  # missing data
            # missing Title


def generate_page(json_info):
    page = str(uuid.uuid4().hex)
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('body'):
            with tag('article'):
                with tag('h1'):
                    text(json_info['title'])
                if json_info.get('comment'):
                    with tag('p'):
                        text(json_info['comment'])
                if json_info.get('photos'):
                    with tag('slideshow'):
                        for photo in json_info['photos']:
                            with tag('figure'):
                                doc.stag('img', src=photo['url'])
                                if photo.get('caption'):
                                    with tag('figcaption'):
                                        text(photo['caption'])
                if json_info.get('audios'):
                    for audio in json_info['audios']:
                        doc.stag('audio', src=audio['url'])
    f = open(iv_path + '{}.html'.format(page), mode='w')
    f.write(doc.getvalue())
    f.close()
    return {'ok': True, 'url': 'https://asergey.me/iv/{}.html'.format(page),
            'iv_url': 'https://t.me/iv?url=https://asergey.me/iv/{}.html&rhash=610fa9e72e9e1a'.format(page)}


@app.errorhandler(401)
def custom_401():
    return Response('Unauthorized', 401, {'ok': False})


@app.route('/', methods=['POST'])
def post_request():
    if request.headers.get('content-type') == 'application/json':
        if True:  # request.headers.get('Bearer'):
            info = request.get_data().decode('utf-8')
            json_info = checkJson(info)
            if json_info:
                if checkattrs(json_info):
                    return generate_page(json_info)
                else:
                    flask.abort(400)
            else:
                flask.abort(400)

        else:
            flask.abort(401)
    else:
        flask.abort(403)


app.run(host='127.0.0.1', port=7000, debug=True)
