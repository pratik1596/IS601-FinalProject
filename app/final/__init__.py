from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from . import view

db = SQLAlchemy()
mysql = MySQL(cursorclass=DictCursor)
login_manager = LoginManager()

def init_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    mysql.init_app(app)
    db.init_app(app)

    with app.app_context():

        from . import routes
        from .view import routes
        from . import auth


        from .view.routes import view_bp
        app.register_blueprint(view_bp)
        app.register_blueprint(auth.auth_bp)

        return app