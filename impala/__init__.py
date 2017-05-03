from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from impala.api import v1
import impala.config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from impala.catalog.models import *

def init_app():
    app.register_blueprint(v1.bp, url_prefix='/api/v1')

init_app()

if __name__ == "__main__":
    app.run()
