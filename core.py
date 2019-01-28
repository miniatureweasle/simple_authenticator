"""
Defines a REST-based interfaces without
using a full-fledged web programming framework.

SimpleWSGIApp registers all WSGI based handlers (our views)
and their URLS on instantiation. SimpleWSGIApp can then
be passed to a server installation to handle incoming HTTP requests

"""

import cgi
from typing import List, Callable, Any

import const
import urls
from database import db_ops


def notfound_404(environ: dict, start_response: Callable[..., Any]):
    """No page here"""
    start_response(const.NOT_FOUND, const.TEXT_HEADERS)
    return [b'Not Found']


class SimpleWSGIApp:
    """
    Registers all urlpatterns found in urls.py

    When a request arrives, the method and path are extracted and
    used to dispatch to a view.
    """
    def __init__(self):
        self.pathmap = {}
        for method, pattern, view_func in urls.urlpatterns:
            self.register(method, pattern, view_func)
        # for easy of use lets ensure the DB is setup here
        db_ops.setup()

    def __call__(self, environ: dict, start_response: Callable[..., Any]) -> List[bytes]:
        """
        Before any view is called transform post
        parameters into a dictionary for ease of use
        """
        path = environ['PATH_INFO']
        params = cgi.FieldStorage(
            environ['wsgi.input'],
            environ=environ
        )
        method = environ['REQUEST_METHOD'].lower()
        environ['params'] = {key: params.getvalue(key) for key in params}
        view = self.pathmap.get((method, path), notfound_404)
        return view(environ, start_response)

    def register(self, method: str, path: str, view_func: Callable[..., Any]) -> Callable[..., Any]:
        """Maps methods and URLS to views"""
        self.pathmap[method.lower(), path] = view_func
        return view_func
