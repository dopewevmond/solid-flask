from flask import Blueprint

bp = Blueprint('auth', __name__)

from cackle.auth import email, forms, routes