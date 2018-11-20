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
        @api {POST} /api/v1/auth/login Login
        @apiName Login
        @apiGroup Authentication
        @apiDescription Login a user if the supplied credentials are correct.

        @apiParam {String} email Email of the user
        @apiParam {String} password Password of the user

        @apiSuccess (Success) {String} auth_token Auth token to be used for requesting
        @apiSuccess (Success) {String} message Message
        @apiSuccess (Success) {String} status Status

        @apiSampleRequest /api/v1/auth/login

        @apiExample cURL example
        $ curl -H "Content-Type: application/json" -X POST -d '{"email": "tep@gmail.com", "password": "password"}' https://ec2-35-153-68-36.compute-1.amazonaws.com/api/v1/auth/login

        @apiSuccessExample {json} Success-Response:
            HTTP/1.0 200 OK
            {
                "auth_token": "some random sheet",
                "message": "Successfully logged in",
                "status": "success"
            }
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
