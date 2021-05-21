from config import API_URL

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
