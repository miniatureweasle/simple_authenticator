"""
Defines a simple HTTPS Server with:
    1. any available port (preferably 8080)
    2. SSL enabled
    3. a self-signed certificate generated with OpenSSL
    4. a daemon thread allowing instantiation within the codebase
"""

import datetime
import ssl
from threading import Thread
from wsgiref.simple_server import make_server

import const
import tools
from core import SimpleWSGIApp



class SimpleHTTPSServer(object):

    def __init__(self):
        """
        Configure a simple server for the REST endpoints.
        If scaling up make this work with a real server.
        """
        self.port = tools.get_free_port()
        self.httpd = make_server('', self.port, SimpleWSGIApp())
        self.httpd.socket = ssl.wrap_socket(
            self.httpd.socket,
            keyfile='./ssl/self-signed.key',
            certfile='./ssl/self-signed.crt',
            server_side=True,
            ssl_version=ssl.PROTOCOL_TLS
        )
        print('Starting server at https://127.0.0.1:{}/...'.format(self.port))  # check
        # make server callable in app by not blocking main thread
        self.thread = Thread(target=self.httpd.serve_forever)
        # ensure the server terminates with the main process
        self.thread.daemon = True
        self.thread.start()


if __name__ == '__main__':
    """Runs server indefinitely"""
    print(const.APP_NAME)
    print(datetime.datetime.now().strftime("%B, %d, %Y - %X"))
    s = SimpleHTTPSServer()
    tools.wait_for_sigint()
