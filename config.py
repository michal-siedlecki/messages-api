import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
os.chdir(basedir)


def get_tokens():
    with open('tokens.txt', 'r') as f:
        tokens = f.read().split('\n')
    return tokens


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '21fsd32fds3rvfsdr3gf'
app.config['DEBUG'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

clients_num = 5
tokens = get_tokens()
API_VERSION = 'v1'
API_URL = 'api/' + API_VERSION
MAX_CONTENT_LENGTH = 160

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
