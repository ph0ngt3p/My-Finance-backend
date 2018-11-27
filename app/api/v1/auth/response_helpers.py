from flask import make_response, jsonify


def response_auth(status, message, email, token, status_code):
    """
    Make a Http response to send the auth token
    :param status: Status
    :param message: Message
    :param email: Email
    :param token: Authorization Token
    :param status_code: Http status code
    :return: Http Json response
    """
    return make_response(jsonify({
        'status': status,
        'message': message,
        'email': email,
        'auth_token': token
    })), status_code
