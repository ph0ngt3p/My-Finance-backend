from flask import request, _request_ctx_stack
from flask.views import MethodView
from app.models import BlacklistedToken, User
from app.api.general_helpers import response, token_required


class Logout(MethodView):
    decorators = [token_required]

    def post(self):
        """
        @api {POST} /api/v1/auth/logout Logout
        @apiVersion 0.0.1
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
        $ curl -H "Content-Type: application/json" -H "Authorization": "Bearer {auth_token_here}" -X POST -d '{}' http://ec2-35-153-68-36.compute-1.amazonaws.com/api/v1/auth/logout

        @apiSuccessExample {json} Success-Response:
            HTTP/1.0 200 OK
            {
                "message": "Successfully logged out",
                "status": "success"
            }
        """
        ctx = _request_ctx_stack.top
        auth_token = ctx.token
        token = BlacklistedToken.create(auth_token)
        token.blacklist()
        ctx.user = None
        ctx.token = None
        return response('success', 'Successfully logged out', 200)
