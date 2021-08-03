from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_assets import Environment
from . import view

db = SQLAlchemy()
mysql = MySQL(cursorclass=DictCursor)
login_manager = LoginManager()
sess = Session()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mysql.init_app(app)
    db.init_app(app)
    sess.init_app(app)
    assets = Environment()
    assets.init_app(app)

    with app.app_context():

        from . import routes
        from .view import routes
        from . import auth
        from .assets import compile_static_assets


        from .view.routes import view_bp
        app.register_blueprint(view_bp)
        app.register_blueprint(auth.auth_bp)

        compile_static_assets(assets)

        return app