"""
    Settings for the flask application object
"""

"""
    API description for swagger
"""
API_NAME = 'Flask API'
APP_VERSION = '1.0'

"""
    API key for jwt token
"""
API_KEY = 'RSRPLP2021'

"""
    Flask server URL
"""
API_URL = 'http://0.0.0.0:5001'

"""
    API development configuration with swagger
"""
env = 'DEVELOPMENT'
class BaseConfig():
    DEBUG = True

class DevelopmentConfig(BaseConfig):
    SWAGGER_URL ='/docs'
    DATA_SWAGGER = API_URL + '/swagger'