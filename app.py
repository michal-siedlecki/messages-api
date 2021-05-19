import uuid

from flask import request, jsonify, make_response

from models import MessageModel, message_schema, messages_schema
from config import app, db, tokens, API_URL, app_info, MAX_CONTENT_LENGTH

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


# A route to return app info.
@app.route('/', methods=['GET'])
def home():
    """
        This function returns basic application info

        :return:        {'App name': 'Messages API',
                        'API version': API_VERSION,}
    """
    links = home_links(request)
    app_info.update(links)

    return make_response(jsonify(app_info), 200)


# A route to return all of the available entries in the system.
@app.route('/' + API_URL + '/messages', methods=['GET'])
def MessagesListView() -> object:
    """
        This function returns all messages in the system

        :rtype: object
        :return:
        {
            "id": "1",
            "content": "Russia’s Foreign Intelligence Service (SVR) director Sergei Naryshkin had said he was “flattered” by the accusations from the UK and US but denied involvement.",
            "views": 23
        },
        {
            "id": "2",
            "content": "Turtle nesting and hatching season is between February and August in Puerto Rico and its beaches attract several protected species, including the endangered leatherback.",
            "views": 3
        }
   """

    messages = MessageModel.query.all()
    for message in messages:
        message.views += 1
        db.session.add(message)
        db.session.commit()

    return messages_schema.jsonify(messages)


@app.route('/' + API_URL + '/messages/<id>', methods=['GET'])
def MessagesDetailView(id) -> object:
    """
        This function returns detail view for message with secified id.

        :param id:
        :return:
        :rtype: object
        :return:
        {
            "id": "1",
            "content": "Russia’s Foreign Intelligence Service (SVR) director Sergei Naryshkin had said he was “flattered” by the accusations from the UK and US but denied involvement.",
            "views": 23
        }
   """

    message = MessageModel.query.filter_by(id=id).first()
    if not message:
        return make_response(jsonify(**not_found_error_404), 404)

    message.views += 1
    db.session.add(message)
    db.session.commit()

    return make_response(message_schema.jsonify(message), 200)


# A route to create a new message.
@app.route('/' + API_URL + '/messages', methods=['POST'])
def MessagesCreateView() -> object:
    """
        This function creates a new message.

        :rtype: object
        :return:
        {
            "id": "1",
            "content": "Russia’s Foreign Intelligence Service (SVR) director Sergei Naryshkin had said he was “flattered” by the accusations from the UK and US but denied involvement.",
            "views": 23
        },
        {
            "id": "2",
            "content": "Turtle nesting and hatching season is between February and August in Puerto Rico and its beaches attract several protected species, including the endangered leatherback.",
            "views": 3
        }
   """
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

            return MessagesListView()

    return make_response(jsonify(unauthorized_403), 403)


# A route to create a new message.
@app.route('/' + API_URL + '/messages/<id>', methods=['PATCH'])
def MessagesUpdateView(id) -> object:
    """
        This function updates the existing message.

        :rtype: object
        :return:
        {
            "id": "1",
            "content": "Russia’s Foreign Intelligence Service (SVR) director Sergei Naryshkin had said he was “flattered” by the accusations from the UK and US but denied involvement.",
            "views": 23
        }

   """
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

            return MessagesDetailView(id)

    return make_response(jsonify(unauthorized_403), 403)


@app.route('/' + API_URL + '/messages/<id>', methods=['DELETE'])
def MessagesDeleteView(id) -> object:
    """
        This function delete message with secified id.

        :param id:
        :return:
        :rtype: object
        :return:
        {
            "id": "1",
            "content": "Russia’s Foreign Intelligence Service (SVR) director Sergei Naryshkin had said he was “flattered” by the accusations from the UK and US but denied involvement.",
            "views": 23
        }
   """
    message = MessageModel.query.filter_by(id=id).first()
    if message:
        password = request.get_json().get('password')

        for token in tokens:
            if password == token:

                db.session.delete(message)
                db.session.commit()

        return MessagesListView()
    else:
        return make_response(jsonify(not_found_error_404), 404)




if __name__ == '__main__':
    app.run(host='localhost', port=5000)
