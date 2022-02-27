from flask import Blueprint

from .. import models

bp = Blueprint('main', __name__)

from . import forms, routes