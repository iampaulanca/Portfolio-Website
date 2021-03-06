from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import json
with open('config.json') as config_file:
    config = json.load(config_file)


app = Flask(__name__)
app.config['SECRET_KEY'] = config.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Flask-Migrate https://www.youtube.com/watch?v=BAOfjPuVby0&t=29s
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = 'blog'
login_manager.login_message_category = 'info'

from PortfolioWebsite import routes
