from flask import request
from flask.views import MethodView
from app.models import User
from .auth_helpers import response_auth
from app.api.general_helpers import response
import re


class Register(MethodView):
    """
    View function to register a user via the api
    """

    def post(self):
        """
        Register a user, generate their token and add them to the database
        :return: Json Response with the user`s token
        """
        if request.content_type == 'application/json':
            post_data = request.get_json()
            email = post_data.get('email')
            password = post_data.get('password')
            if re.match(r'[^@]+@[^@]+\.[^@]+', email) and len(password) > 4 and not bool(re.search(' +', password)):
                user = User.get_by_email(email)
                if not user:
                    token = User(email=email, password=password).save()
                    return response_auth('success', 'Successfully registered', token, 201)
                else:
                    return response('failed', 'User already exists, please sign in', 400)
            return response('failed', 'Missing, or wrong email format, or wrong password format (must be at least 5 characters and contain no spaces)', 400)
        return response('failed', 'Content-Type must be application/json', 400)
