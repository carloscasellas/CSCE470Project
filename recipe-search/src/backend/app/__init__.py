from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Configure CORS globally
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register Blueprints
    from .routes import recipes_bp
    app.register_blueprint(recipes_bp)

    return app
