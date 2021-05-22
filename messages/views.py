import json

from flask import request, jsonify, make_response

import config
from app import db
from messages.models import MessageModel
from messages.validators import validate_pk, content_is_valid, token_is_valid, error_response
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
    if not isinstance(pk, int):
        return pk
    message = MessageModel.query.filter_by(id=pk).first()
    if not message:
        return error_response(err_code="not_found_error_404")

    message.add_view()

    return make_response(jsonify(message.serialize_detail), 200)


def message_create_view() -> object:

    content = request.get_json().get('content')
    if content_is_valid(content) != True:
        return error_response(err_code=content_is_valid(content))
    token = request.get_json().get('password')
    if token_is_valid(token):
        message = MessageModel(content=content, views=0)
        message.save()
        return make_response(messages_list_view(), 201)
    return error_response(err_code="unauthorized_403")



def message_update_view(pk_str) -> object:
    pk = validate_pk(pk_str)
    if not isinstance(pk, int):
        return pk
    content = request.get_json().get('content')
    content = validate_content(content)
    password = request.get_json().get('password')

    if password == TOKEN:
        message = MessageModel.query.filter_by(id=pk).first()
        message.update_content(content)
        return message_detail_view(pk)

    return error_response("unauthorized_403")


def message_delete_view(pk_str) -> object:
    pk = validate_pk(pk_str)
    if not isinstance(pk, int):
        return pk
    message = MessageModel.query.filter_by(id=pk).first()
    if message:
        password = request.get_json().get('password')

        if password == TOKEN:
            db.session.delete(message)
            db.session.commit()
            return messages_list_view()
        else:
            return error_response("unauthorized_403")
    return error_response('not_found_error_404')
