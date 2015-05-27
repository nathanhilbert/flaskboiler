from sqlalchemy import *
from migrate import *
from datetime import datetime
from flaskboiler.model.common import MutableDict, JSONType
meta = MetaData()


def upgrade(migrate_engine):
   # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine

    #########################Account
    account = Table('account', meta,
                    Column('id', Integer, primary_key=True),
                    Column('fullname', Unicode(2000)),
                    Column('email', Unicode(2000), unique=True),
                    Column('password', Unicode(2000)),
                    Column('api_key', Unicode(2000)),
                    Column('usg_group', Unicode(2000)),
                    Column('login_hash', Unicode(2000)),
                    Column('admin', Boolean, default=False),
                    Column('verified', Boolean, default=False) 
                    )

    account.create()


    ####################Dataset


    dataset = Table('dataset', meta,
                    Column('id', Integer, primary_key=True),
                    Column('name', Unicode(255), unique=True),
                    Column('label', Unicode(2000)),
                    Column('description', Unicode),
                    Column('category', Unicode()),
                    Column('private', Boolean),
                    Column('created_at', DateTime, default=datetime.utcnow),
                    Column('updated_at', DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow),
                    Column('datalastupdated', DateTime, default=datetime.utcnow),
                    Column('mapping', MutableDict.as_mutable(JSONType), default=dict),
                    Column('ORoperations', MutableDict.as_mutable(JSONType), default=dict),
                    Column('prefuncs', MutableDict.as_mutable(JSONType), default=dict),
                    Column('dataType', Unicode(2000)),
                    Column('published', Boolean, default=False),
                    Column('loaded', Boolean, default=False),
                    Column('tested', Boolean, default=False),
                    )

    dataset.create()




    ################## ManytoMany accounts to datasets
    account_dataset_table = Table(
        'account_dataset', meta,
        Column('dataset_id', Integer, ForeignKey('dataset.id'),
               primary_key=True),
        Column('account_id', Integer, ForeignKey('account.id'),
               primary_key=True)
    )

    account_dataset_table.create()


    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass