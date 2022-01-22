from flask import Flask
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
Bootstrap(app)

from cackle import routes