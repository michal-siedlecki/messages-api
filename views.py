from flask import request, jsonify, make_response

from models import MessageModel, message_schema, messages_schema
from config import db, tokens, API_URL, app_info, MAX_CONTENT_LENGTH


# :::::::::::::::::: UTILS ::::::::::::::::::::::::::

def home_links(request):
    host = request.headers.get('Host')
    path = f'http://{host}{request.path}'
    links = {
        'links': {
            'self': path,
            'items': f'{path}{API_URL}/messages'
        }
    }
    return links

def list_link(request):
    host = request.headers.get('Host')
    path = f'http://{host}{request.path}{API_URL}'
    links = {
        'links': {
            'items': f'{path}{API_URL}/messages'
        }
    }
    return links

def detail_link(request, id):
    host = request.headers.get('Host')
    path = f'http://{host}{request.path}{API_URL}'
    links = {
        'links': {
            'self': f'{path}{API_URL}/messages/{id}',
            'items': f'{path}{API_URL}/messages'
        }
    }
    return links


# :::::::::::::::::: ERRORS ::::::::::::::::::::::::::
bad_request_400 = {
        "code": 400,
        "name": "Bad Request",
        "description": f"There is no content in request",
    }

unauthorized_403 = {
        "code": 403,
        "name": "Unauthorized",
        "description": "Unauthorized users cannot create, update or delete messages",
    }

not_found_error_404 = {
        "code": 404,
        "name": "Not found",
        "description": "Not found the resource with requested URL.",
    }

method_not_allowed_405 = {
        "code": 405,
        "name": "Method Not Allowed",
        "description": "The method is not allowed for the requested URL.",
    }


payload_too_large_413 = {
        "code": 413,
        "name": "Payload Too Large",
        "description": f"The maximum content length is {MAX_CONTENT_LENGTH}",
    }


# :::::::::::::::::: API VIEWS ::::::::::::::::::::::::::


def info_view():

    links = home_links(request)
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
        return make_response(jsonify(**not_found_error_404), 404)

    message.views += 1
    db.session.add(message)
    db.session.commit()

    return make_response(message_schema.jsonify(message), 200)


def message_create_view() -> object:

    content = request.get_json().get('content')
    if len(content) > MAX_CONTENT_LENGTH:
        return make_response(jsonify(payload_too_large_413), 413)
    if content == "":
        return make_response(jsonify(bad_request_400), 400)

    password = request.get_json().get('password')

    for token in tokens:
        if password == token:
            message = MessageModel(content=content, views=0)
            db.session.add(message)
            db.session.commit()

            return messages_list_view()

    return make_response(jsonify(unauthorized_403), 403)


def message_update_view(id) -> object:

    content = request.get_json().get('content')
    if len(content) > MAX_CONTENT_LENGTH:
        return make_response(jsonify(payload_too_large_413), 413)
    if content == "":
        return make_response(jsonify(bad_request_400), 400)

    password = request.get_json().get('password')

    for token in tokens:
        if password == token:
            message = MessageModel.query.filter_by(id=id).first()
            message.content = content
            db.session.add(message)
            db.session.commit()

            return message_detail_view(id)

    return make_response(jsonify(unauthorized_403), 403)


def message_delete_view(id) -> object:

    message = MessageModel.query.filter_by(id=id).first()
    if message:
        password = request.get_json().get('password')

        for token in tokens:
            if password == token:

                db.session.delete(message)
                db.session.commit()

        return messages_list_view()
    else:
        return make_response(jsonify(not_found_error_404), 404)
