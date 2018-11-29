from flask import Blueprint
from app.api.general_helpers import response
from .accounts import Accounts

account = Blueprint('account', __name__)

# Register classes as views
accounts_view = Accounts.as_view('accounts')

# Add rules for the api Endpoints
account.add_url_rule('/accounts', view_func=accounts_view, methods=['POST'])
account.add_url_rule('/accounts', view_func=accounts_view, methods=['GET'])


@account.errorhandler(404)
def handle_404_error(e):
    """
    Return a custom message for 404 errors.
    :param e:
    :return:
    """
    return response('failed', 'Account resource cannot be found', 404)


@account.errorhandler(400)
def handle_400_errors(e):
    """
    Return a custom response for 400 errors.
    :param e:
    :return:
    """
    return response('failed', 'Bad Request', 400)
