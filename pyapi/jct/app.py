import sys

from jct.core import app, es_connection, initialise_index

from jct.views.api import blueprint as api
from jct.views.suggest import blueprint as suggest

app.register_blueprint(api, url_prefix="/")
app.register_blueprint(suggest, url_prefix="/suggest")

initialise_index(app, es_connection)

def run_server(host=None, port=None, fake_https=False):
    """
    :param host:
    :param port:
    :param fake_https:
        if fake_https is True, develop can use https:// to access the server
        that can help for debugging Plausible
    :return:
    """
    pycharm_debug = app.config.get('DEBUG_PYCHARM', False)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-d':
            pycharm_debug = True

    if pycharm_debug:
        app.config['DEBUG'] = False
        import pydevd
        pydevd.settrace(app.config.get('DEBUG_PYCHARM_SERVER', 'localhost'),
                        port=app.config.get('DEBUG_PYCHARM_PORT', 6000),
                        stdoutToServer=True, stderrToServer=True)

    run_kwargs = {}
    if fake_https:
        run_kwargs['ssl_context'] = 'adhoc'

    host = host or app.config['HOST']
    port = port or app.config['PORT']
    app.run(host=host, debug=app.config['DEBUG'], port=port,
            **run_kwargs)


if __name__ == "__main__":
    run_server()
