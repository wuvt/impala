from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from impala import defaults
import os

app = Flask(__name__)
app.config.from_object(defaults)

config_path = os.environ.get('APP_CONFIG_PATH', 'config.py')
if config_path.endswith('.py'):
    app.config.from_pyfile(config_path, silent=True)
else:
    app.config.from_json(config_path, silent=True)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from impala.catalog.models import *
from impala.api import v1
from impala.catalog import views


def init_app():
    app.register_blueprint(v1.bp, url_prefix='/api/v1')


init_app()

if __name__ == "__main__":
    app.run()
