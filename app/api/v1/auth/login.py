from app import bcrypt
from flask import request
from flask.views import MethodView
from app.models import User
from .auth_helpers import response_auth
from app.api.general_helpers import response
import re


class Login(MethodView):
    def post(self):
        """
        Login a user if the supplied credentials are correct.
        :return: Http Json response
        """
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
            if re.match(r'[^@]+@[^@]+\.[^@]+', email) and len(password) > 4:
                user = User.query.filter_by(email=email).first()
                if user and bcrypt.check_password_hash(user.password, password):
                    return response_auth('success', 'Successfully logged in', user.encode_auth_token(user.id), 200)
                return response('failed', 'User does not exist or password is incorrect', 401)
            return response('failed', 'Missing or wrong email format or password is incorrect', 401)
        return response('failed', 'Content-Type must be appication/json', 202)
