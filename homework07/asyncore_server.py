import asyncore
import asynchat
import socket
import multiprocessing
import logging
import mimetypes
import os
from urlparse import parse_qs
import urllib
import argparse
from time import strftime, gmtime

"""
def url_normalize(path):
    if path.startswith("."):
        path = "/" + path
        while "../" in path:
            p1 = path.find("/..")
            p2 = path.rfind("/", 0, p1)
            if p2 != -1:
                path = path[:p2] + path[p1+3:]
            else:
                path = path.replace("/..", "", 1)
                path = path.replace("/./", "/")
            path = path.replace("/.", "")
return path
"""


class FileProducer(object):


def __init__(self, file, chunk_size=4096):
    self.file = file
    self.chunk_size = chunk_size

def more(self):
    if self.file:
        data = self.file.read(self.chunk_size)
        if data:
            return data
        self.file.close()
        self.file = None
    return ""

class AsyncServer(asyncore.dispatcher):

def __init__(self, host="127.0.0.1", port=9000):
    pass

def handle_accepted(self):
    pass

def serve_forever(self):
    pass

class AsyncHTTPRequestHandler(asynchat.async_chat):


def __init__(self, sock):
    pass

def collect_incoming_data(self, data):
    pass

def found_terminator(self):
    pass

def parse_request(self):
    pass

def parse_headers(self):
    pass

def handle_request(self):
    pass

def send_header(self, keyword, value):
    pass

def send_error(self, code, message=None):
    pass

def send_response(self, code, message=None):
    pass

def end_headers(self):
    pass

def date_time_string(self):
    pass

def send_head(self):
    pass

def translate_path(self, path):
    pass

def do_GET(self):
    pass

def do_HEAD(self):
    pass

responses = {
    200: ('OK', 'Request fulfilled, document follows'),
    400: ('Bad Request',
        'Bad request syntax or unsupported method'),
    403: ('Forbidden',
        'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
        'Specified method is invalid for this resource.'),
}

"""
def parse_args():
parser = argparse.ArgumentParser("Simple asynchronous web-server")
parser.add_argument("--host", dest="host", default="127.0.0.1")
parser.add_argument("--port", dest="port", type=int, default=9000)
parser.add_argument("--log", dest="loglevel", default="info")
parser.add_argument("--logfile", dest="logfile", default=None)
parser.add_argument("-w", dest="nworkers", type=int, default=1)
parser.add_argument("-r", dest="document_root", default=".")
return parser.parse_args()
"""


def run():
    server = AsyncServer(host=args.host, port=args.port)
    server.serve_forever()


if name == "main":
    args = parse_args()


logging.basicConfig(
    filename=args.logfile,
    level=getattr(logging, args.loglevel.upper()),
    format="%(name)s: %(process)d %(message)s")
log = logging.getLogger(__name__)

DOCUMENT_ROOT = args.document_root
for _ in xrange(args.nworkers):
    p = multiprocessing.Process(target=run)
    p.start()
