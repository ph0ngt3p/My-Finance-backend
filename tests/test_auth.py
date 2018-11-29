import json
import jwt
import datetime
from unittest.mock import Mock, patch
from app import app
from app.models import User, BlacklistedToken
from nose2.tools import such
from .helpers import fix_case

with such.A('authentication system') as it:
    @it.has_setup
    def setup():
        app.config.from_object('app.config.TestConfig')
        it.app = app.test_client()
        it.mock_id = '1'
        it.mock_email = 'test@mail.com'
        it.mock_password = 'password'
        it.mock_user = User(it.mock_email, it.mock_password)
        it.mock_user.id = it.mock_id
        it.mock_jwt_payload = {
            'exp': datetime.datetime(2018, 11, 22) + datetime.timedelta(seconds=5),
            'iat': datetime.datetime(2018, 11, 22),
            'sub': it.mock_id
        }
        it.mock_jwt_token = jwt.encode(
            it.mock_jwt_payload,
            app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @it.has_teardown
    def teardown():
        pass

    with it.having('a login route'):
        @it.has_setup
        def setup():
            it.endpoint = '/api/v1/auth/login'

        @it.should('return 200 and return the JWT to user if provided correct credentials')
        @fix_case
        @patch('app.models.User.get_by_email')
        def test(mock_get_by_email, case=None):
            mock_get_by_email.return_value = it.mock_user
            it.mock_user.encode_auth_token = Mock(return_value=it.mock_jwt_token)

            expected_response = {
                'auth_token': it.mock_jwt_token,
                'email': it.mock_email,
                'message': 'Successfully logged in',
                'status': 'success'
            }

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            mock_get_by_email.assert_called_once_with(it.mock_email)
            it.mock_user.encode_auth_token.assert_called_once()
            it.assertEqual(response.status_code, 200)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided username does not exist in the database')
        @fix_case
        @patch('app.models.User.get_by_email')
        def test(mock_get_by_email, case=None):
            mock_get_by_email.return_value = None

            expected_response = {
                'message': 'User does not exist or password is incorrect',
                'status': 'failed'
            }

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            mock_get_by_email.assert_called_once_with(it.mock_email)
            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided username and password does not match')
        @fix_case
        @patch('app.models.User.get_by_email')
        def test(mock_get_by_email, case=None):
            mock_get_by_email.return_value = None

            expected_response = {
                'message': 'User does not exist or password is incorrect',
                'status': 'failed'
            }

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': 'wrong_password'}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            mock_get_by_email.assert_called_once_with(it.mock_email)
            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the Content-Type header is not application/json')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='wrong_content_type',
                data=json.dumps({'email': it.mock_email, 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Content-Type must be application/json',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided email is in wrong format')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': 'tepgmail.com', 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Missing or wrong email or password format',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided password is less than 5 characters')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': '123'}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Missing or wrong email or password format',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided password contains spaces')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': 'te p123'}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Missing or wrong email or password format',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)

    with it.having('a register route'):
        @it.has_setup
        def setup():
            it.endpoint = '/api/v1/auth/register'

        @it.should('return 200 and return the JWT to user if the user does not exist in the database and the credentials provided are in correct form')
        @fix_case
        @patch('app.models.User.get_by_email')
        @patch('app.models.User.create')
        def test(mock_create, mock_get_by_email, case=None):
            mock_get_by_email.return_value = None
            mock_create.return_value = it.mock_user
            it.mock_user.save = Mock(return_value=it.mock_jwt_token)

            expected_response = {
                'auth_token': it.mock_jwt_token,
                'email': it.mock_email,
                'message': 'Successfully registered',
                'status': 'success'
            }

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            mock_get_by_email.assert_called_once_with(it.mock_email)
            mock_create.assert_called_once_with(it.mock_email, it.mock_password)
            it.mock_user.save.assert_called_once()
            it.assertEqual(response.status_code, 200)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided email exist in the database')
        @fix_case
        @patch('app.models.User.get_by_email')
        def test(mock_get_by_email, case=None):
            mock_get_by_email.return_value = it.mock_user

            expected_response = {
                'message': 'User already exists, please sign in',
                'status': 'failed'
            }

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            mock_get_by_email.assert_called_once_with(it.mock_email)
            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the Content-Type header is not application/json')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='wrong_content_type',
                data=json.dumps({'email': it.mock_email, 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Content-Type must be application/json',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided email is in wrong format')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': 'tepgmail.com', 'password': it.mock_password}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Missing, wrong email format, or wrong password format (at least 5 characters and contain no spaces)',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided password is less than 5 characters')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': '123'}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Missing, wrong email format, or wrong password format (at least 5 characters and contain no spaces)',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the provided password contains spaces')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({'email': it.mock_email, 'password': 'te p123'}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Missing, wrong email format, or wrong password format (at least 5 characters and contain no spaces)',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)

    with it.having('a logout route'):
        @it.has_setup
        def setup():
            it.endpoint = '/api/v1/auth/logout'
            it.blacklisted_token = BlacklistedToken(it.mock_jwt_token)


        @it.should('return 200, log user out and blacklist the token if provided a correct token in the Authorization header')
        @fix_case
        @patch('app.models.User.get_by_id')
        @patch('app.models.User.decode_auth_token')
        @patch('app.models.BlacklistedToken.create')
        def test(mock_create_blacklisted_token, mock_decode_auth_token, mock_get_user_by_id, case=None):
            mock_get_user_by_id.return_value = it.mock_user
            mock_decode_auth_token.return_value = 1
            mock_create_blacklisted_token.return_value = it.blacklisted_token
            it.blacklisted_token.blacklist = Mock(return_value=None)

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                headers={'Authorization': 'Bearer {}'.format(it.mock_jwt_token)},
                data=json.dumps({}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Successfully logged out',
                'status': 'success'
            }

            mock_get_user_by_id.assert_called_once_with(int(it.mock_id))
            mock_decode_auth_token.assert_called_once_with(it.mock_jwt_token)
            mock_create_blacklisted_token.assert_called_once_with(it.mock_jwt_token)
            it.blacklisted_token.blacklist.assert_called_once()
            it.assertEqual(response.status_code, 200)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 403 if not provided a token in the Authorization header')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                data=json.dumps({}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Provide an authorization header',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 403)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 403 if the token in the Authorization header is in incorrect form')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                headers={'Authorization': '{}'.format(it.mock_jwt_token)},
                data=json.dumps({}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Provide a valid auth token',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 403)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the token provided is expired')
        def test():
            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                headers={'Authorization': 'Bearer {}'.format(it.mock_jwt_token)},
                data=json.dumps({}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Signature expired, Please sign in again',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)


        @it.should('return 400 if the token provided is blacklisted')
        @fix_case
        @patch('app.models.BlacklistedToken.check_blacklist')
        def test(mock_check_blacklist, case=None):
            mock_check_blacklist.return_value = True

            mock_jwt_payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),
                'iat': datetime.datetime.utcnow(),
                'sub': it.mock_id
            }

            mock_jwt_token = jwt.encode(
                mock_jwt_payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            ).decode('utf-8')

            response = it.app.post(
                it.endpoint,
                content_type='application/json',
                headers={'Authorization': 'Bearer {}'.format(mock_jwt_token)},
                data=json.dumps({}),
                follow_redirects=True
            )
            res_body = json.loads(response.get_data(as_text=True))

            expected_response = {
                'message': 'Token was blacklisted, please sign in again',
                'status': 'failed'
            }

            it.assertEqual(response.status_code, 400)
            it.assertDictEqual(res_body, expected_response)

#
# To convert the layer definitions into test cases, you have to call
# `createTests` and pass in the module globals, so that the test cases
# and layer objects can be inserted into the module.
#
it.createTests(globals())
