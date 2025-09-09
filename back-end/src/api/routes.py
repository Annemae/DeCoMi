"""routes.py file.

Define routes for the API.
Initialize REST API endpoints by registering resources.
"""
import flask_restful
from api.extract_dmn import ExtractDMN


def initialize_routes(api: flask_restful.Api) -> None:
    """Initialize API routes for the Flask application."""
    api.add_resource(ExtractDMN, '/extract')
