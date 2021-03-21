from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from todolistsapi.utils.utils import abort_if_id_list_doesnt_exist, get_username, get_TODOLISTS, set_TODOLISTS

class TodolistId(Resource):
    def get(self, id_list:int) -> Dict[str, Any]:
        """ 
        Return todolist
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
        responses : 
            200:
                description : All elements in todolist
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
            'message': 'Successful get todolist',
            'data': TODOLISTS[id_list]
        }           
        return response, 200
    
    def delete(self, id_list: int) -> Dict[str,Any]:
        """
        Delete a todolist
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
              description: The id of the todolist to delete
              required: true
              schema:
                type: integer
                minimum: 1
        responses:
            200:
                description: JSON representing the todolists
            401: 
                description: The token or id are missing or are not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        TODOLISTS = get_TODOLISTS(username)
        abort_if_id_list_doesnt_exist(TODOLISTS, id_list)
        del TODOLISTS[id_list]
        set_TODOLISTS(username, TODOLISTS)
        response = {
            'status': 200,
            'message': 'Successful delete todolist',
            'data': TODOLISTS
        } 
        return response, 200

    def patch(self, id_list:int) -> Dict[str, Any]:
        """
        Edit a todolist
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
              description: The id of the list to edit
              required: true
              schema:
                type: integer
                minimum: 1
            - in: body
              name: attribute
              description : The edited name of the todolist
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
        responses:
            202:
                description: JSON representing edited todolist
            400: 
                description: The paramaters ars missing or are not correct
            401: 
                description: The token or id are missing or are not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type = str, required = True, help='Missing the name of the list')
        args = body_parser.parse_args(strict = True)
        try:
            TODOLISTS = get_TODOLISTS(username)
            abort_if_id_list_doesnt_exist(TODOLISTS, id_list)
            name = args['name']
            TODOLISTS[id_list]['name'] = name
            set_TODOLISTS(username, TODOLISTS)
            response = {
                'status': 202,
                'message': 'Successful patch todolist',
                'data': TODOLISTS[id_list]
            }             
            return response, 202
        except:
            abort(400, message = 'Error patch list', data = '')
