from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from todolistsapi.utils.utils import abort_if_id_list_doesnt_exist, abort_if_task_id_doesnt_exist, get_username, get_TODOLISTS, set_TODOLISTS

class TodolistIdTodoId(Resource):
    def get(self, id_list:int, id_todo:int) -> Dict[str, Any]:
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
            - in: path
              name: id_todo
              description: The id of the task to delete
              required: true
              schema:
                type: integer
                minimum: 1
        responses : 
            200:
                description: JSON representing the todos
            401: 
                description: The token or id are missing or are not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        TODOLISTS = get_TODOLISTS(username)
        abort_if_id_list_doesnt_exist(TODOLISTS, id_list)    
        abort_if_task_id_doesnt_exist(TODOLISTS, id_list, id_todo)
        response = {
            'status': 200,
            'message': 'Successful get todo',
            'data': TODOLISTS[id_list]['list'][id_todo]
        } 
        return response, 200
    
    def delete(self, id_list: int, id_todo:int) -> Dict[str,Any]:
        """
        Delete a task
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
              description: The id of the todolist
              required: true
              schema:
                type: integer
                minimum: 1
            - in: path
              name: id_todo
              description: The id of the task to delete
              required: true
              schema:
                type: integer
                minimum: 1
        responses: 
            200:
                description: JSON representing the todos
            401: 
                description: The token or id are missing or are not correct
            404:
                description: The users file or user data file not found
        """
        auth_headers = request.headers.get('Authorization', '').split()
        username = get_username(auth_headers)
        TODOLISTS = get_TODOLISTS(username)
        abort_if_id_list_doesnt_exist(TODOLISTS, id_list)    
        abort_if_task_id_doesnt_exist(TODOLISTS, id_list, id_todo)
        del TODOLISTS[id_list]['list'][id_todo]
        set_TODOLISTS(username, TODOLISTS)
        response = {
            'status': 200,
            'message': 'Successful delete todo',
            'data': TODOLISTS
        }
        return response, 200
    
    def patch(self, id_list:int, id_todo:int) -> Dict[str, Any]:
        """
        Edit a task
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
              description: The id of the todolist
              required: true
              schema:
                type: integer
                minimum: 1
            - in: path
              name: id_todo
              description: The id of the task to edit
              required: true
              schema:
                type: integer
                minimum: 1
            - in: body
              name: attribute
              description : The edited name of the task
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
                    do: 
                        type: bool
        responses:
            202:
                description: JSON representing edited task
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
        body_parser.add_argument('name', type = str, required = False, help = 'Missing the name of the task')
        body_parser.add_argument('do', type = bool, required = False, help = 'Missing the state of the task')
        args = body_parser.parse_args(strict=True)
        try:
            TODOLISTS = get_TODOLISTS(username)
            abort_if_id_list_doesnt_exist(TODOLISTS, id_list)    
            abort_if_task_id_doesnt_exist(TODOLISTS, id_list, id_todo)
            name = args['name']
            do = args['do']
            if name != None:
                TODOLISTS[id_list]['list'][id_todo]['name'] = name
            if do != None:
                TODOLISTS[id_list]['list'][id_todo]['do'] = do
            set_TODOLISTS(username, TODOLISTS) 
            response = {
                'status': 202,
                'message': 'Successful patch todo',
                'data': TODOLISTS[id_list]['list'][id_todo]
            }   
            return response, 202
        except:
            abort(400, message = 'Error patch todo', data = '')
