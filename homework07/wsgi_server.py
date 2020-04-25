import io
import socket
import sys
from datetime import datetime
import asyncore_server as httpd


class AsyncWSGIServer(httpd.AsyncServer):

    def __init__(self, host='localhost', port=9000):
        super(AsyncWSGIServer, self).__init__(host, port)
        self.headers_set = []
    
    def set_app(self, application):
        self.application = application

    def get_app(self):
        return self.application

class AsyncWSGIRequestHandler(httpd.AsyncHTTPRequestHandler):

    def __init__(self):
        self.application = None

    def get_environ(self):
        env = {}
        # Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = io.StringIO(self.data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False
        # Required CGI variables
        env['REQUEST_METHOD']    = self.method 
        env['PATH_INFO']         = self.path    
        env['SERVER_NAME']       = self.server_name       
        env['SERVER_PORT']       = str(self.port) 
        return env

    @staticmethod
    def date_time_string():
        now = datetime.now()
        return now.strftime("%c")

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', self.date_time_string()),
            ('Server', 'WSGIServer 47.2'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def handle_request(self):
        # request_data = self.client_connection.recv(1024)
        # self.request_data = request_data = request_data.decode('utf-8')
        # # Print formatted request data a la 'curl -v'
        # print(''.join(
        #     f'< {line}\n' for line in request_data.splitlines()
        # ))

        # self.parse_request()

        # Construct environment dictionary using request data
        env = self.get_environ()

        # It's time to call our application callable and get
        # back a result that will become HTTP response body

        self.application = self.get_app()
        result = self.application(env, self.start_response)

        # Construct a response and send it back to the client
        self.finish_response(result)

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            # Print formatted response data a la 'curl -v'
            print(''.join(
                f'> {line}\n' for line in response.splitlines()
            ))
            response_bytes = response.encode()
            self.send(response_bytes)
        except:
            pass


# address_family = socket.AF_INET
# socket_type = socket.SOCK_STREAM
# request_queue_size = 1

# args = httpd.parse_args()
# SERVER_ADDRESS = (HOST, PORT) = args.host, args.port
SERVER_ADDRESS = (HOST, PORT) = 'localhost', 9000


def make_server(server_address, application):
    server = AsyncWSGIServer()
    server.set_app(application)
    return server


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'Provide a WSGI application object as module:callable {sys.argv}')
    app_path = sys.argv[1]
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever() 