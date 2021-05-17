import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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


messages = [
    {
        'title': 'The great title',
        'text': 'Run a marathon in under two hours. Impossible? Not for Nike (@Nike). '
                'Last May, the company brought three of the best runners on the planet '
                'together in Italy to set a new record in a closed-door marathon that '
                'was broadcast live on Twitter.',
        'views': 23
    },
    {
        'title': 'The another great title',
        'text': 'Run a marathon in under two hours. Impossible? Not for Nike (@Nike). '
                'Last May, the company brought three of the best runners on the planet '
                'together in Italy to set a new record in a closed-door marathon that '
                'was broadcast live on Twitter.',
        'views': 51
    },
    {
        'title': 'The first great title',
        'text': 'Run a marathon in under two hours. Impossible? Not for Nike (@Nike). '
                'Last May.',
        'views': 5
    }


]

# A route to return app info.
@app.route('/', methods=['GET'])
def home():
    host = request.headers.get('Host')
    path = request.path
    links = {
        'links': {
            'self': 'http://' + host + path,
            'items': 'http://'+ host + path + API_URL + '/messages'
        }
    }
    app_info.update(links)

    return jsonify(app_info)


# A route to return all of the available entries in the system.
@app.route('/' + API_URL + '/messages', methods=['GET'])
def api_all():
    return jsonify(messages)

app.run()