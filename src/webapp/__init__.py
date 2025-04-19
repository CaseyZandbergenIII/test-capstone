from flask import Flask
from .pages import pages


def create_app():
    # Create Flask isntance
    app = Flask(__name__)
    # Setup configs with key for security
    app.config.from_mapping(SECRET_KEY="dev")
    # Register blueprints for web pages
    app.register_blueprint(pages, url_prefix="/")
    ## TODO Potentailly add parent and child blueprints

    return app
