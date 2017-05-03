from flask import Blueprint

bp = Blueprint('v1', __name__)

from impala.api.v1 import views
