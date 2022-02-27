from flask import Flask
from cackle.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'You need to log in to access this page'
login.login_message_category = 'warning'
mail = Mail()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from cackle.errors import bp as errors_bp
    from cackle.auth import bp as auth_bp
    from cackle.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cackle.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Cackle Social App')
    return app