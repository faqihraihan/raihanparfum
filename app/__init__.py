from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from .controller.dashboard import dashb
app.register_blueprint(dashb)

from .controller.database import datab
app.register_blueprint(datab)