from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from todolistsapi.utils.utils import abort_if_id_list_doesnt_exist, get_username, get_TODOLISTS, set_TODOLISTS

class TodolistIdTodo(Resource):
    def get(self, id_list) -> Dict[str, Any]:
        """ 
        Return todos
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
            - in: path
              name: id_list
              description: The id of the todolist to get
              required: true
              schema:
                type: integer
                minimum: 1
        responses: 
            200:
                description : All elements in todos
            401: 
                description: The token or id are missing or are not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        TODOLISTS = get_TODOLISTS(username)
        abort_if_id_list_doesnt_exist(TODOLISTS, id_list) 
        response = {
            'status': 200,
            'message': 'Successful get todos',
            'data': TODOLISTS[id_list]['list']
        }         
        return response, 200

    def put(self, id_list) -> Dict[str, Any]:
        """
        Add a new task
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
            - in: path
              name: id_list
              description: The id of the todolist to get
              required: true
              schema:
                type: integer
                minimum: 1
            - in: body
              name: attributes
              description: The name, creation date, do state of the task to create
              schema:
                type: object
                required:
                    -name
                    -created_at
                    -do
                properties:
                    name:
                        type: string
                    created_at:
                        type: string
                    do: 
                        type: boolean
        responses:
            201:
                description: JSON representing created task
            400:
                decription: The Parameter are missing or not correct
            401: 
                description: The token or id are missing or are not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type = str, required = True, help = 'Missing the name of the task')
        body_parser.add_argument('created_at', type = str, required = True, help = 'Missing the date of the task')
        body_parser.add_argument('do', type = bool, required = True, help = 'Missing the state of the task')
        args = body_parser.parse_args(strict = True)
        try:
            TODOLISTS = get_TODOLISTS(username)
            abort_if_id_list_doesnt_exist(TODOLISTS, id_list)  
            name = args['name']
            created_at = args['created_at']
            do = args['do']
            todo = {'name': name, 'created_at':created_at, 'do':do}
            TODOLISTS[id_list]['list'].append(todo)
            set_TODOLISTS(username, TODOLISTS)
            response = {
                'status': 201,
                'message': 'Successful put todo',
                'data': todo
            }
            return response, 201
        except:
            abort(400, message = 'Missing parameters', data = '')