from datetime import datetime
from sqlalchemy.orm import reconstructor, relationship, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, Boolean, DateTime
from sqlalchemy import BigInteger
from sqlalchemy.sql.expression import false, or_
from sqlalchemy.ext.associationproxy import association_proxy

from flaskboiler.core import db

from flaskboiler.model.common import (MutableDict, JSONType,
                                       DatasetFacetMixin)



class Dataset(db.Model):

    """ The dataset is the core entity of any access to data. All
    requests to the actual data store are routed through it, as well
    as data loading and model generation.

    """
    __tablename__ = 'dataset'
    __searchable__ = ['label', 'description']

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True)
    label = Column(Unicode(2000))
    description = Column(Unicode())


    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)

    datalastupdated = Column(DateTime, default=datetime.utcnow)


    source_id = Column(Integer, ForeignKey('source.id'))
    source = relationship(Source, backref=backref("dataset", uselist=False))

    mapping = Column(MutableDict.as_mutable(JSONType), default=dict)

    ORoperations = Column( MutableDict.as_mutable(JSONType), default=dict)

    prefuncs = Column(MutableDict.as_mutable(JSONType), default=dict)

    dataType = Column(Unicode(2000))

    published = Column(Boolean, default=False)

    loaded = Column(Boolean, default=False)

    tested = Column(Boolean, default=False)


    #TODO
    #tag stuff




    def __init__(self, data = None):
        if data == None:
            return
        self.label = data.get('label')
        self.name = data.get('name', self.label)
        #check if name is already taken
        if Dataset.by_name(self.name):
            for x in range(10):
                newname = self.name + "_" + str(x)
                if not Dataset.by_name(newname):
                    self.name = newname
                    break


        self.description = data.get('description')
        self.ORoperations = data.get('ORoperations', {})
        self.mapping = data.get('mapping', {})
        self.prefuncs = data.get('prefuncs', {})
        self.created_at = datetime.utcnow()
        self.dataType = data.get('dataType')


    def to_json_dump(self):
        """ Returns a JSON representation of an SQLAlchemy-backed object.
        """

        json = {}
        json['fields'] = {}
        json['pk'] = getattr(self, 'id')
        json['model'] = "Dataset"

        fields = ['name', 'label', 'description', 
                 'source_id', 'mapping', 'ORoperations', 'prefuncs', 'dataType','published','loaded', 'tested','dataorg_id']

        for field in fields:
            json['fields'][field] = getattr(self, field)

     
        return json






    @property 
    def tags_str(self):
        output = []
        for t in self.tags:
            output.append(str(t))
        return ",".join(output)


        

    def touch(self):
        """ Update the dataset timestamp. This is used for cache
        invalidation. """
        self.updated_at = datetime.utcnow()
        db.session.add(self)



    def __repr__(self):
        return "%s (%s)" % (self.label, self.id, )

    def update(self, data):
        #not to update name
        self.label = data.get('label')
        self.name = data.get('name', self.label)
            
        self.description = data.get('description')
        self.dataType = data.get('dataType')


    def as_dict(self):
        return {
            'label': self.label,
            'name': self.name,
            'description': self.description,
            'dataType': self.dataType,
        }



    @classmethod
    def all_by_account(cls, account, order=True):
        """ Query available datasets based on dataset visibility. """
        from openspending.model.account import Account
        #limit to certain published/loaded/tested
        criteria = []
        if isinstance(account, Account) and account.is_authenticated():
            criteria += ["1=1" if account.admin else "1=2",
                         cls.managers.any(Account.id == account.id)]
        q = db.session.query(cls).filter(or_(*criteria))
        if order:
            q = q.order_by(cls.label.asc())
        return q

    @classmethod
    def get_all_admin(cls, order=True):
        """ Query available datasets based on dataset visibility. """
        q = db.session.query(cls)
        if order:
            q = q.order_by(cls.label.asc())
        return q

    @classmethod
    def all(cls, order=True):
        """ Query available datasets based on dataset visibility. """
        q = db.session.query(cls)
        if order:
            q = q.order_by(cls.label.asc())
        return q

    @classmethod
    def by_name(cls, name):
        return db.session.query(cls).filter_by(name=name).first()


    @classmethod
    def by_label(cls, label):
        return db.session.query(cls).filter_by(label=label).first()

    @classmethod
    def by_id(cls, id):
        return db.session.query(cls).filter_by(id=id).first()




