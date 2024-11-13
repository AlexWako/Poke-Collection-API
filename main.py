from flask import Flask
from flask.json import jsonify
import os
from collection import collection
from models import db

# Create app
def create_app(test_config = None):

    app = Flask(__name__, instance_relative_config = True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)

    app.register_blueprint(collection)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error': 'Not found'}), 404
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'error': 'Something went wrong'}), 500

    return app
