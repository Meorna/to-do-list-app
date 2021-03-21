import json
import jwt
import os

from datetime import datetime, timedelta
from flask_restful import abort

from todolistsapi import config


def abort_if_id_list_doesnt_exist(TODOLISTS, id_list: int):
    if len(TODOLISTS) <= id_list:
        abort(404, message="id_list doesn't exist", data = id_list)

def abort_if_task_id_doesnt_exist(TODOLISTS, id_list: int, id_todo: int):
    if len(TODOLISTS[id_list]['list']) <= id_todo:
        abort(404, message="id_todo doesn't exist", data = id_todo)

def generate_encoded_jwt(username):
    return jwt.encode({
        'sub': username,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        config.API_KEY, algorithm="HS256")

def generate_decod_jwt(encoded_jwt):
    return jwt.decode(encoded_jwt, config.API_KEY, algorithms='HS256')

def get_username(auth_headers):
    if len(auth_headers) != 2:
        abort(401, message="The token is invalid", data=False)
    try:
        token = auth_headers[1]
        data = generate_decod_jwt(token)
        username = data['sub']
        if not os.path.exists('todolistsapi/services/' + username + '/todolistsService.json'):
            abort(404, message = 'Error users data file not found', data = '')     
        return username
    except jwt.ExpiredSignatureError:
        abort(401, message = 'The token has expired', data = '')
    except (jwt.InvalidTokenError, Exception):
        abort(401, message = 'The token is invalid', data = '')  
    except:
        abort(401, message = 'Get username unauthorized', data = '')

def get_TODOLISTS(username):
    try:
        with open('todolistsapi/services/' + username + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)
            fichier.close
            return TODOLISTS
    except (OSError, IOError):
            abort(404, message = 'Error user data file not found', data = '')  

def set_TODOLISTS(username, TODOLISTS): 
    try:
        with open('todolistsapi/services/' + username + '/todolistsService.json', 'w') as fichier:
            json.dump(TODOLISTS, fichier, indent = 4)
            fichier.close
    except (OSError, IOError):
            abort(404, message = 'Error user data file not found', data = '') 