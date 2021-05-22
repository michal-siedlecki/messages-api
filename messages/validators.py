import json
from config import MAX_CONTENT, TOKEN
from flask import jsonify, make_response

with open('messages/error_codes.json', 'r') as f:
    error_msgs = json.load(f)


# :::::::::::::::::: VALIDATORS ::::::::::::::::::::::::::


def pk_is_valid(pk):
    try:
        int(pk)
    except (ValueError or TypeError):
        return 'not_found_error_404'
    return True


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
