import logging
from flask import Flask, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.cache import Cache
import formencode_jinja2
from flask.ext.login import current_user
from flask import request

from flaskboiler import default_settings
#from settings import OPENREFINE_SERVER 
#from settings import LOCKDOWN_FORCE
#from flaskboiler.lib.routing import NamespaceRouteRule
#from flaskboiler.lib.routing import FormatConverter, NoDotConverter
#from flask.ext.superadmin import Admin, model
import flask_admin as admin
from flask import g

logging.basicConfig(level=logging.DEBUG)

# specific loggers
logging.getLogger('markdown').setLevel(logging.WARNING)


db = SQLAlchemy()
login_manager = LoginManager()
cache = Cache()
#auth = HTTPDigestAuth()






def create_app(**config):
    app = Flask(__name__)

    app.config.from_object(default_settings)
    app.config.from_envvar('FLASKBOILER_SETTINGS', silent=True)
    app.config.update(config)

    app.jinja_options['extensions'].extend([
        formencode_jinja2.formfill,
        'jinja2.ext.i18n'
    ])

    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)

    @app.before_request
    def require_basic_auth(*args, **kwargs):
        LOCKDOWN_FORCE = app.config.get('LOCKDOWN_FORCE', False)
        if not current_user.is_authenticated() and request.path not in ["/lockdown", "/__ping__"] and LOCKDOWN_FORCE:
            return redirect("/lockdown", code=302)



    return app


def create_web_app(**config):
    app = create_app(**config)

    app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

    with app.app_context():

        from openspending.views import register_views
        register_views(app)

        from openspending.admin.routes import register_admin
        flaskadmin = admin.Admin(app, name='FIND Admin')
        #flaskadmin = Admin(app, url='/admin', name='admin2')
        register_admin(flaskadmin, db)


    return app
