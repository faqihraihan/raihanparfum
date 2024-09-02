from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

app = Flask(__name__)

app.config.from_pyfile('config.py')


convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention = convention)
db = SQLAlchemy(app, metadata = metadata)

migrate = Migrate(app, db)


from .controller.dashboard import dashb
app.register_blueprint(dashb)

from .controller.database import datab
app.register_blueprint(datab)

from .controller.pelanggan import cust
app.register_blueprint(cust)

from .controller.scan import scan
app.register_blueprint(scan)

from .controller.mobile import mobile
app.register_blueprint(mobile)


def format_telp(value):
    return '-'.join([value[i:i+4] for i in range(0, len(value), 4)])

app.jinja_env.filters['format_telp'] = format_telp

def format_rupiah(value):
    return "Rp. {:0,.0f}".format(value).replace(',', '.')

app.jinja_env.filters['format_rupiah'] = format_rupiah

def format_rupiah_full(value):
    return "Rp. " + "{:0,.2f}".format(value).replace(',', 'x').replace('.', ',').replace('x', '.')

app.jinja_env.filters['format_rupiah_full'] = format_rupiah_full