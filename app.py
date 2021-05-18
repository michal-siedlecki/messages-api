from flask import request, jsonify

from models import MessageModel, message_schema, messages_schema
from config import app

# ====== CONSTANTS ==========
API_VERSION = 'v1'
API_URL = 'api/' + API_VERSION

# Create some test data for app.
app_info = {
    'App name': 'Messages API',
    'API version': API_VERSION,
    'links':
        {
            'self': '',
            'items': ''
        }
}

# :::::::::::::::::: UTILS ::::::::::::::::::::::::::

def create_links(request):
    host = request.headers.get('Host')
    path = request.path
    links = {
        'links': {
            'self': 'http://' + host + path,
            'items': 'http://' + host + path + API_URL + '/messages'
        }
    }
    return links


# :::::::::::::::::: API VIEWS ::::::::::::::::::::::::::


# A route to return app info.
@app.route('/', methods=['GET'])
def home():
    """
        This function returns basic application info

        :return:        {'App name': 'Messages API',
                        'API version': API_VERSION,}
    """
    links = create_links(request)
    app_info.update(links)

    return jsonify(app_info)


# A route to return all of the available entries in the system.
@app.route('/' + API_URL + '/messages', methods=['GET'])
def listMessages() -> object:
    result = MessageModel.query.all()
    return messages_schema.jsonify(result)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
