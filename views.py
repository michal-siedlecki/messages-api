import json

from flask import request, jsonify, make_response

import config
from app import db
from models import MessageModel, message_schema, messages_schema


with open('utils/error_codes.json', 'r') as f:
    error_msgs = json.load(f)

TOKEN = config.TOKEN
API_URL = config.API_URL
MAX_CONTENT = config.MAX_CONTENT

# :::::::::::::::::: UTILS ::::::::::::::::::::::::::

def get_app_info():
    return {
        'App name': 'Messages API',
        'links':
            {
                'self': '',
                'items': ''
            }
    }


def home_links(request):
    host = request.headers.get('Host')
    path = f'http://{host}{request.path}'
    links = {
        'links': {
            'self': path,
            'items': f'{path}{API_URL}'
        }
    }
    return links


def list_link(request):
    host = request.headers.get('Host')
    path = f'http://{host}{request.path}{API_URL}'
    links = {
        'links': {
            'items': f'{path}{API_URL}'
        }
    }
    return links


def detail_link(request, id):
    host = request.headers.get('Host')
    path = f'http://{host}{request.path}{API_URL}'
    links = {
        'links': {
            'self': f'{path}{API_URL}/{id}',
            'items': f'{path}{API_URL}'
        }
    }
    return links


# :::::::::::::::::: API VIEWS ::::::::::::::::::::::::::


def info_view():
    links = home_links(request)
    app_info = get_app_info()
    app_info.update(links)
    return make_response(jsonify(app_info), 200)


def messages_list_view() -> object:
    messages = MessageModel.query.all()
    for message in messages:
        message.views += 1
        db.session.add(message)
        db.session.commit()

    return messages_schema.jsonify(messages)


def message_detail_view(id) -> object:
    message = MessageModel.query.filter_by(id=id).first()
    if not message:
        return make_response(jsonify(**error_msgs.get('not_found_error_404')), 404)

    message.views += 1
    db.session.add(message)
    db.session.commit()

    return make_response(message_schema.jsonify(message), 200)


def message_create_view() -> object:

    content = request.get_json().get('content')
    if len(content) > MAX_CONTENT:
        e = error_msgs.get('payload_too_large_413')
        return make_response(jsonify(e), 413)
    if content == "":
        e = error_msgs.get('bad_request_400')
        return make_response(jsonify(**e), 400)

    password = request.get_json().get('password')


    if password == TOKEN:
        message = MessageModel(content=content, views=0)
        db.session.add(message)
        db.session.commit()

        return make_response(messages_list_view(), 201)
    e = error_msgs.get('unauthorized_403')
    return make_response(jsonify(**e), 403)


def message_update_view(id) -> object:
    content = request.get_json().get('content')
    if len(content) > MAX_CONTENT:
        e = error_msgs.get('payload_too_large_413')
        return make_response(jsonify(**e), 413)
    if content == "":
        e = error_msgs.get('bad_request_400')
        return make_response(jsonify(**e), 400)

    password = request.get_json().get('password')


    if password == TOKEN:
        message = MessageModel.query.filter_by(id=id).first()
        message.content = content
        db.session.add(message)
        db.session.commit()

        return message_detail_view(id)

    e = error_msgs.get('unauthorized_403')
    return make_response(jsonify(**e), 403)


def message_delete_view(id) -> object:
    message = MessageModel.query.filter_by(id=id).first()
    if message:
        password = request.get_json().get('password')


        if password == TOKEN:
            db.session.delete(message)
            db.session.commit()

        return messages_list_view()
    else:
        e = error_msgs.get('not_found_error_404')
        return make_response(jsonify(**e), 404)
