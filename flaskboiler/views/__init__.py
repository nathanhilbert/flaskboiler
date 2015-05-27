
from flaskboiler.views.context import home
# from openspending.views.entry import blueprint as entry
from flaskboiler.views.account import blueprint as account
from flaskboiler.views.error import handle_error


def register_views(app):

    app.register_blueprint(home)
    # app.register_blueprint(entry)
    app.register_blueprint(account)
  
    app.error_handler_spec[None][400] = handle_error
    app.error_handler_spec[None][401] = handle_error
    app.error_handler_spec[None][402] = handle_error
    app.error_handler_spec[None][403] = handle_error
    app.error_handler_spec[None][404] = handle_error
    app.error_handler_spec[None][500] = handle_error

    app.error_handler_spec[None][NotModified] = handle_not_modified

    app.jinja_env.filters.update({
        'markdown_preview': filters.markdown_preview,
        'markdown': filters.markdown,
        'format_date': filters.format_date,
        'readable_url': filters.readable_url
    })

