from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.routes import initialize_routes

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

initialize_routes(api)