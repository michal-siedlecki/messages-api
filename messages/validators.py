import json
from config import MAX_CONTENT, TOKEN
from flask import request, jsonify, make_response

with open('error_codes.json', 'r') as f:
    error_msgs = json.load(f)

# :::::::::::::::::: DECORATORS ::::::::::::::::::::::::::



def validate_pk(pk):
    try :
        pk = int(pk)
    except ValueError:
        return make_response(jsonify(**error_msgs.get('not_found_error_404')), 404)
    try :
        pk = int(pk)
    except TypeError:
        return make_response(jsonify(**error_msgs.get('not_found_error_404')), 404)
    return pk


def content_is_valid(content):
    if len(content) > MAX_CONTENT:
        return 'payload_too_large_413'
    if content == "":
        return 'bad_request_400'
    return True


def token_is_valid(x):
    return x == TOKEN


def error_response(err_code):
    e = error_msgs.get(err_code)
    return make_response(jsonify(**e), e['code'])