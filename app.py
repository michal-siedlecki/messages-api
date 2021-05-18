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
        'id': 'RfVh2ZV7oJWg',
        'title': 'The great title',
        'text': 'Run a marathon in under two hours. Impossible? Not for Nike (@Nike). '
                'Last May, the company brought three of the best runners on the planet '
                'together in Italy to set a new record in a closed-door marathon that '
                'was broadcast live on Twitter.',
        'views': 23
    },
    {
        'id': 'v8VSgK4BM0nMoI',
        'title': 'The another great title',
        'text': 'Run a marathon in under two hours. Impossible? Not for Nike (@Nike). '
                'Last May, the company brought three of the best runners on the planet '
                'together in Italy to set a new record in a closed-door marathon that '
                'was broadcast live on Twitter.',
        'views': 51
    },
    {
        'id': 'v8VSgK4BM0nMoIm',
        'title': 'The first great title',
        'text': 'Run a marathon in under two hours. Impossible? Not for Nike (@Nike). '
                'Last May.',
        'views': 5
    }

]

# =========== UTILS ====================

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

'''
● widok tworzenia wiadomości
● widok edycji (nadpisania treści) wiadomości. Nadpisanie treści wiadomości ma
skutkować wyzerowaniem licznika wyświetleń.
● widok kasowania wiadomości
● widok wiadomości (ma podawać treść wiadomości i licznik “wyświetleń”
danej wiadomości)
● tylko uwierzytelnione requesty mogą tworzyć/modyfikować/usuwać
wiadomości
● uwierzytelnienie nie jest potrzebne do przeczytania wiadomości
● API powinno być zgodne z dobrymi praktykami tworzenia aplikacji web

'''

# A route to return all of the available entries in the system.
@app.route('/' + API_URL + '/messages', methods=['GET'])
def listMessages():
    return jsonify(messages)


# A route to return all of the available entries in the system.
@app.route('/' + API_URL + '/messages', methods=['GET'])
def listMessages():
    return jsonify(messages)




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
