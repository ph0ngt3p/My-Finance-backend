from flask import request
from flask.views import MethodView
from app.models import BlacklistedToken, User
from app.api.general_helpers import response


class Logout(MethodView):
    def post(self):
        """
        @api {POST} /api/v1/auth/logout Logout
        @apiName Logout
        @apiGroup Authentication
        @apiDescription Logout a user and blacklist the auth token.

        @apiHeader {String} Authorization Users auth token

        @apiHeaderExample {json} Header-Example:
        {
            "Authorization": "Bearer {auth_token_here}"
        }

        @apiParam {Object} . Nothing is required here

        @apiSuccess (Success) {String} message Message
        @apiSuccess (Success) {String} status Status

        @apiSampleRequest /api/v1/auth/logout

        @apiExample cURL example
        $ curl -H "Content-Type: application/json" -H "Authorization": "Bearer {auth_token_here}" -X POST -d '{}' https://ec2-35-153-68-36.compute-1.amazonaws.com/api/v1/auth/logout

        @apiSuccessExample {json} Success-Response:
            HTTP/1.0 200 OK
            {
                "message": "Successfully logged out",
                "status": "success"
            }
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(' ')[1]
            except IndexError:
                return response('failed', 'Provide a valid auth token', 403)
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    token = BlacklistedToken(auth_token)
                    token.blacklist()
                    return response('success', 'Successfully logged out', 200)
                return response('failed', decoded_token_response, 401)
        return response('failed', 'Provide an authorization header', 403)
