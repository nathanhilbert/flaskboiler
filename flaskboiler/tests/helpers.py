from openspending.model.dataset import Dataset
from openspending.core import db

from datetime import datetime
import os
import shutil
import json
import csv




def make_account(name='test', fullname='Test User',
                 email='test@test.com', 
                 admin=False, verified=True):
    from openspending.model.account import Account

    # First see if the account already exists and if so, return it
    account = Account.by_email(email)
    if account:
        return account

    # Account didn't exist so we create it and return it
    account = Account()
    account.fullname = fullname
    account.email = email
    account.admin = admin
    account.verified = verified
    db.session.add(account)
    db.session.commit()
    return account


def init_db(app):
    """
    Intialize the database
    """
    db.create_all(app=app)


def clean_db(app):
    db.session.rollback()
    db.drop_all(app=app)
    shutil.rmtree(app.config.get('UPLOADS_DEFAULT_DEST'))

