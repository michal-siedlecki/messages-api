import json
from config import MAX_CONTENT, TOKEN
from flask import request, jsonify, make_response

with open('error_codes.json', 'r') as f:
    error_msgs = json.load(f)

# :::::::::::::::::: DECORATORS ::::::::::::::::::::::::::



def validate_pk(pk_str):
    try :
        pk = int(pk_str)
    except ValueError:
        return make_response(jsonify(**error_msgs.get('not_found_error_404')), 404)
    try :
        pk = int(pk_str)
    except TypeError:
        return make_response(jsonify(**error_msgs.get('not_found_error_404')), 404)
    return pk

def validate_content(content):
    if len(content) > MAX_CONTENT:
        e = error_msgs.get('payload_too_large_413')
        return make_response(jsonify(**e), 413)
    if content == "":
        e = error_msgs.get('bad_request_400')
        return make_response(jsonify(**e), 400)
    return content

