from flask import Flask
from cackle.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = 'You need to log in to access this page'
login.login_message_category = 'warning'
mail = Mail(app)
moment = Moment(app)

from cackle import routes, models, errors