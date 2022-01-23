from flask import Flask
import os
from cackle.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from cackle import routes