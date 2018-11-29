from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from click import option
import os
import subprocess

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

# Initialize Flask Migrate
migrate = Migrate(app, db)


@app.cli.command()
@option('--input', default='app')
@option('--output', default='docker/nginx/apidoc')
@option('--template', default=None)
def apidoc(input, output, template):
    cmd = ['apidoc']
    if input:
        cmd.append('--input')
        cmd.append(input)
    if output:
        cmd.append('--output')
        cmd.append(output)
    if template:
        cmd.append('--template')
        cmd.append(template)
    p = subprocess.Popen(cmd)
    p.communicate()
    return p.returncode


# Error handlers
from app.api import error_handlers

# Register blue prints
from app.api.v1.auth import auth
from app.api.v1.account import account

app.register_blueprint(auth, url_prefix='/api/v1')
app.register_blueprint(account, url_prefix='/api/v1')
