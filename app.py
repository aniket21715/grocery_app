from flask import Flask
from web.dbase import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'thisisasecretkey'

    db.init_app(app)

    app.app_context().push()
    return app

app = create_app()

from web.control import *

from web.api import api_bp

app.register_blueprint(api_bp)

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=2345, debug=True)
