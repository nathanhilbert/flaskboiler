import colander
from flask import Blueprint, render_template, request, redirect
from flask.ext.login import current_user, login_user, logout_user
from flask import current_app
from sqlalchemy.sql.expression import desc, func, or_
from werkzeug.security import check_password_hash, generate_password_hash

from flaskboiler.core import db, login_manager
from flaskboiler.auth import require
from flaskboiler.model.dataset import Dataset
from flaskboiler.model.account import (Account, AccountRegister,
                                        AccountSettings)
from flaskboiler.lib.jsonexport import jsonify
from flaskboiler.lib.helpers import flash_error
from flaskboiler.lib.helpers import flash_notice, flash_success


from wtforms import Form, TextField, PasswordField, validators



blueprint = Blueprint('account', __name__)


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.args.get('api_key')
    if api_key and len(api_key):
        account = Account.by_api_key(api_key)
        if account:
            return account

    api_key = request.headers.get('Authorization')
    if api_key and len(api_key) and ' ' in api_key:
        method, api_key = api_key.split(' ', 1)
        if method.lower() == 'apikey':
            account = Account.by_api_key(api_key)
            if account:
                return account
    return None


@blueprint.route('/login', methods=['GET'])
def login():
    """ Render the login/registration page. """
    disable_cache()
    return render_template('account/login.jade')


@blueprint.route('/login', methods=['POST', 'PUT'])
def login_perform():
    account = Account.by_email(request.form.get('login'))
    #if account is not None and account.verified == True:
    if account is not None:
        if check_password_hash(account.password, request.form.get('password')):
            logout_user()
            login_user(account, remember=True)
            flash_success("Welcome back, " + account.fullname + "!")
            return redirect(url_for('home.index'))
    flash_error(_("Incorrect user name or password!"))
    return login()


@blueprint.route('/register', methods=['POST', 'PUT'])
def register():
    """ Perform registration of a new user """
    disable_cache()
    errors, values = {}, dict(request.form.items())

    try:
        # Grab the actual data and validate it
        data = AccountRegister().deserialize(values)

        #check if email is already registered
            # it is, then send the email hash for the login

        #check that email is real
        #get the domain
        print data['email']
        if (data['email'].find('@') == -1 or data['email'].find('.') == -1):
            raise colander.Invalid(AccountRegister.email,
                    "You must use a valid USG email address")

        domain = data['email'][data['email'].find('@') + 1:]

        if 'EMAIL_WHITELIST' not in current_app.config.keys():
            raise colander.Invalid(AccountRegister.email,
                "System not set correctly.  Please contact the administrator.")

        domainvalid = False

        for domainemail in current_app.config['EMAIL_WHITELIST']:
            if domain.lower() == domainemail.lower():
                domainvalid = True

        if not domainvalid:
            raise colander.Invalid(AccountRegister.email,
                "Your email is not available for registration.  Currently it is only available for US Government emails.")



        # Check if the username already exists, return an error if so
        if Account.by_email(data['email']):
            #resend the hash here to the email and notify the user
            raise colander.Invalid(
                AccountRegister.email,
                "Login Name already exists.  Click reset password.")



        # Create the account
        account = Account()
        account.fullname = data['fullname']
        account.email = data['email']
        

        db.session.add(account)
        db.session.commit()

        # Perform a login for the user
        #login_user(account, remember=True)

        sendhash(account)


        # TO DO redirect to email sent page
        return redirect(url_for('account.email_message', id=account.id))
    except colander.Invalid as i:
        errors = i.asdict()
    return render_template('account/login.jade', form_fill=values,
                           form_errors=errors)

