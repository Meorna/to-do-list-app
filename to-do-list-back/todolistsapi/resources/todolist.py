import json
from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from todolistsapi.utils.utils import generate_decod_jwt, get_username, get_TODOLISTS, set_TODOLISTS

class Todolist(Resource):
    def get(self) -> Dict[str, Any]:
        """ 
        Return all todolists
        ---
        tags: 
            - Flask API
        parameters:
            - in: header
              name: Authorization
              description: user token
              required: true
              securitySchemes:
                bearerAuth:
                    type: http
                    scheme: bearer
                    bearerFormet: JWT
        responses : 
            200:
                description : todolists
            401: 
                description: The token is missing or is not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        TODOLISTS = get_TODOLISTS(username)
        response = {
            'status': 200,
            'message': 'Successful get TODOLISTS',
            'data': TODOLISTS
        }
        return response, 200

    def put(self) -> Dict[str, Any]:
        """
        Add a new list
        ---
        tags: 
          - Flask API
        parameters:
          - in: header
            name: Authorization
            description: user token
            required: true
            securitySchemes:
                bearerAuth:
                    type: http
                    scheme: bearer
                    bearerFormet: JWT
          - in: body
            name: attributes
            description: The name and creation date of the list to create
            schema:
                type: object
                required:
                    -name
                    -created_at
                properties:
                    name:
                        type: string
                    created_at:
                        type: string
        responses:
            201:
                description: JSON representing created todolist
            400:
                decription: The Parameter are missing or not correct
            401: 
                description: The token is missing or is not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type = str, required = True, help = 'Missing the name of the list')
        body_parser.add_argument('created_at', type = str, required = True, help = 'Missing the date of the list')
        args = body_parser.parse_args(strict = True)
        try:
            name = args['name']
            created_at = args['created_at']
            todolist = {'name': name, 'created_at': created_at, 'list':[]}
            TODOLISTS = get_TODOLISTS(username)
            TODOLISTS.append(todolist)
            TODOLISTS = set_TODOLISTS(username, TODOLISTS)
            response = {
                'status': 201,
                'message': 'Successful put todolist',
                'data': todolist
            }
            return response, 201
        except:
            abort(400, message = 'Missing parameters', data = '')