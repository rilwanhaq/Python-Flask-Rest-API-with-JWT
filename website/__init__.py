import flask_restful
from flask import Flask
from flask_jwt_extended import JWTManager
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secRET'

    JWTManager(app)

    from .routes import routes
    from .auth import auth

    app.register_blueprint(auth, url_prefix=('/'))
    app.register_blueprint(routes, url_prefix=('/'))

    return app
