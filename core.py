import cgi

import urls
from database import db_ops


def notfound_404(environ, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Not Found']


class SimpleWSGIApp:
    """
    Registers and maps URLS to Views.
    """
    def __init__(self):
        self.pathmap = {}
        for method, pattern, view in urls.urlpatterns:
            self.register(method, pattern, view)
        # for easy of use let ensure the DB is setup here
        db_ops.setup()

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(
            environ['wsgi.input'],
            environ=environ
        )
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        handler = self.pathmap.get((method, path), notfound_404)
        return handler(environ, start_response)

    def register(self, method, path, function):
        self.pathmap[method.lower(), path] = function
        return function
