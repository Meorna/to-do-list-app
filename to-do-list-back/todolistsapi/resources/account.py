import json
import os

from flask import request
from flask_restful import Resource, reqparse, abort

class Account(Resource):
    def get(self):
        return (200)
    def post(self):
        """
        Create an account
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
            201:
                description: Successful account creation
            400: 
                description: The paramaters are missing or are not correct
            404:
                description: The users file not found
        """
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('username', type = str, required = True, help = 'Missing the username of the user')
        body_parser.add_argument('password', type = str, required = True, help = 'Missing the password of the user')
        args= body_parser.parse_args(strict = True)
        try:
            username = args['username']        
            password_hash = args['password']

            if(len(username) < 1 or len(password_hash) < 1):
                abort(400, message = 'Account Creation Failed : Username or password must be at least 1 char', data = username)

            with open('todolistsapi/services/usersService.json', 'r') as users_service_file:
                USERS = json.load(users_service_file)
                users_service_file.close
            
            for user in USERS:
                if(username == user['username'] and password_hash == user['password']):
                    abort(400, message = 'Account Creation Failed : Username already exists', data = username)

            USERS.append({'username': username, 'password': password_hash})

            with open('todolistsapi/services/usersService.json', 'w') as users_service_file:
                json.dump(USERS, users_service_file, indent=4)
                users_service_file.close

            if not os.path.exists('todolistsapi/services/' + username):
                os.makedirs('todolistsapi/services/' + username)

            with open('todolistsapi/services/' + username + '/todolistsService.json', 'x') as fichier:
                json.dump([], fichier, indent = 4)
                fichier.close

            response = {
                'status': 201,
                'message': 'Successful account creation',
                'data': username
            }
            return (response, 201)
        except (OSError, IOError):
            abort(404, message = 'Error users file not found', data = '')
        else:
            abort(400, message = 'Account Creation Failed', data = '')