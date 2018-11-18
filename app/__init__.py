from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os

# Initialize application
app = Flask(__name__, static_folder=None)

# Enabling CORS
CORS(app)

# app configuration
app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.Config'
)
app.config.from_object(app_settings)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Error handlers
from app.api import error_handlers

# Register blue prints
from app.api.v1.auth import auth

app.register_blueprint(auth, url_prefix='/api/v1')
