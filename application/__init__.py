from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

# import routes after declaring application
from application import routes, models, errors, log_conf

if not app.debug:
    log_conf.configure_logging(app)
