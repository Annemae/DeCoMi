import flask_restful

from api.extract_dmn import ExtractDMN

def initialize_routes(api: flask_restful.Api):
    api.add_resource(ExtractDMN, '/extract')
