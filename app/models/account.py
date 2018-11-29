from app import app, db
from datetime import datetime, timedelta


class Account(db.Model):
    """
    Accounts table schema
    """
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    account_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, nullable=False)
    initial_balance = db.Column(db.BigInteger, nullable=False)
    current_balance = db.Column(db.BigInteger, nullable=False)
    saving_duration = db.Column(db.Interval)
    saving_interest_rate = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity': 'cash',
        'polymorphic_on': account_type
    }

    def __init__(self, name, account_type, user_id, initial_balance, saving_duration=None, saving_interest_rate=None):
        self.name = name
        self.account_type = account_type
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.saving_duration = timedelta(saving_duration * 30) if saving_duration else None
        self.saving_interest_rate = saving_interest_rate

    def save(self):
        """
        Persist an account in the database
        :return:
        """
        db.session.add(self)
        db.session.commit()

    def json(self):
        """
        JSON representation.
        :return:
        """
        return {
            'name': self.name,
            'type': self.account_type,
            'created': self.created_at.isoformat(),
            'ini_bal': self.initial_balance,
            'cur_bal': self.current_balance,
            'sav_dur': self.saving_duration,
            'sav_itr': self.saving_interest_rate,
            'limit': None
        }


class CreditAccount(Account):
    """
    Credit accounts table schema
    """
    __tablename__ = 'credit_accounts'

    __mapper_args__ = {
        'polymorphic_identity': 'credit',
    }
    id = db.Column(db.Integer, db.ForeignKey('accounts.id'), primary_key=True)
    limit = db.Column(db.BigInteger, nullable=False)

    def __init__(self, limit, **kwargs):
        super().__init__(**kwargs)
        self.limit = limit

    def json(self):
        """
        JSON representation.
        :return:
        """
        return {
            'name': self.name,
            'type': self.account_type,
            'created': self.created_at.isoformat(),
            'ini_bal': self.initial_balance,
            'cur_bal': self.current_balance,
            'sav_dur': self.saving_duration,
            'sav_itr': self.saving_interest_rate,
            'limit': self.limit
        }


class AccountFactory(object):
    OBJ_TYPE_MAP = {
        x.polymorphic_identity: x.class_
        for x in Account.__mapper__.self_and_descendants
    }

    def create_account(self, **kwargs):
        acc_type = self.OBJ_TYPE_MAP.get(kwargs['account_type'].lower())
        assert acc_type, "Unknown type: {}".format(kwargs['account_type'].lower())
        return acc_type(**kwargs)
