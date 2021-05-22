from flask import request, jsonify, make_response

import config
from messages.models import MessageModel
from messages.validators import pk_is_valid, content_is_valid, token_is_valid, error_response
from messages.links import home_links, get_app_info


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


def message_create_view() -> object:
    content = request.get_json().get('content')
    if not content_is_valid(content):
        return error_response(err_code=content_is_valid(content))

    token = request.get_json().get('password')
    if not token_is_valid(token):
        return error_response(err_code="unauthorized_403")

    message = MessageModel(content=content, views=0)
    message.save()
    return make_response(messages_list_view(), 201)


def message_detail_view(pk) -> object:
    if not pk_is_valid(pk):
        return error_response(pk_is_valid(pk))

    message = MessageModel.query.filter_by(id=pk).first()
    if not message:
        return error_response(err_code="not_found_error_404")

    message.add_view()
    return make_response(jsonify(message.serialize_detail), 200)


def message_update_view(pk) -> object:
    if not pk_is_valid(pk):
        return error_response(pk_is_valid(pk))

    content = request.get_json().get('content')
    if not content_is_valid(content):
        return error_response(err_code=content_is_valid(content))

    password = request.get_json().get('password')
    if not token_is_valid(password):
        return error_response("unauthorized_403")

    message = MessageModel.query.filter_by(id=pk).first()
    message.update_content(content)
    return message_detail_view(pk)


def message_delete_view(pk) -> object:
    if not pk_is_valid(pk):
        return error_response(pk_is_valid(pk))

    message = MessageModel.query.filter_by(id=pk).first()
    if not message:
        return error_response('not_found_error_404')

    password = request.get_json().get('password')
    if not token_is_valid(password):
        return error_response("unauthorized_403")

    message.delete()
    return messages_list_view()

