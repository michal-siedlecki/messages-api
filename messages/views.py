import json

from flask import request, jsonify, make_response

import config
from app import db
from messages.models import MessageModel
from messages.validators import validate_pk, validate_content
from messages.links import home_links, get_app_info

with open('error_codes.json', 'r') as f:
    error_msgs = json.load(f)

TOKEN = config.TOKEN
API_URL = config.API_URL
MAX_CONTENT = config.MAX_CONTENT


# :::::::::::::::::: API VIEWS ::::::::::::::::::::::::::


def info_view():
    links = home_links(request)
    app_info = get_app_info()
    app_info.update(links)
    return make_response(jsonify(app_info), 200)


def messages_list_view() -> object:
    messages = MessageModel.query.all()
    for message in messages:
        message.add_view()

    return jsonify([m.serialize for m in messages])


def message_detail_view(pk_str) -> object:
    pk = validate_pk(pk_str)
    message = MessageModel.query.filter_by(id=pk).first()
    if not message:
        return make_response(jsonify(**error_msgs.get('not_found_error_404')), 404)

    message.add_view()

    return make_response(jsonify(message.serialize_detail), 200)


def message_create_view() -> object:

    content = request.get_json().get('content')
    content = validate_content(content)
    password = request.get_json().get('password')

    if password == TOKEN:
        message = MessageModel(content=content, views=0)
        message.save()

        return make_response(messages_list_view(), 201)
    e = error_msgs.get('unauthorized_403')
    return make_response(jsonify(**e), 403)


def message_update_view(pk_str) -> object:
    pk = validate_pk(pk_str)
    content = request.get_json().get('content')
    content = validate_content(content)

    password = request.get_json().get('password')

    if password == TOKEN:
        message = MessageModel.query.filter_by(id=pk).first()
        message.content = content
        message.views = 0
        message.save()

        return message_detail_view(pk)

    e = error_msgs.get('unauthorized_403')
    return make_response(jsonify(**e), 403)


def message_delete_view(pk_str) -> object:
    pk = validate_pk(pk_str)
    message = MessageModel.query.filter_by(id=pk).first()
    if message:
        password = request.get_json().get('password')

        if password == TOKEN:
            db.session.delete(message)
            db.session.commit()
            return messages_list_view()
        else:
            e = error_msgs.get('unauthorized_403')
            return make_response(jsonify(**e), 403)

    e = error_msgs.get('not_found_error_404')
    return make_response(jsonify(**e), 404)
