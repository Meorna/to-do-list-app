"""
    Import
"""
from flask import Flask, jsonify
from flask_restful import Api
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from todolistsapi import config
from todolistsapi.resources.account import Account
from todolistsapi.resources.login import Login
from todolistsapi.resources.todolist import Todolist
from todolistsapi.resources.todolistId import TodolistId
from todolistsapi.resources.todolistIdTodo import TodolistIdTodo
from todolistsapi.resources.todolistIdTodoId import TodolistIdTodoId

"""
    Config
"""
app = Flask(__name__)
api = Api(app)

if config.env == "DEVELOPMENT":
    conf = config.DevelopmentConfig
app.config.from_object(conf)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

"""
    API Routes 
"""
api.add_resource(Account, '/account')
api.add_resource(Login, '/login')
api.add_resource(Todolist, '/lists')
api.add_resource(TodolistId, '/lists/<int:id_list>')
api.add_resource(TodolistIdTodo, '/lists/todos/<int:id_list>')
api.add_resource(TodolistIdTodoId, '/lists/todos/<int:id_list>/<int:id_todo>')


"""
    Swagger
"""
@app.route("/swagger")
def swaggerController():
    swag = swagger(app)
    swag['info']['version'] = config.APP_VERSION
    swag['info']['title'] = config.API_NAME
    return jsonify(swag)

swaggerui_blueprint = get_swaggerui_blueprint(
    conf.SWAGGER_URL,
    conf.DATA_SWAGGER,
    config = {
        'app_name': "Flask API"
    },
)
app.register_blueprint(swaggerui_blueprint, url_prefix = conf.SWAGGER_URL)