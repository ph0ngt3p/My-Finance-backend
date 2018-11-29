
from flask import make_response, jsonify, url_for


def response_created_account(new_account, status_code):
    """
    Method returning the response when an account has been successfully created.
    :param status_code:
    :param new_account: Account
    :return: Http Response
    """
    status = {
        'status': 'success'
    }
    new_acc_info = new_account.json()
    return make_response(jsonify({**status, **new_acc_info})), status_code


def response_paginate_accounts(user, page):
    """
    Get an user's account and also paginate the results.
    Generate previous and next pagination urls
    :param user: Current User
    :param page: Page number
    :return: Pagination next url, previous url and the user buckets.
    """
    pagination = user.get_paginated_accounts(page)
    previous_page = None
    if pagination.has_prev:
        previous_page = url_for('account.accounts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('account.accounts', page=page+1, _external=True)
    items = pagination.items
    return make_response(jsonify({
        'status': 'success',
        'previous': previous_page,
        'next': next_page,
        'total': pagination.total,
        'accounts': [item.json() for item in items]
    })) if items else make_response(jsonify({
        'status': 'success',
        'previous': None,
        'next': None,
        'total': 0,
        'accounts': []
    }))
