from flask import Blueprint

bp = Blueprint('errors', __name__)

from cackle.errors import handlers