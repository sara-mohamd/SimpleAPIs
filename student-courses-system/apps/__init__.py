from flask import Flask
from .database import db
from .routes.student import studentBP
from .routes.course import courseBP
from .routes.student_course import scBP

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    db.init_app(app)

    app.register_blueprint(studentBP, url_prefix='/students')
    app.register_blueprint(courseBP)
    app.register_blueprint(scBP)


    return app