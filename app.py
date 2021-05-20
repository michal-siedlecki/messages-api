from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import app_config, API_URL

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    import views
    # A route to return messages_app info.
    @app.route('/', methods=['GET'])
    def info():
        return views.info_view()


    # A route to return all of the available entries in the system.
    @app.route(f'/{API_URL}', methods=['GET'])
    def list_view() -> object:
        return views.messages_list_view()

    # A route to get message details.
    @app.route(f'/{API_URL}/<pk>', methods=['GET'])
    def detail(pk) -> object:
        return views.message_detail_view(pk)


    # A route to create a new message.
    @app.route(f'/{API_URL}', methods=['POST'])
    def create() -> object:
        return views.message_create_view()


    # A route to create a new message.
    @app.route(f'/{API_URL}/<pk>', methods=['PATCH'])
    def update(pk) -> object:
        return views.message_update_view(pk)


    # A route to delete message.
    @app.route(f'/{API_URL}/<pk>', methods=['DELETE'])
    def delete(pk) -> object:
        return views.message_delete_view(pk)


    return app


if __name__ == '__main__':
    app = create_app('development')
    db.init_app(app)
    ma.init_app(app)
    app.run(host='localhost', port=5000)
