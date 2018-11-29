from flask import request
from flask.views import MethodView
from app.models import User
from app.api.v1.auth.response_helpers import response_auth
from app.api.general_helpers import response, check_content_type
import re


class Register(MethodView):
    decorators = [check_content_type]

    def post(self):
        """
        @api {POST} /api/v1/auth/register Register
        @apiVersion 0.0.1
        @apiName Register
        @apiGroup Authentication
        @apiDescription Register a user, generate their token and add them to the database

        @apiParam {String} email Email of the user
        @apiParam {String} password Password of the user

        @apiSuccess (Success) {String} auth_token Auth token to be used for requesting
        @apiSuccess (Success) {String} message Message
        @apiSuccess (Success) {String} status Status
        @apiSuccess (Success) {String} email Email of the user

        @apiSampleRequest /api/v1/auth/register

        @apiExample cURL example
        $ curl -H "Content-Type: application/json" -X POST -d '{"email": "tep@gmail.com", "password": "password"}' http://ec2-35-153-68-36.compute-1.amazonaws.com/api/v1/auth/register

        @apiSuccessExample {json} Success-Response:
            HTTP/1.0 200 OK
            {
                "auth_token": "some random sheet",
                "email": "tep@gmail.com"
                "message": "Successfully registered",
                "status": "success"
            }
        """
        post_data = request.get_json()
        email = post_data.get('email')
        password = post_data.get('password')
        if re.match(r'[^@]+@[^@]+\.[^@]+', email) and len(password) > 4 and not bool(re.search(' +', password)):
            user = User.get_by_email(email)
            if not user:
                new_user = User.create(email, password)
                token = new_user.save()
                return response_auth('success', 'Successfully registered', email, token, 200)
            else:
                return response('failed', 'User already exists, please sign in', 400)
        return response(
            'failed',
            'Missing, wrong email format, or wrong password format (at least 5 characters and contain no spaces)',
            400
        )
