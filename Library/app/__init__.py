from flask import Flask
from .DB import db
from .routes.author import authorBluePrint
from .routes.book import bookBluePrint
from .routes.borrow_record import borrowBluePrint
from .routes.authentcation import authBluePrint
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/static/swagger.yaml')
def serve_swagger_yaml():
    return send_from_directory('DOC', 'swagger.yaml')


def createApp():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')  # Load configuration from the Config class
    db.init_app(app)


    # Register blueprints
    app.register_blueprint(authorBluePrint, url_prefix='/authors')
    app.register_blueprint(bookBluePrint, url_prefix='/books')
    app.register_blueprint(borrowBluePrint, url_prefix='/borrowRecords')
    app.register_blueprint(authBluePrint, url_prefix='/auth')



    return app
