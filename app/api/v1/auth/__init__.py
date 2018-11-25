from flask import Blueprint
from .login import Login
from .logout import Logout
from .register import Register

auth = Blueprint('auth', __name__)

# Register classes as views
registration_view = Register.as_view('register')
login_view = Login.as_view('login')
logout_view = Logout.as_view('logout')

# Add rules for the api Endpoints
auth.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
auth.add_url_rule('/auth/logout', view_func=logout_view, methods=['POST'])
