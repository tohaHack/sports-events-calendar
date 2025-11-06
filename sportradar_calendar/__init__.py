from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Database
    from . import db
    db.init_app(app=app)

    return app