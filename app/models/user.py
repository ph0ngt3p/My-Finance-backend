from app import app, db, bcrypt
import datetime
import jwt
from .blacklisted_token import BlacklistedToken


class User(db.Model):
    """
    User table schema
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    accounts = db.relationship('Account', backref='account', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')

    @staticmethod
    def create(email, password):
        user = User(email, password)
        return user

    def save(self):
        """
        Persist the user in the database
        :param user:
        :return:
        """
        db.session.add(self)
        db.session.commit()
        return self.encode_auth_token()

    def encode_auth_token(self):
        """
        Encode the Auth token
        :param user_id: User's Id
        :return:
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=app.config.get('AUTH_TOKEN_EXPIRY_DAYS'),
                    seconds=app.config.get('AUTH_TOKEN_EXPIRY_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id
            }
            return jwt.encode(
                payload,
                app.config['SECRET_KEY'],
                algorithm='HS256'
            ).decode('utf-8')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(token):
        """
        Decoding the token to get the payload and then return the user Id in 'sub'
        :param token: Auth Token
        :return:
        """
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            is_token_blacklisted = BlacklistedToken.check_blacklist(token)
            if is_token_blacklisted:
                return 'Token was blacklisted, please sign in again'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired, Please sign in again'
        except jwt.InvalidSignatureError:
            return 'Signature verification failed'

    @staticmethod
    def get_by_id(user_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Check a user by their email address
        :param email:
        :return:
        """
        return User.query.filter_by(email=email).first()

    def reset_password(self, new_password):
        """
        Update/reset the user password.
        :param new_password: New User Password
        :return:
        """
        self.password = bcrypt.generate_password_hash(new_password, app.config.get('BCRYPT_LOG_ROUNDS')) \
            .decode('utf-8')
        db.session.commit()

    def get_paginated_accounts(self, page):
        """
        Get a user's accounts and also paginate the results.
        :param page: Page number
        :return: Accounts of the user.
        """
        paginated_accounts_list = self.accounts.paginate(page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
        return paginated_accounts_list
