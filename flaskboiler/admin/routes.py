

#from flask.ext.superadmin.model.backends.sqlalchemy import ModelAdmin
#from flask.ext.superadmin.model.base import BaseModelAdmin
from flask.ext import wtf
from flask_admin.contrib import sqla
from wtforms.fields import StringField, PasswordField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from flask import flash, current_app
from flask_admin import form

from flask_admin.model.form import InlineFormAdmin
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.contrib.sqla.fields import InlineModelFormList
from flask_admin.form import RenderTemplateWidget
#from flask.ext.superadmin.model.backends.sqlalchemy.orm import AdminModelConverter as _AdminModelConverter
#from flask.ext import superadmin
#from wtforms.ext.sqlalchemy.orm import converts

from flaskboiler.model import Account
from flaskboiler.auth import require
from werkzeug.security import generate_password_hash

from jinja2 import Markup

#from settings import UPLOADED_FILES_DEST

from flaskboiler.model.tags import TAG_OPTIONS

from slugify import slugify



#import copy

#see http://flask-admin.readthedocs.org/en/latest/api/mod_model/




class AccountView(sqla.ModelView):

    #form_overrides = dict(name=PasswordField)

    form_extra_fields = {
        "password1": PasswordField('Password', validators=[DataRequired()]),
        "password2": PasswordField('Password (Again)', validators=[DataRequired()])
    }

    form_excluded_columns = ('password', 'datasets',)


    def validate_form(self, form):
        if form.data['password1'] == None:
            return False
        if form.data['password1'] == "":
            raise ValidationError('Passwords do not match')
        if form.data['password1'] == form.data['password2']:
            return True
        else:
            raise ValidationError('passwords do not match')
        return False

        #if db.session.query(User).filter_by(login=self.login.data).count() > 0:
        #    raise ValidationError('Duplicate username')


    def is_accessible(self):
        return require.account.is_admin()



    # Model handlers
    def on_model_change(self, form, model, is_created=False):
    #def create_model(self, form):
        if form.data['password1'] != None:
            model.password = generate_password_hash(form.data['password1'])
        return




def register_admin(flaskadmin, db):

    from flaskboiler.model import Account

    flaskadmin.add_view(AccountView(Account, db.session, endpoint='useraccount', category="Manager", name="User Management"))
    return flaskadmin

