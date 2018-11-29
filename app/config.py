import os

if os.getenv('FLASK_ENV') == 'development':
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'root')
db_name = os.getenv('DB_NAME', 'my_finance')
db_pass = os.getenv('DB_PASS', '')
db_string = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_name)
db_test_name = db_name + '_test'
db_test_string = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_pass, db_host, db_test_name)


class Config:
    DEBUG = os.getenv('DEBUG', False)
    SECRET_KEY = os.getenv('SECRET_KEY', 'team searekt')
    BCRYPT_HASH_PREFIX = int(os.getenv('BCRYPT_HASH_PREFIX', 14))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL', db_string)
    AUTH_TOKEN_EXPIRY_DAYS = int(os.getenv('AUTH_TOKEN_EXPIRY_DAYS', 1))
    AUTH_TOKEN_EXPIRY_SECONDS= int(os.getenv('AUTH_TOKEN_EXPIRY_SECONDS', 30))
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 10))


class TestConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL_TEST', db_test_string)
    SECRET_KEY = 'secret'
    BCRYPT_HASH_PREFIX = 4
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3
    AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS = 5
