from flask import make_response, jsonify, request, _request_ctx_stack
from app.models import User


def token_required(f):
    """
    Decorator function to ensure that a resource is access by only authenticated users`
    provided their auth tokens are valid
    :param f:
    :return:
    """
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        ctx = _request_ctx_stack.top
        if auth_header:
            try:
                scheme, auth_token = auth_header.split(' ')
                if scheme != 'Bearer':
                    raise ValueError
            except ValueError:
                return response('failed', 'Provide a valid auth token', 403)
            else:
                decoded_token_response = User.decode_auth_token(auth_token)
                if not isinstance(decoded_token_response, str):
                    current_user = User.get_by_id(decoded_token_response)
                    if not current_user:
                        return response('failed', 'Invalid user', 400)
                    ctx.user = current_user
                    ctx.token = auth_token
                    return f(*args, **kwargs)
                return response('failed', decoded_token_response, 400)
        return response('failed', 'Provide an authorization header', 403)
    return decorated_function


def check_content_type(f):
    """
    Decorator function to ensure content-type is application/json
    :param f:
    :return:
    """
    def decorated_function(*args, **kwargs):
        if request.content_type == 'application/json':
            return f(*args, **kwargs)
        return response('failed', 'Content-Type must be application/json', 400)
    return decorated_function


def response(status, message, status_code):
    """
    Helper method to make an Http response
    :param status: Status
    :param message: Message
    :param status_code: Http status code
    :return:
    """
    return make_response(jsonify({
        'status': status,
        'message': message
    })), status_code
