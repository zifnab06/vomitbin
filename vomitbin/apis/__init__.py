from flask import Blueprint
from flask_restplus import Api

from .v1 import api as v1
blueprint = Blueprint('api', __name__)
api = Api(blueprint, title="vomitbin APIs")

api.add_namespace(v1, path="/v1")
