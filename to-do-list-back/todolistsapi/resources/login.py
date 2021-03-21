import json
import os
from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from todolistsapi.utils.utils import generate_encoded_jwt

class Login(Resource):
    def post(self) -> Dict[str, Any]:
        """
        Login to an account
        ---
        tags: 
            - Flask API
        parameters:
            - in: body
              name: attribute
              description : The username and the hashed password of the user
              schema: 
                type: object
                required:
                    -username
                    -password
                properties: 
                    username: 
                        type: string
                    password:
                        type: string
        responses:
            200:
                description: Successful account login
            400: 
                description: The paramaters are missing or are not correct
            404:
                description: The users file not found
        """
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('username', type = str, required = True, help='Missing the username of the user')
        body_parser.add_argument('password', type = str, required = True, help='Missing the password of the user')
        args= body_parser.parse_args(strict=True)
        try:
            username = args['username']
            password_hash= args['password']

            with open('todolistsapi/services/usersService.json', 'r') as fichier:
                USERS = json.load(fichier)

            for user in USERS:
                if(username == user['username'] and password_hash == user['password']):
                    token = generate_encoded_jwt(username)
                    response = {
                        'status': 200,
                        'message': 'Successful authentication',
                        'data': token
                    }
                    return(response, 200)
        except (OSError, IOError):
            abort(404, message = 'Error users file not found', data = '')
        else:
            abort(400, message = 'Account Login Failed', data = '')