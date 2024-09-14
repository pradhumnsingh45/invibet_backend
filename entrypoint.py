import os
import time
from config import SETTINGS
from flask import Flask, jsonify
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
from routes.login_routes import login_bp
app.register_blueprint(login_bp, url_prefix='/login')

def define_routes(app):

    @app.route("/public/health", methods=["GET"])
    def health_ping():
        return jsonify({'message': 'success'}), 200
    
define_routes(app)