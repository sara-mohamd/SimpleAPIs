from flask import Flask
from .DB import db
from .routes.author import authorBluePrint

def createApp():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Load configuration from the Config class
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(authorBluePrint, url_prefix='/authors')

    return app
