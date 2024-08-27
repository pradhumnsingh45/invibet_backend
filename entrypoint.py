import os
import time
from config import SETTINGS
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)
db_cred = SETTINGS.DB_CREDENTIALS


rds_url = 'postgresql://{}:{}@{}/{}'.format(db_cred.get('user'), db_cred.get('password'), db_cred.get('host'),
                                            db_cred.get('database'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = rds_url
db = SQLAlchemy(app)


from routes import define_routes

define_routes(app)
